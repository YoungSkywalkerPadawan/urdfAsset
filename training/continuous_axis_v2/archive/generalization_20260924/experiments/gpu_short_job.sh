#!/bin/bash
ROOT=/root/autodl-tmp/axis-generalization-20260924
PY=/root/autodl-tmp/envs/instruct-particulate/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
(
set -e
bash "$ROOT/run_generalization.sh" extract-smoke
"$PY" "$ROOT/gpu_feature_smoke.py" --source /root/autodl-tmp/continuous-axis-training-v2-20260911 --metadata /root/autodl-tmp/axis-diagnostics-20260923/cpu100_inputs/inputs.json --features "$ROOT/features_partfield_4rot" --output "$ROOT/partfield_fit32" --fit --steps 3200
) > "$ROOT/gpu_short.log" 2>&1
code=$?
printf '%s\n' "$code" > "$ROOT/gpu_short.exit"
exit "$code"
