# IGET v1 Spec

- **Normal Run vs Soft Run**: 
  - Normal Run: runs with all checks.
  - Soft Run: runs with reduced checks.

- **W3 0.5 Color Semantics**:
  - Define usage of colors in different contexts.

- **Nodes A-F**:
  - A: Input handling
  - B: Processing
  - C: Output generation
  - D: Error handling
  - E: Configuration
  - F: Logging

- **Outputs**:
  - Expected outputs from each node in various runs.

- **Config-Driven Behavior**: 
  - Behavior determined by configuration files.
  - **Lint Check**: Must pass lint check if specified in config.

## Example YAML

```yaml
mode: soft
check:
  name: lint
```