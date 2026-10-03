"""Verify all archived bytes against manifests recorded on AutoDL."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
count=0
for manifest in sorted((root/'archive').glob('*/MANIFEST.json')):
    for r in json.loads(manifest.read_text()):
        p=manifest.parent/r['path']
        if not p.is_file(): raise FileNotFoundError(p)
        if p.stat().st_size!=r['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:
            raise ValueError('Hash mismatch or unhydrated LFS pointer: '+str(p))
        count+=1
print(json.dumps(dict(verified_files=count,status='ok')))
