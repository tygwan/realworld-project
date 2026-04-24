# Configuration

`environment.example.toml` defines the project-level configuration shape.
It is not a secret file and should stay committed.

Local machine-specific paths may be supplied through `.env` using
`.env.example` as a template. Do not commit `.env`.

## Principles

- Keep private raw video and user-provided assets outside git by default.
- Keep generated reconstruction artifacts outside git by default.
- Record the existence, role, and phase usage of user assets in the asset
  registry even when the asset itself is not committed.
- Promote repeated manual settings into this config once they become stable.

