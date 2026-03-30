# AGENTS.md

## Environment
- **OS**: Arch Linux (CachyOS kernel)
- **Desktop**: GNOME
- **User preferences**: Native, simple, open-source solutions. Avoid unnecessary complexity.

## Constraints
- **Android device**: Banking app blocks developer options. Do **not** enable USB debugging or developer options.
- **System changes**: The user typically prefers a "plan first" approach. Wait for explicit approval before executing commands that modify the system.
- **Security**: Avoid installing packages from untrusted sources without verification. Prefer official repositories or well‑vetted AUR packages.

## Common Tasks
- Android screen mirroring to Linux (without developer options) – see `.opencode/plans/android-screen-mirror.md`.
- General system configuration and troubleshooting.
- Package management via `pacman` and AUR helpers (paru).

## Research Approach
When researching solutions, especially for niche tasks (e.g., Android screen mirroring without developer options), follow this systematic process:
1. **Define constraints** (user preferences, security, system limitations).
2. **Search official channels** – Arch Wiki, official repos (`pacman -Ss`), AUR (`aurweb`), and upstream documentation.
3. **Evaluate open‑source projects** – check GitHub/GitLab for active development, star count, recent commits, and license.
4. **Test feasibility** – consider dependencies, integration with the existing desktop (GNOME), and whether the solution meets the core constraints.
5. **Document findings** – create a plan file in `.opencode/plans/` with pros/cons, steps, and alternatives.
6. **Update AGENTS.md** – record the successful approach for future reference.

For Android screen mirroring, the key discovery was that **ScreenStream** (open‑source, F‑Droid) provides a simple HTTP‑based streaming solution that respects the “no developer options” constraint.

## Notes
- Always ask clarifying questions when requirements are ambiguous.
- When suggesting software, provide brief pros/cons and security considerations.
- Remember that the user may be running in a "plan mode" where only research and suggestions are allowed.

## Relevant Files
- `.opencode/plans/android-screen-mirror.md` – detailed plan for Android screen mirroring.
- `README.md` – project overview (if any).