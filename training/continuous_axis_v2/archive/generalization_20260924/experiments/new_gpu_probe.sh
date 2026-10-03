set -eu
PY=/root/autodl-tmp/envs/instruct-particulate/bin/python
ROOT=/root/autodl-tmp/axis-generalization-20260924
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
"$PY" - <<'PY'
import sys,torch,torch_scatter
print(sys.version,torch.__version__,torch.cuda.get_device_name())
x=torch.tensor([1.,3.],device='cuda'); idx=torch.tensor([0,0],device='cuda')
assert torch_scatter.scatter_mean(x,idx).item()==2
print('CUDA scatter passed')
PY
"$PY" "$ROOT/check_generalization.py" --source /root/autodl-tmp/continuous-axis-training-v2-20260911
"$PY" - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0,'/root/autodl-tmp/continuous-axis-training-v2-20260911')
from train import verify_snapshot
r=verify_snapshot(Path('/root/autodl-tmp/continuous-axis-training-v2-20260911/prepared'),Path('/root/autodl-tmp/continuous-axis-training-v1-20260911/prepared'))
print('snapshot verified:',r['snapshot_sha256'])
PY
df -h /root/autodl-tmp
