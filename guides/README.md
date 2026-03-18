# Lenovo Yoga 7 2-in-1 (14AKP10) CachyOS Configuration

This is a collection of files and notes for optimizing the Lenovo Yoga 7 2-in-1 14AKP10 (AMD Ryzen AI 7 350) on CachyOS. 

These changes helped transform this laptop into a hyper-efficient, privacy-respecting, developer-focused workstation.

---

## Results
- **Idle Power:** Reduced to ~6.8W - 7.2W (previously ~7.4W) with native PSR active.
- **Active Light Power:** ~8W (yielding ~9 hours of real-world use on the 70Wh battery).
- **Video:** 10-12W draw during YouTube playback with hardware acceleration confirmed via `vainfo` / `mpv`.
- **Audio:** Native 4-speaker support (Kernel 6.18+) + Atmos-style 3D effects via PipeWire/EasyEffects.
- **Screen:** Fixed flickering and enabled power-saving PSR (Panel Self Refresh).

---

## 1. Power and Kernel
- **Display Optimization (PSR):** To reach the "Best State" battery life on the Ryzen AI 300 OLED panel, add `amdgpu.dcdebugmask=0x600` to your bootloader.
    - **Why?** Standard feature masks like `0x8` or `0xA` often fail or cause flickering on Strix Point. `0x600` enables stable **PSR1/2** while explicitly disabling the unstable **Selective Update (SU)** which causes black screens. This allows the GPU to sleep during static images, saving ~1W of power.
    - **Verification:** Run `sudo cat /sys/kernel/debug/dri/0000:04:00.0/eDP-1/psr_state`. A value of `21` or `22` means the panel is successfully in deep sleep.
- **Battery Longevity:** I use the native **Battery Health / Conservation Mode** support in the Desktop Environment (KDE Plasma 6.1+ or GNOME) to limit the charge to 80%.
- I use a systemd service to run `powertop --auto-tune` on boot. The service file is in `system/power/`.

---

## 2. CPU Scheduler (Work & Efficiency)
For a productive coding and web-browsing workflow, I use the eBPF **`scx_bpfland`** scheduler through `scx_loader`. 

- **Why `bpfland`?** Unlike `lavd` (which is gaming-centric), `bpfland` uses a vruntime-based algorithm that excels at prioritizing interactive desktop tasks while aggressively idling background processes.
- **Auto-Power Logic:** The config (`system/scheduler/scx_loader.toml`) uses the `["-m", "auto", "-f"]` flags. This allows the scheduler to natively communicate with `power-profiles-daemon`. When on battery, it automatically throttles background tasks and utilizes the most efficient cores, keeping the CPU in deep C-states longer.
- **Frequency Control:** The `-f` flag enables the scheduler to manage CPU frequencies directly, working in tandem with the `amd_pstate=active` driver for maximum efficiency. 

---

## 3. AMD XDNA 2 NPU (Ryzen AI)
The NPU is fully supported under CachyOS using the `amdxdna` kernel driver.
- It requires **infinite memlock limits** to load models (`echo -e "* soft memlock unlimited\n* hard memlock unlimited" > /etc/security/limits.d/99-npu-memlock.conf`).
- You can run local LLMs (like `deepseek-r1-0528:8b` or `qwen3:8b`) directly on the NPU using **FastFlowLM** (`flm`). 
- *Note:* Depending on your kernel version, the FastFlowLM compiler may require firmware `1.1.2.x` (Protocol 7), while older 6.19 kernels expect `1.0.0.x` (Protocol 6). You may need to manage symlinks in `/lib/firmware/amdnpu/17f0_10/` or wait for kernel 6.20.

---

## 4. Audio Setup
Previously, Linux only used the top two speakers by default. Starting with **Kernel 6.18+**, the subwoofers (bass speakers) are now natively supported via the `alc287-yoga9-bass-spk-pin` quirk. This quirk is automatically applied by the kernel, making all 4 speakers work as a single hardware sink out of the box.

- **EasyEffects:** Since the hardware is now fully active, I use EasyEffects primarily for spatial depth and physical correction using a Dolby Atmos Impulse Response (IR) file.
- **Presets:** Presets are located in `/audio/easyeffects/`.
- **Requirements:** You still need `lsp-plugins-lv2` and `calf` installed for the EQ effects.

---

## 5. GNOME Tweaks & Integration
- I uninstalled `lsp-plugins-standalone` and `zam-plugins-standalone` to remove all the clutter icons from the GNOME app menu.
- I use the Flatpak version of Bazaar (App Store) because it lets you disable background activity in GNOME settings, which saves about 500MB of RAM.
- Auto-brightness is handled by `wluma` using the config in `display/wluma/` (mapped to `iio:device1`).
- **Terminal:** I use **Ptyxis** as the default terminal for better Wayland scaling, GPU acceleration, and built-in container support (Toolbox/Distrobox).
  - Set as default GNOME handler: `gsettings set org.gnome.desktop.default-applications.terminal exec 'ptyxis'`
  - Replaced the default Nautilus "Open in Console" with the AUR package `nautilus-open-any-terminal` and configured it using:
    `gsettings set com.github.stunkymonkey.nautilus-open-any-terminal terminal ptyxis`
  - Exported `TERMINAL=ptyxis` in `.zshrc` for compatibility with older tools.

---

## Other Distributions
- [Fedora CachyOS Hybrid Guide](Fedora_CachyOS_Hybrid_Guide.md): A specialized guide for running Fedora with CachyOS optimizations on this hardware.

Configuration tailored using Gemini CLI on CachyOS/Fedora.
