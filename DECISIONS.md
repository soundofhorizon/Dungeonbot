# DECISIONS

## 2026-03-03
- Context: `cogs/ranking.py` contained broken string literals that prevented compilation.
- Decision: Prioritized buildability by replacing malformed message literals with valid English error messages in the affected branches.
- Risk: Some user-facing texts are now mixed-language until encoding normalization is done across the project.
- Follow-up: Normalize file encoding and restore intended JP messages in a dedicated, scoped pass.
