# Changelog

All notable changes to Shape Keys (N-Panel) will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Releases include an `index.json`, so the add-on can be added in Blender as a remote repository (`https://github.com/PsyDreamer-3D/shape_keys_ntab/releases/latest/download/index.json`) and Blender offers updates. The release workflow generates it with Blender's own `extension server-generate`.

### Fixed

- List didn't populate on Blender 5.2 — was calling `template_list` with `MESH_UL_shape_keys`, a `bl_ui`-internal class no longer registered under that name. Replaced with an add-on-owned `OBJECT_UL_shapekeys_ntab`.

## [0.1.0] — 2026-08-31

Initial release.

### Added

- Shape Keys panel in its own N-panel tab (Mesh/Curve/Surface/Lattice objects).
- Add, Remove, New Shape From Mix, and Clear Values operators.
- Specials menu: Move to Top/Up/Down/Bottom.
- Value slider with min/max range and a driven-value indicator.
- Vertex Group and Relative To pickers.
- Mirror button (wraps the built-in topology-aware mirror operator).
