"""Small paired-part networks for an unoriented, fixed rotation axis.

Inputs share one coordinate frame, centered and scaled using the child part.
The projection head predicts a geometric field; it does not propose or rank
candidate axes. All geometry and losses are evaluated in float32, including
when the feature network runs under automatic mixed precision.
"""

import math

import torch
from torch import nn
from torch.nn import functional as F


def gather(values, indices):
    """Gather batched point values using [B, ...] point indices."""
    batch_index = torch.arange(values.shape[0], device=values.device)
    batch_index = batch_index.reshape((-1,) + (1,) * (indices.ndim - 1))
    return values[batch_index, indices]


def unit_direction(direction):
    """Normalize a direction, with a finite fallback for a zero prediction."""
    direction = direction.float()
    length = torch.linalg.vector_norm(direction, dim=-1, keepdim=True)
    fallback = torch.zeros_like(direction)
    fallback[..., 2] = 1.0
    return torch.where(length > 1e-8, direction / length.clamp_min(1e-8), fallback)


def canonical_origin(origin, direction):
    """Choose the point on an axis nearest this shared coordinate frame's zero."""
    origin = origin.float()
    direction = unit_direction(direction)
    return origin - (origin * direction).sum(-1, keepdim=True) * direction


def axis_projection(points, origin, direction):
    """Return each point's orthogonal projection onto its sample's axis."""
    points = points.float()
    origin = origin.float()[:, None, :]
    direction = unit_direction(direction)[:, None, :]
    return origin + ((points - origin) * direction).sum(-1, keepdim=True) * direction


def vector_huber(residual, beta=0.05):
    """Radial Smooth-L1: a scaled Huber penalty on each vector's length.

    Unlike averaging coordinate-wise penalties, this is invariant to a common
    rotation of the residuals. Return one value per vector, without reduction.
    """
    length = torch.linalg.vector_norm(residual.float(), dim=-1)
    return F.smooth_l1_loss(length, torch.zeros_like(length), beta=beta, reduction="none")


@torch.no_grad()
def farthest_points(xyz, count):
    """Deterministic FPS without a point-by-point distance matrix."""
    xyz = xyz.float()
    count = min(count, xyz.shape[1])
    if count < 1:
        raise ValueError("A point cloud must contain at least one point.")
    distance = torch.full(xyz.shape[:2], float("inf"), device=xyz.device)
    farthest = ((xyz - xyz.mean(1, keepdim=True)) ** 2).sum(-1).argmax(-1)
    selected = []
    for _ in range(count):
        selected.append(farthest)
        anchor = gather(xyz, farthest[:, None])
        distance = torch.minimum(distance, ((xyz - anchor) ** 2).sum(-1))
        farthest = distance.argmax(-1)
    return torch.stack(selected, dim=1)


@torch.no_grad()
def nearest_neighbors(queries, reference, count, chunk_size=256):
    """Exact KNN, chunked along both axes to bound pairwise distance memory.

    Return squared distances and reference indices. Neighbor selection is a
    geometric input operation; features gathered at those indices keep their
    usual gradients. Sorting is only used to make the smaller-scale KNN subset
    consistent with the larger neighborhood.
    """
    count = min(count, reference.shape[1])
    if count < 1 or queries.shape[1] < 1 or chunk_size < 1:
        raise ValueError("KNN requires nonempty clouds and positive sizes.")
    all_distances = []
    all_indices = []
    with torch.autocast(device_type=queries.device.type, enabled=False):
        queries = queries.float()
        reference = reference.float()
        for start in range(0, queries.shape[1], chunk_size):
            query = queries[:, start:start + chunk_size]
            best_distance = None
            best_index = None
            for offset in range(0, reference.shape[1], chunk_size):
                block = reference[:, offset:offset + chunk_size]
                # Direct differences avoid catastrophic cancellation when a
                # large parent and a small child share child-scale coordinates.
                distance = (query[:, :, None, :] - block[:, None, :, :]).square().sum(-1)
                index = torch.arange(offset, offset + block.shape[1], device=query.device)
                index = index[None, None, :].expand_as(distance)
                if best_distance is not None:
                    distance = torch.cat((best_distance, distance), dim=-1)
                    index = torch.cat((best_index, index), dim=-1)
                take = min(count, distance.shape[-1])
                best_distance, positions = distance.topk(take, dim=-1, largest=False, sorted=True)
                best_index = torch.gather(index, -1, positions)
            all_distances.append(best_distance)
            all_indices.append(best_index)
    return torch.cat(all_distances, dim=1), torch.cat(all_indices, dim=1)


