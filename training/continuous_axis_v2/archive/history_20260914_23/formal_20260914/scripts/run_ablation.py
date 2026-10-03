"""Run the four authorized ablations sequentially, with durable status and logs."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def now():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, value):
    temporary = path.with_suffix('.partial')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def run(root, queue, expected_code_sha256):
    sys.path.insert(0, str(root))
    from common import code_digest, config_from, digest, read_json
    from train import verify_snapshot
    queue.mkdir(parents=True, exist_ok=True)
    with (root / '.ablation_training.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError('An ablation queue is already running') from error
        if (queue / 'status.json').exists():
            raise ValueError('Queue status exists; use a new queue directory')
        if code_digest() != expected_code_sha256:
            raise ValueError('Source code differs from the verified launch version')
        names = ['A_direct', 'B_projection', 'C_multiscale', 'D_motion']
        configurations = {name: config_from(root / 'configs' / (name + '.json')) for name in names}
        snapshots = {}
        for name, config in configurations.items():
            output = Path(config['run_dir'])
            if output.exists() and any(output.iterdir()):
                raise ValueError('Training output is not empty: ' + str(output))
            snapshots[name] = verify_snapshot(config['prepared_dir'], config['cache_root'])['snapshot_sha256']
        stage_records = [dict(name=name, state='pending', run_dir=configurations[name]['run_dir']) for name in names]
        status = dict(state='running', runner_pid=os.getpid(), started_at=now(), updated_at=now(),
                      code_sha256=expected_code_sha256, current_stage=None, stages=stage_records,
                      test_evaluation_scheduled=False)
        atomic_json(queue / 'launch_manifest.json', dict(python=sys.executable, project_root=str(root),
            code_sha256=expected_code_sha256, snapshots=snapshots, configs=configurations,
            config_file_hashes={str(p.relative_to(root)): digest(p) for p in sorted((root / 'configs').glob('*.json'))}))
        atomic_json(queue / 'status.json', status)
        current = None
        try:
            for current in stage_records:
                name = current['name']
                config = configurations[name]
                if code_digest() != expected_code_sha256 or config_from(root / 'configs' / (name + '.json')) != config:
                    raise ValueError('Code or configuration changed while queue was active')
                if verify_snapshot(config['prepared_dir'], config['cache_root'])['snapshot_sha256'] != snapshots[name]:
                    raise ValueError('Data changed while queue was active')
                command = [sys.executable, '-u', str(root / 'train.py'), '--config',
                           str(root / 'configs' / (name + '.json')), '--device', 'cuda']
                logfile = queue / (name + '.log')
                current.update(state='running', started_at=now(), log=str(logfile))
                status.update(current_stage=name, updated_at=now())
                started = time.monotonic()
                with logfile.open('x', encoding='utf-8') as stream:
                    process = subprocess.Popen(command, cwd=root, stdin=subprocess.DEVNULL,
                                               stdout=stream, stderr=subprocess.STDOUT)
                    current['pid'] = process.pid
                    atomic_json(queue / 'status.json', status)
                    print(json.dumps(dict(event='stage_started', name=name, pid=process.pid, log=str(logfile))), flush=True)
                    returncode = process.wait()
                current.update(returncode=returncode, finished_at=now(), elapsed_seconds=time.monotonic() - started)
                if returncode != 0:
                    raise RuntimeError(name + ' failed with exit code ' + str(returncode))
                outcome = read_json(Path(config['run_dir']) / 'status.json')
                if outcome.get('smoke_only') or not outcome.get('completed') or outcome.get('epochs_completed') != config['epochs']:
                    raise RuntimeError(name + ' exited without completing the full production run')
                current.update(state='complete', epochs_completed=outcome['epochs_completed'])
                status['updated_at'] = now()
                atomic_json(queue / 'status.json', status)
                print(json.dumps(dict(event='stage_completed', name=name, elapsed_seconds=current['elapsed_seconds'])), flush=True)
            status.update(state='complete', current_stage=None, finished_at=now(), updated_at=now())
            atomic_json(queue / 'status.json', status)
            print(json.dumps(dict(event='queue_completed', stages=names)), flush=True)
        except BaseException as error:
            if current is not None:
                current.update(state='failed', error=str(error))
            status.update(state='failed', error=str(error), updated_at=now())
            atomic_json(queue / 'status.json', status)
            raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--queue-dir', type=Path, required=True)
    parser.add_argument('--expected-code-sha256', required=True)
    args = parser.parse_args()
    run(args.project_root.resolve(), args.queue_dir.resolve(), args.expected_code_sha256)
