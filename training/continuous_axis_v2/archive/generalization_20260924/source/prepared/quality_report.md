# Geometry audit for continuous-axis v2

Frozen original pairs: 2155; retained: 2147; excluded: 8.
The original split and group assignments are preserved byte-for-byte in splits.json.
All decisions use geometry only. No labels, predictions, validation scores or test scores decide exclusions.
A visual/collision scale contradiction must also be a >100x outlier among all other links; tiny collision placeholders alone do not trigger exclusion.
Child-centred robust scaling replaces whole-scene scaling; source meshes and labels are not rescaled or edited.

| Quarantined asset | Original split | Indexed pairs | Reason |
|---|---|---:|---|
| public/urdf_files_robotisTurtleBot3WaffleForOpenManipulator_47803e7f14 | train | 2 | visual_scale_contradicts_collision_and_other_links |
| public/urdf_files_robotisTurtleBot3Waffle_bc03a53fbe | train | 2 | visual_scale_contradicts_collision_and_other_links |
| public/urdf_files_turtlebot3_waffle_70222b7262 | train | 2 | visual_scale_contradicts_collision_and_other_links |
| public/urdf_files_turtlebot3_waffle_for_open_manipulator_efd0d67380 | train | 2 | visual_scale_contradicts_collision_and_other_links |
