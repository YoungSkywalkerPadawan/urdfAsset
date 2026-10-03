#!/bin/bash
# Sequential GPU experiments. Stop on any failed command, preserving logs.
set -eu
ROOT=/root/autodl-tmp/axis-generalization-20260924
PY=/root/autodl-tmp/envs/instruct-particulate/bin/python
SOURCE=/root/autodl-tmp/continuous-axis-training-v2-20260911
META=/root/autodl-tmp/axis-diagnostics-20260923/cpu100_inputs/inputs.json
ADAPTER=/root/autodl-tmp/ParticulateDemo/experiments/instruct_particulate/upstream/instruct_particulate/utils/partfield_feature_utils.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
trap 'code=$?; printf "%s\n" "$code" > "$ROOT/pipeline.exit"' EXIT
for phase in E1 E2; do
    printf '%s\n' "$phase" > "$ROOT/pipeline.stage"
    bash "$ROOT/run_generalization.sh" "$phase" > "$ROOT/$phase.log" 2>&1
    printf '0\n' > "$ROOT/$phase.exit"
done
# Require all 32 fixed training pairs to fit before spending a full E3 run.
"$PY" - "$ROOT/partfield_fit32/smoke.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]))
if r['strict_count'] != r['samples']:
    raise SystemExit('E1/E2 done. E3 held: inspect incomplete 32-pair fitting first.')
PY
printf 'PartField_full_cache\n' > "$ROOT/pipeline.stage"
"$PY" "$ROOT/extract_partfield.py" --source "$SOURCE" --metadata "$META" --adapter "$ADAPTER" --output "$ROOT/features_partfield_4rot" --split train --limit 0 --rotations 4 > "$ROOT/cache_train.log" 2>&1
"$PY" "$ROOT/extract_partfield.py" --source "$SOURCE" --metadata "$META" --adapter "$ADAPTER" --output "$ROOT/features_partfield_4rot" --split val --limit 0 --rotations 1 > "$ROOT/cache_val.log" 2>&1
printf 'E3\n' > "$ROOT/pipeline.stage"
FEATURES_DIR="$ROOT/features_partfield_4rot" bash "$ROOT/run_generalization.sh" E3 > "$ROOT/E3.log" 2>&1
printf '0\n' > "$ROOT/E3.exit"
printf 'complete\n' > "$ROOT/pipeline.stage"
