#!/bin/bash
set -u
export CUDA_VISIBLE_DEVICES=''
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
/root/autodl-tmp/envs/instruct-particulate/bin/python -u /root/autodl-tmp/axis-diagnostics-20260923/cpu100.py \
  --mode train --threads 1 --batch-size 4 --samples 100 --epochs 120 \
  --eval-every 5 --log-every 25 --variants free_sin2 baseline free_chordal \
  --source /root/autodl-tmp/continuous-axis-training-v2-20260911 \
  --inputs /root/autodl-tmp/axis-diagnostics-20260923/cpu100_inputs \
  --output /root/autodl-tmp/axis-diagnostics-20260923/cpu100_run120
code=$?
printf '%s\n' "$code" > /root/autodl-tmp/axis-diagnostics-20260923/cpu100_run120.exit
exit "$code"