@torch.no_grad()
def mixed_geometry_anchors(xyz, other_xyz, count, chunk_size=256):
    """Keep global coverage while representing the likely connection region.

    At least half the anchors are global FPS points. Remaining anchors use FPS
    within the closest half of the cloud, with proximity approximated using up
    to 128 FPS landmarks from the other part. This requires O(N * 128) distance
    work, not a full N-by-N search. Contact features are separately evaluated
    against the complete other cloud using exact KNN.

    The global and regional anchor sets may overlap. Keeping that overlap is
    intentional: it retains the coverage guarantee and gives the geometrically
    selected region its allocated token budget without a data-dependent loop.
    """
    count = min(count, xyz.shape[1])
    global_count = (count + 1) // 2
    global_indices = farthest_points(xyz, global_count)
    regional_count = count - global_count
    if regional_count == 0:
        return global_indices

    landmark_indices = farthest_points(other_xyz, min(128, other_xyz.shape[1]))
    landmarks = gather(other_xyz, landmark_indices)
    distance, _ = nearest_neighbors(xyz, landmarks, 1, chunk_size)
    candidate_count = max((xyz.shape[1] + 1) // 2, regional_count)
    candidate_indices = distance[..., 0].topk(
        candidate_count, dim=-1, largest=False, sorted=False
    ).indices
    candidate_xyz = gather(xyz, candidate_indices)
    regional_local_indices = farthest_points(candidate_xyz, regional_count)
    regional_indices = torch.gather(candidate_indices, 1, regional_local_indices)
    return torch.cat((global_indices, regional_indices), dim=1)


class LocalBranch(nn.Module):
    """Shared point features and relative-coordinate neighborhood aggregation."""

    def __init__(self, width):
        super().__init__()
        self.point = nn.Sequential(
            nn.Linear(9, 64),
            nn.GELU(),
            nn.Linear(64, width),
            nn.LayerNorm(width),
        )
        self.relative = nn.Sequential(
            nn.Linear(4, width),
            nn.GELU(),
            nn.Linear(width, width),
        )
        self.aggregate = nn.Sequential(
            nn.Linear(2 * width, width),
            nn.LayerNorm(width),
            nn.GELU(),
        )

    def forward(self, xyz, normal, anchors, neighbor_indices):
        descriptor = torch.cat((xyz, normal, xyz - xyz.mean(1, keepdim=True)), dim=-1)
        point_features = self.point(descriptor)
        relative = gather(xyz, neighbor_indices) - anchors[:, :, None, :]
        radius = torch.linalg.vector_norm(relative.float(), dim=-1, keepdim=True)
        geometry = self.relative(torch.cat((relative, radius), dim=-1))
        neighborhood = gather(point_features, neighbor_indices) + geometry
        pooled = torch.cat((neighborhood.mean(2), neighborhood.amax(2)), dim=-1)
        return self.aggregate(pooled), point_features


class PairedPartEncoder(nn.Module):
    """Encode each role using shared weights and geometry-only contact cues."""

    def __init__(self, width, tokens, neighbors, multiscale, large_neighbors, distance_chunk):
        super().__init__()
        self.tokens = tokens
        self.neighbors = neighbors
        self.large_neighbors = large_neighbors
        self.distance_chunk = distance_chunk
        self.multiscale = multiscale
        self.local_branch = LocalBranch(width)
        if multiscale:
            self.pair_branch = LocalBranch(width)
            self.merge = nn.Sequential(
                nn.Linear(2 * width, width),
                nn.LayerNorm(width),
                nn.GELU(),
            )
        self.position = nn.Sequential(nn.Linear(3, width), nn.LayerNorm(width))
        self.contact = nn.Sequential(
            nn.Linear(5, width),
            nn.GELU(),
            nn.Linear(width, width),
            nn.LayerNorm(width),
        )

    def forward(self, cloud, other, pair_center, pair_scale):
        xyz = cloud[..., :3].float()
        normal = cloud[..., 3:6].float()
        other_xyz = other[..., :3].float()
        if self.multiscale:
            anchor_indices = mixed_geometry_anchors(
                xyz, other_xyz, self.tokens, self.distance_chunk
            )
        else:
            anchor_indices = farthest_points(xyz, self.tokens)
        anchors = gather(xyz, anchor_indices)
        count = self.large_neighbors if self.multiscale else self.neighbors
        _, neighbors = nearest_neighbors(anchors, xyz, count, self.distance_chunk)
        token, point_features = self.local_branch(
            xyz, normal, anchors, neighbors[..., :self.neighbors]
        )
        if self.multiscale:
            # The first branch preserves child-scale detail; this branch sees
            # the complete pair in a bounded global frame and a wider vicinity.
            pair_xyz = (xyz - pair_center) / pair_scale
            pair_anchors = (anchors - pair_center) / pair_scale
            global_token, _ = self.pair_branch(pair_xyz, normal, pair_anchors, neighbors)
            token = self.merge(torch.cat((token, global_token), dim=-1))

        distance, nearest = nearest_neighbors(anchors, other_xyz, 1, self.distance_chunk)
        nearest = nearest[..., 0]
        offset = gather(other_xyz, nearest) - anchors
        anchor_normal = gather(normal, anchor_indices)
        other_normal = gather(other[..., 3:6].float(), nearest)
        alignment = (anchor_normal * other_normal).sum(-1, keepdim=True).abs().clamp(0, 1)
        contact = torch.cat((offset, distance.sqrt(), alignment), dim=-1)
        token = token + self.position(anchors) + self.contact(contact)
        return token, anchors, point_features


class CrossBlock(nn.Module):
    """Simultaneous parent-to-child and child-to-parent feature exchange."""

    def __init__(self, width, heads, dropout):
        super().__init__()
        self.norm = nn.LayerNorm(width)
        self.attention = nn.MultiheadAttention(width, heads, dropout=dropout, batch_first=True)
        self.feedforward = nn.Sequential(
            nn.LayerNorm(width),
            nn.Linear(width, 4 * width),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(4 * width, width),
        )

    def one(self, query, context):
        normalized_query = self.norm(query)
        normalized_context = self.norm(context)
        attended = self.attention(
            normalized_query, normalized_context, normalized_context, need_weights=False
        )[0]
        result = query + attended
        return result + self.feedforward(result)

    def forward(self, parent, child):
        return self.one(parent, child), self.one(child, parent)


class PairAxisNet(nn.Module):
    """Ablatable direct/projection regression with an optional second scale."""

    def __init__(
        self,
        width=128,
        tokens=64,
        neighbors=24,
        heads=4,
        layers=2,
        dropout=0.1,
        head="projection",
        multiscale=False,
        large_neighbors=96,
        distance_chunk=256,
    ):
        super().__init__()
        if head not in {"direct", "projection"}:
            raise ValueError("head must be 'direct' or 'projection'.")
        if width < 1 or heads < 1 or width % heads:
            raise ValueError("width must be positive and divisible by heads.")
        if min(tokens, neighbors, large_neighbors, distance_chunk) < 1 or layers < 0:
            raise ValueError("Neighborhood sizes must be positive and layers nonnegative.")
        if multiscale and large_neighbors <= neighbors:
            raise ValueError("The multiscale branch needs large_neighbors > neighbors.")
        self.head_type = head
        self.distance_chunk = distance_chunk
        self.encoder = PairedPartEncoder(
            width, tokens, neighbors, multiscale, large_neighbors, distance_chunk
        )
        self.role = nn.Parameter(torch.randn(2, width) * 0.02)
        self.blocks = nn.ModuleList(CrossBlock(width, heads, dropout) for _ in range(layers))
        self.shape_encoder = nn.Sequential(
            nn.Linear(12, width), nn.GELU(), nn.LayerNorm(width)
        )
        self.global_context = nn.Sequential(
            nn.Linear(5 * width, 2 * width),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(2 * width, 2 * width),
            nn.LayerNorm(2 * width),
            nn.GELU(),
        )
        self.direction_head = nn.Sequential(
            nn.Linear(2 * width, width), nn.GELU(), nn.Linear(width, 3)
        )
        nn.init.zeros_(self.direction_head[-1].bias)
        with torch.no_grad():
            self.direction_head[-1].bias[2] = 1.0
        if head == "direct":
            self.origin_head = nn.Sequential(
                nn.Linear(2 * width, width), nn.GELU(), nn.Linear(width, 3)
            )
            nn.init.zeros_(self.origin_head[-1].bias)
        else:
            self.projection_head = nn.Sequential(
                nn.Linear(4 * width + 3, width),
                nn.GELU(),
                nn.Linear(width, width),
                nn.GELU(),
                nn.Linear(width, 3),
            )
            nn.init.zeros_(self.projection_head[-1].bias)

    def _interpolate(self, child_xyz, anchors, features):
        distance_squared, indices = nearest_neighbors(
            child_xyz, anchors, 3, self.distance_chunk
        )
        inverse_distance = distance_squared.sqrt().clamp_min(1e-8).reciprocal()
        weights = inverse_distance / inverse_distance.sum(-1, keepdim=True)
        return (gather(features, indices) * weights[..., None]).sum(2)

    def forward(self, parent, child):
        if parent.ndim != 3 or child.ndim != 3 or parent.shape[-1] != 6 or child.shape[-1] != 6:
            raise ValueError("parent and child must have shape [B, N, 6].")
        if parent.shape[0] != child.shape[0] or min(parent.shape[1], child.shape[1]) < 1:
            raise ValueError("Both nonempty clouds must have the same batch size.")
        parent_xyz = parent[..., :3].float()
        child_xyz = child[..., :3].float()
        minimum = torch.minimum(parent_xyz.amin(1), child_xyz.amin(1))
        maximum = torch.maximum(parent_xyz.amax(1), child_xyz.amax(1))
        pair_center = ((minimum + maximum) * 0.5)[:, None, :]
        pair_scale = torch.linalg.vector_norm(maximum - minimum, dim=-1).clamp_min(1e-6)
        pair_scale = pair_scale[:, None, None]

        parent_tokens, _, _ = self.encoder(parent, child, pair_center, pair_scale)
        child_tokens, child_anchors, child_features = self.encoder(child, parent, pair_center, pair_scale)
        parent_tokens = parent_tokens + self.role[0]
        child_tokens = child_tokens + self.role[1]
        for block in self.blocks:
            parent_tokens, child_tokens = block(parent_tokens, child_tokens)

        geometry = []
        for xyz in (parent_xyz, child_xyz):
            geometry.extend((xyz.mean(1), xyz.amax(1) - xyz.amin(1)))
        shape = self.shape_encoder(torch.cat(geometry, dim=-1))
        pooled = torch.cat(
            (
                parent_tokens.mean(1), parent_tokens.amax(1),
                child_tokens.mean(1), child_tokens.amax(1), shape,
            ),
            dim=-1,
        )
        context = self.global_context(pooled)
        direction = unit_direction(self.direction_head(context))
        if self.head_type == "direct":
            origin = canonical_origin(self.origin_head(context), direction)
            return {"origin": origin, "direction": direction}

        interpolated = self._interpolate(child_xyz, child_anchors, child_tokens)
        point_context = context[:, None, :].expand(-1, child.shape[1], -1)
        dense_input = torch.cat((child_features, interpolated, point_context, child_xyz), dim=-1)
        offset = self.projection_head(dense_input).float()
        # An orthogonal projection cannot shift a point along the predicted
        # axis. Its transverse location remains learned independently per point.
        offset = offset - (offset * direction[:, None, :]).sum(-1, keepdim=True) * direction[:, None, :]
        projection_points = child_xyz + offset
        # Equal weights ensure every child point contributes. The line loss
        # below penalizes transverse disagreement between these axis votes.
        origin = canonical_origin(projection_points.mean(1), direction)
        return {"origin": origin, "direction": direction, "projection_points": projection_points}


def rotate_points(points, origin, direction, angles_deg=(45.0, 90.0)):
    """Rodrigues rotation with point identity preserved; output [B, K, N, 3]."""
    if len(angles_deg) < 1:
        raise ValueError("At least one motion supervision angle is required.")
    points = points.float()
    origin = origin.float()[:, None, None, :]
    direction = unit_direction(direction)[:, None, None, :]
    angles = torch.as_tensor(angles_deg, dtype=torch.float32, device=points.device)
    angles = angles.reshape(1, -1, 1, 1) * (math.pi / 180.0)
    centered = points[:, None, :, :] - origin
    parallel = (centered * direction).sum(-1, keepdim=True) * direction
    tangent = torch.cross(direction.expand_as(centered), centered, dim=-1)
    return origin + centered * angles.cos() + tangent * angles.sin() + parallel * (1 - angles.cos())


def _motion_errors(prediction, batch, angles_deg, smooth):
    """Choose one direction sign per object, shared by all points and angles."""
    points = batch["child"][..., :3]
    target = rotate_points(points, batch["origin"], batch["direction"], angles_deg)
    errors = []
    for sign in (1.0, -1.0):
        actual = rotate_points(points, prediction["origin"], sign * prediction["direction"], angles_deg)
        if smooth:
            error = vector_huber(actual - target).mean(dim=(1, 2))
        else:
            error = torch.linalg.vector_norm(actual - target, dim=-1).mean(dim=(1, 2))
        errors.append(error)
    return torch.minimum(errors[0], errors[1])


def axis_loss(
    prediction,
    batch,
    origin_weight=10.0,
    projection_weight=1.0,
    line_weight=0.1,
    motion_weight=0.0,
    motion_angles_deg=(45.0, 90.0),
):
    """Sign/gauge-invariant axis supervision, with optional dense and motion loss."""
    direction = unit_direction(prediction["direction"])
    target_direction = unit_direction(batch["direction"])
    origin = canonical_origin(prediction["origin"], direction)
    target_origin = canonical_origin(batch["origin"], target_direction)
    dot = (direction * target_direction).sum(-1).clamp(-1, 1)
    direction_loss = (1 - dot.square()).mean()
    origin_loss = vector_huber(origin - target_origin).mean()
    zero = origin.new_zeros(())
    projection_loss = zero
    line_loss = zero
    if "projection_points" in prediction:
        if "projection_target" not in batch:
            raise KeyError("Projection training requires batch['projection_target'] after augmentation.")
        projected = prediction["projection_points"].float()
        projection_loss = vector_huber(projected - batch["projection_target"].float()).mean()
        on_final_axis = axis_projection(projected, origin, direction)
        line_loss = vector_huber(projected - on_final_axis).mean()

    motion_loss = zero
    if motion_weight:
        motion_loss = _motion_errors(prediction, batch, motion_angles_deg, smooth=True).mean()
    total = (
        direction_loss + origin_weight * origin_loss
        + projection_weight * projection_loss + line_weight * line_loss
        + motion_weight * motion_loss
    )
    components = {
        "direction_loss": direction_loss,
        "origin_loss": origin_loss,
        "projection_loss": projection_loss,
        "line_loss": line_loss,
        "motion_loss": motion_loss,
    }
    return total, components


@torch.no_grad()
def axis_metrics(prediction, batch):
    """Per-pair metrics; the training loop can also aggregate by asset/family.

    A point-to-axis distance alone misses intersecting axes at a wrong angle.
    Always report it together with angle error; success requires both. Inputs
    use child-size units, while batch['scale'] converts those units to meters.
    """
    direction = unit_direction(prediction["direction"])
    target_direction = unit_direction(batch["direction"])
    origin = canonical_origin(prediction["origin"], direction)
    target_origin = canonical_origin(batch["origin"], target_direction)
    dot = (direction * target_direction).sum(-1).abs().clamp(0, 1)
    sine = torch.linalg.vector_norm(torch.cross(direction, target_direction, dim=-1), dim=-1)
    angle = torch.rad2deg(torch.atan2(sine, dot))
    delta = origin - target_origin
    offset = torch.linalg.vector_norm(torch.cross(delta, target_direction, dim=-1), dim=-1)
    scale = batch["scale"].float().reshape(-1)
    return {
        "angle_deg": angle,
        "origin_to_axis_normalized": offset,
        "origin_to_axis_m": offset * scale,
        "canonical_origin_normalized": torch.linalg.vector_norm(delta, dim=-1),
        "success_5deg_1pct": ((angle <= 5.0) & (offset <= 0.01)).float(),
        "motion_error_normalized": _motion_errors(prediction, batch, (45.0, 90.0), smooth=False),
    }
