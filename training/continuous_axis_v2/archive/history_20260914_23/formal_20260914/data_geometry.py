"""NumPy geometry shared by preparation, training and GLB inference.

The frame and sampling cues use observed surfaces only, never annotated axes.
"""
import numpy as np


def child_frame(child_xyz, quantile=0.005):
    """A robust child-centred frame; both parts must use this same transform."""
    xyz = np.asarray(child_xyz, dtype=np.float64)
    if xyz.ndim != 2 or xyz.shape[1] != 3 or len(xyz) < 3 or not np.isfinite(xyz).all():
        raise ValueError('Invalid child point cloud')
    bounds = np.quantile(xyz, [quantile, 1.0 - quantile], axis=0)
    center = bounds.mean(axis=0)
    scale = float(np.linalg.norm(bounds[1] - bounds[0]))
    if not np.isfinite(scale) or scale <= 1e-8:
        raise ValueError('Degenerate child surface scale')
    return center.astype(np.float32), scale


def normalize_pair(parent, child, center, scale):
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError('Scale must be finite and positive')
    result = []
    for cloud in (parent, child):
        value = np.asarray(cloud, dtype=np.float32).copy()
        if value.ndim != 2 or value.shape[1] != 6 or not np.isfinite(value).all():
            raise ValueError('Expected finite XYZ and normals')
        value[:, :3] = (value[:, :3] - center) / scale
        result.append(value)
    return tuple(result)


def axis_projection(xyz, origin, direction):
    """Orthogonal projection of the actual (possibly augmented) input points."""
    direction = np.asarray(direction, dtype=np.float32)
    direction = direction / max(float(np.linalg.norm(direction)), 1e-12)
    origin = np.asarray(origin, dtype=np.float32)
    return (origin + ((np.asarray(xyz) - origin) @ direction)[:, None] * direction).astype(np.float32)


def _nearest_distance(xyz, other):
    # SciPy is optional; both paths query observed geometry and bound memory.
    try:
        from scipy.spatial import cKDTree
        return cKDTree(np.asarray(other, dtype=np.float64)).query(xyz, workers=1)[0]
    except ImportError:
        reference = np.asarray(other, dtype=np.float64)
        result = []
        for begin in range(0, len(xyz), 128):
            query = np.asarray(xyz[begin:begin + 128], dtype=np.float64)
            minimum = np.full(len(query), np.inf)
            for offset in range(0, len(reference), 1024):
                block = reference[offset:offset + 1024]
                distance2 = ((query[:, None] - block[None]) ** 2).sum(-1)
                minimum = np.minimum(minimum, distance2.min(axis=1))
            result.append(np.sqrt(minimum))
        return np.concatenate(result)


def nearby_weights(parent_pool, child_pool):
    """Soft geometry-only proximity weights, with a uniform floor.

    A disconnected pair falls back to uniform weights instead of manufacturing
    a contact. Uniform global samples are reserved separately by sample_pair.
    """
    _, scale = child_frame(np.asarray(child_pool)[:, :3])
    result = []
    for cloud, other in ((parent_pool, child_pool), (child_pool, parent_pool)):
        distance = _nearest_distance(np.asarray(cloud)[:, :3], np.asarray(other)[:, :3])
        if distance.min() > 2.0 * scale:
            weights = np.ones(len(distance), dtype=np.float64)
        else:
            weights = 0.05 + np.exp(-(distance - distance.min()) / max(0.15 * scale, 1e-12))
        result.append((weights / weights.sum()).astype(np.float64))
    return tuple(result)


def _mixed_indices(size, count, rng, local_fraction, weights):
    if size <= 0 or count <= 0:
        raise ValueError('Point pool and requested count must be positive')
    local_count = int(np.floor(count * local_fraction))
    global_count = count - local_count
    global_indices = rng.choice(size, global_count, replace=global_count > size)
    if not local_count:
        return global_indices
    probability = np.asarray(weights, dtype=np.float64).copy()
    if probability.shape != (size,) or not np.isfinite(probability).all() or np.any(probability < 0):
        raise ValueError('Invalid proximity weights')
    if size >= count:
        probability[global_indices] = 0
    if probability.sum() <= 0:
        probability[:] = 1
        if size >= count:
            probability[global_indices] = 0
    probability /= probability.sum()
    local_indices = rng.choice(size, local_count, replace=size < count, p=probability)
    indices = np.concatenate([global_indices, local_indices])
    rng.shuffle(indices)
    return indices


def sample_pair(parent_pool, child_pool, points, rng, local_fraction=0.0, weights=None):
    """Sample each part, reserving at least 50% uniformly sampled global points."""
    if not 0.0 <= local_fraction <= 0.5:
        raise ValueError('local_fraction must be between 0 and 0.5')
    pools = [np.asarray(parent_pool), np.asarray(child_pool)]
    for pool in pools:
        if pool.ndim != 2 or pool.shape[1] != 6 or not np.isfinite(pool).all():
            raise ValueError('Point pools must contain finite XYZ and normals')
    if local_fraction and weights is None:
        weights = nearby_weights(*pools)
    result = []
    for index, pool in enumerate(pools):
        probability = weights[index] if local_fraction else None
        chosen = _mixed_indices(len(pool), points, rng, local_fraction, probability)
        result.append(np.array(pool[chosen], dtype=np.float32, copy=True))
    return tuple(result)
