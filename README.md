# 🛠️ bukutsu's System Config
A consolidated repository of configurations, guides, and scripts for creating optimized Linux workstations, primarily targeting Fedora and Arch-based systems on modern AMD hardware.

This repository follows a modular structure to easily reuse components across different machines and setups.

---

## Repository Structure

*   **/guides/**: Long-form documentation, post-install optimization guides, and architectural notes for specific operating systems and hardware.
*   **/configs/**: A collection of "dotfiles" and application presets, organized by category (audio, display, system). These are the building blocks referenced by the guides.
*   **/scripts/**: A collection of standalone shell scripts for system configuration, maintenance, and automation. See the `scripts/README.md` for detailed usage of each script.

---

## Philosophy
The configurations herein are guided by a "Solid Core, Liquid Edge" philosophy:
*   **Solid Core:** Prioritize a stable, official OS base (like Fedora Workstation).
*   **Liquid Edge:** "Inject" performance and hardware-specific optimizations (like `scx` schedulers or power-profiles) in a non-destructive way.

This approach aims for maximum reliability and longevity without sacrificing the "snappiness" and hardware-specific tuning that makes a custom setup feel powerful.

---
*Maintained using Gemini CLI.*
