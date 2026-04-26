# AGENTS.md

**Agent name**: Abigail

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
- Terminal integration (Ghostty ↔ Nautilus context menu) – requires `ghostty-nautilus` package.

## Research Approach
A systematic methodology for any research task:

1. **Define the problem & constraints** – clarify requirements, user preferences, and any hard limitations (e.g., security, no developer options).
2. **Search official/standard channels** – Arch Wiki, official repositories (`pacman -Ss`), AUR, upstream documentation. These are the most trusted and well‑maintained sources.
3. **Evaluate community/alternative solutions** – open‑source projects on GitHub/GitLab: assess activity (recent commits, stars, forks), license, and community feedback. Check if actively maintained.
4. **Test feasibility** – examine dependencies, integration with existing system (e.g., desktop environment), and whether the solution meets core constraints. If possible, try a lightweight test or review user reports.
5. **Document findings** – create a plan file in `.opencode/plans/` with a clear summary: recommended solution, alternatives, steps, and pros/cons.
6. **Record successful approach** – update `AGENTS.md` (or knowledge base) with discovered solution and pitfalls to avoid.

## Notes
- Always ask clarifying questions when requirements are ambiguous.
- When suggesting software, provide brief pros/cons and security considerations.
- Remember that the user may be running in a "plan mode" where only research and suggestions are allowed.

## Relevant Files
- `.opencode/plans/android-screen-mirror.md` – detailed plan for Android screen mirroring.
- `README.md` – project overview (if any).