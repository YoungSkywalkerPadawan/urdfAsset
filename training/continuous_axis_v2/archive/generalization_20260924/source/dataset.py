"""Child-scaled pair loading and source/family/object/joint sampling."""
import collections
import hashlib
import json
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import Dataset, WeightedRandomSampler
try:
    from .data_geometry import axis_projection, nearby_weights, normalize_pair, sample_pair
except ImportError:
    from data_geometry import axis_projection, nearby_weights, normalize_pair, sample_pair


def _seed(value):
    return int(hashlib.sha256(value.encode()).hexdigest()[:8], 16)


def _rows(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]


def rotate_uniform(rng):
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q = q @ np.diag(np.sign(np.diag(r)))
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    return q.astype(np.float32)


class AxisDataset(Dataset):
    def __init__(self, prepared, split, points=2048, seed=42, augment=False,
                 include_auxiliary=False, jitter=0.001, normal_dropout=0.1,
                 cache_root=None, local_fraction=0.0):
        self.root = Path(prepared)
        self.rows = _rows(self.root / f'{split}_continuous.jsonl')
        if include_auxiliary:
            self.rows += _rows(self.root / f'{split}_auxiliary.jsonl')
        if cache_root is None:
            config = json.loads((self.root / 'config.json').read_text(encoding='utf-8'))
            cache_root = config['cache_root']
            if not Path(cache_root).is_absolute():
                cache_root = self.root / cache_root
        self.cache_root = Path(cache_root).resolve()
        self.points, self.seed, self.augment = points, seed, augment
        self.epoch, self.jitter, self.normal_dropout = 0, jitter, normal_dropout
        self.local_fraction = local_fraction
        if not 0 <= local_fraction <= 0.5:
            raise ValueError('At least half the points must be global samples')
        self._weights = collections.OrderedDict()

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        index, draw = index if isinstance(index, tuple) else (index, 0)
        row = self.rows[index]
        rng = np.random.default_rng(_seed(f'{self.seed}/{self.epoch if self.augment else 0}/{row["id"]}/{draw}'))
        pools = []
        for field in ('parent_file', 'child_file'):
            path = (self.cache_root / row[field]).resolve()
            if not path.is_relative_to(self.cache_root):
                raise ValueError('Cache path escaped cache_root')
            pools.append(np.load(path, mmap_mode='r', allow_pickle=False))
        weights = None
        if self.local_fraction:
            key = (row['parent_file'], row['child_file'])
            weights = self._weights.pop(key, None)
            if weights is None:
                weights = nearby_weights(*pools)
            self._weights[key] = weights
            if len(self._weights) > 256:
                self._weights.popitem(last=False)
        parent, child = sample_pair(*pools, self.points, rng, self.local_fraction, weights)
        center = np.asarray(row['center'], dtype=np.float32)
        scale = float(row['scale'])
        parent, child = normalize_pair(parent, child, center, scale)
        origin = np.asarray(row['origin'], dtype=np.float32).copy()
        direction = np.asarray(row['direction'], dtype=np.float32).copy()
        if self.augment:
            rotation = rotate_uniform(rng)
            origin, direction = origin @ rotation.T, direction @ rotation.T
            for cloud in (parent, child):
                cloud[:, :3] = cloud[:, :3] @ rotation.T
                cloud[:, 3:] = cloud[:, 3:] @ rotation.T
                cloud[:, :3] += np.clip(rng.normal(0, self.jitter, cloud[:, :3].shape), -3 * self.jitter, 3 * self.jitter)
                if rng.random() < self.normal_dropout:
                    cloud[:, 3:] = 0
        # The target is recomputed after jitter: it projects the points actually
        # seen by the network onto the transformed authored axis.
        projection = axis_projection(child[:, :3], origin, direction)
        return dict(parent=torch.from_numpy(parent), child=torch.from_numpy(child),
                    origin=torch.from_numpy(origin), direction=torch.from_numpy(direction),
                    scale=torch.tensor(scale, dtype=torch.float32), center=torch.from_numpy(center),
                    row_index=index, projection_target=torch.from_numpy(projection))


class BalancedDraws:
    """Equal source -> equal frozen group -> equal asset -> equal joint."""
    def __init__(self, rows, samples, seed, epoch, auxiliary_fraction=0):
        if not 0 <= auxiliary_fraction < 1:
            raise ValueError('auxiliary_fraction must be in [0,1)')
        self.samples, self.seed, self.epoch = samples, seed, epoch
        kinds = collections.defaultdict(list)
        for index, row in enumerate(rows):
            if row['type'] not in ('continuous', 'revolute'):
                raise ValueError('Unexpected joint type')
            kinds[row['type']].append(index)
        if auxiliary_fraction and not kinds['revolute']:
            raise ValueError('No bounded auxiliary rows')
        if not kinds['continuous']:
            raise ValueError('No continuous rows')
        weights = [0.0] * len(rows)
        for kind, indices in kinds.items():
            mass = auxiliary_fraction if kind == 'revolute' else 1 - auxiliary_fraction
            sources = {rows[i]['source'] for i in indices}
            groups = collections.defaultdict(set)
            assets = collections.defaultdict(set)
            joints = collections.Counter()
            for i in indices:
                row = rows[i]
                groups[row['source']].add(row['group'])
                assets[(row['source'], row['group'])].add(row['asset_key'])
                joints[(row['source'], row['group'], row['asset_key'])] += 1
            for i in indices:
                row = rows[i]
                weights[i] = mass / len(sources) / len(groups[row['source']]) / len(assets[(row['source'], row['group'])]) / joints[(row['source'], row['group'], row['asset_key'])]
        self.weights = weights

    def __len__(self):
        return self.samples

    def __iter__(self):
        generator = torch.Generator().manual_seed(self.seed + self.epoch)
        sampler = WeightedRandomSampler(self.weights, self.samples, replacement=True, generator=generator)
        return iter((index, draw) for draw, index in enumerate(sampler))
