#!/bin/bash
export CUDA_VISIBLE_DEVICES=''
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export PYTHONUNBUFFERED=1
ROOT=/root/autodl-tmp/axis-diagnostics-20260923
/root/autodl-tmp/envs/instruct-particulate/bin/python "$ROOT/cpu_full.py" --source /root/autodl-tmp/continuous-axis-training-v2-20260911 --metadata "$ROOT/cpu100_inputs/inputs.json" --output "$ROOT/cpufull_chordal_accum_run120" --epochs 120 --batch-size 4
code=$?
printf '%s\n' "$code" > "$ROOT/cpufull_chordal_accum_run120.exit"
exit "$code"
