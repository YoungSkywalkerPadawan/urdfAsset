#!/bin/bash
set -eu
ROOT=/root/autodl-tmp/axis-generalization-20260924
PY=/root/autodl-tmp/envs/instruct-particulate/bin/python
SOURCE=/root/autodl-tmp/continuous-axis-training-v2-20260911
META=/root/autodl-tmp/axis-diagnostics-20260923/cpu100_inputs/inputs.json
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
MODE=${1:?Use E1, E2, E3 or extract-smoke}
case "$MODE" in
  extract-smoke)
    exec "$PY" "$ROOT/extract_partfield.py" --source "$SOURCE" --metadata "$META" \
      --adapter /root/autodl-tmp/ParticulateDemo/experiments/instruct_particulate/upstream/instruct_particulate/utils/partfield_feature_utils.py \
      --output "$ROOT/features_partfield_4rot" --split train --limit 32 --rotations 4
    ;;
  E1) EXTRA=(--rotation-count 1) ;;
  E2) EXTRA=(--rotation-count 4) ;;
  E3) : "${FEATURES_DIR:?Set complete train/val feature cache directory}"; EXTRA=(--rotation-count 4 --features "$FEATURES_DIR") ;;
  *) echo 'Unknown experiment' >&2; exit 2 ;;
esac
exec "$PY" "$ROOT/cpu_full.py" --source "$SOURCE" --metadata "$META" \
  --output "$ROOT/${MODE}_run120" --device cuda --epochs 120 --batch-size 4 --micro-batch-size 4 \
  --dropout .05 --weight-decay .0001 "${EXTRA[@]}"
