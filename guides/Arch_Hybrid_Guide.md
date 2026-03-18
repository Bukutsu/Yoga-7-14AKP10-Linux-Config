# The "Cachy-Arch" Post-Install Optimization Guide (v4.0)
**Target Device:** Lenovo Yoga Slim 7 14AKP10 (AMD Ryzen AI 300 Series)
**Goal:** Transform a fresh Arch Linux install into a hyper-optimized "Hybrid" workstation with CachyOS power and Btrfs safety.

---

## Phase 1: Adding CachyOS Power (Kernel & Repos)

Assuming you have a fresh Arch Linux installation (base + desktop environment), we will now inject the CachyOS optimizations.

1. **Enable the CachyOS Repositories:**
   ```bash
   wget https://mirror.cachyos.org/cachyos-repo.tar.xz
   tar xvf cachyos-repo.tar.xz
   cd cachyos-repo
   sudo ./cachyos-repo.sh
   ```
2. **Install the CachyOS Kernel & Sched-EXT Tools:**
   ```bash
   sudo pacman -Syu linux-cachyos linux-cachyos-headers scx-scheds cachyos-settings scx-manager
   ```
3. **Enable the Optimization Services:**
   ```bash
   sudo systemctl enable --now scx_loader.service cachyos-settings.service
   ```
4. **Configure via scx-manager (GUI):**
   Open `scx-manager` and set:
   * **Scheduler:** `scx_bpfland`
   * **Profile:** `Auto`
   * **Extra flags:** *(leave empty — Auto mode already includes `-m auto -f`)*

   > `Auto` mode integrates with `power-profiles-daemon` (battery → powersave slice, AC → performance) and uses `-f` to hand frequency hints directly to `amd_pstate=active`. This gives the best efficiency for coding/browsing/light gaming without manual switching.

---

## Phase 2: The Automatic Safety Net (Btrfs Snapshots)

This setup provides "easy" snapshots that appear directly in your bootloader (Limine, GRUB, or systemd-boot).

1. **Install the Snapshot Synchronization Tools:**
   ```bash
   sudo pacman -S snapper snap-pac inotify-tools
   # If using Limine:
   sudo pacman -S limine-snapper-sync
   # If using GRUB:
   sudo pacman -S grub-btrfs
   ```
2. **Configure Snapper for Root:**
   ```bash
   sudo snapper -c root create-config /
   ```
3. **The Snapshot Fix (Standard Btrfs Layout):**
   ```bash
   sudo btrfs subvolume delete /.snapshots
   sudo mkdir /.snapshots
   sudo mount -a
   ```
4. **Enable Auto-Sync & Maintenance:**
   ```bash
   sudo systemctl enable --now snapper-timeline.timer snapper-cleanup.timer
   # If using Limine (Syncs snapshots to boot menu):
   sudo systemctl enable --now limine-snapper-sync.timer
   ```

---

## Phase 3: AMD XDNA 2 NPU (Ryzen AI) Setup

To use the NPU for local LLMs (e.g., DeepSeek, Qwen) on this hardware:

1. **Memlock Limits:**
   ```bash
   echo -e "* soft memlock unlimited\n* hard memlock unlimited" | sudo tee /etc/security/limits.d/99-npu-memlock.conf
   ```
2. **Drivers:** The `linux-cachyos` kernel includes the `amdxdna` driver. Verify it's loaded:
   ```bash
   lsmod | grep amdxdna
   ```
3. **FastFlowLM (flm):** Install the lightweight NPU runtime:
   ```bash
   curl -fsSL https://fastflowlm.com/install.sh | sh
   ```

---

## Phase 4: Display & Power Optimization

1. **CPU Power Scaling:** Add `amd_pstate=active` to your bootloader's kernel command line.
   * **Limine:** Edit `/boot/limine.conf`.
   * **GRUB:** Edit `/etc/default/grub` → `GRUB_CMDLINE_LINUX_DEFAULT`, then run `sudo grub-mkconfig -o /boot/grub/grub.cfg`.
   * **Verify:** `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver` should output `amd-pstate-epp`.
2. **Boot-time power tuning** (USB autosuspend, NIC power save, wake timers):
   ```bash
   sudo cp configs/system/power/powertop.service /etc/systemd/system/
   sudo systemctl enable --now powertop.service
   ```
3. **ZRAM** (compressed swap-in-RAM — ships enabled by default on CachyOS, verify):
   ```bash
   zramctl  # Should show a zram0 device. If empty, install zram-generator.
   ```
4. **Auto-Brightness (wluma):**
   ```bash
   yay -S wluma
   sudo usermod -aG video $USER
   systemctl --user enable --now wluma.service
   ```
5. **Battery Longevity:** Set the 80% charge limit in your DE (KDE/GNOME) settings.
6. **Wi-Fi Powersave flicker fix (MT7925e):** The default NetworkManager Wi-Fi powersave setting causes screen flickering on this hardware. Disable it:
   ```bash
   sudo cp configs/network/wifi-powersave-off.conf /etc/NetworkManager/conf.d/
   sudo systemctl restart NetworkManager
   ```
   *This sets `wifi.powersave = 2` (disabled). The network reconnects immediately, no reboot needed.*

---

## Phase 5: Hardware-Accelerated Multimedia

1. **Video Acceleration:**
   ```bash
   sudo pacman -S libva-mesa-driver
   ```
2. **Audio (4-Speaker + Quad-Mic):** All 4 speakers are native in Kernel 6.18+ via `alc287-yoga9-bass-spk-pin`. Import the EasyEffects presets from the `/audio/easyeffects/` folder in this repo.
   * **Noise Cancellation:** Use the **RNNoise** plugin in EasyEffects on the mic input for real-time noise removal.
   * **Verify mic sources are active:**
     ```bash
     pactl list sources | grep -E 'Name:|Description:' | grep alsa_input
     # Should show both Mic1 (Digital) and Mic2 (Stereo) sources
     ```
3. **Facial Auth (Howdy):** The IR camera works with `howdy` for Linux facial recognition.
   ```bash
   sudo pacman -S howdy
   # Follow setup: sudo howdy add
   ```

---

## Phase 6: Final Verification

Run `fastfetch`. You should see the **Arch Linux Logo** running on the `linux-cachyos` kernel.

### Hardware Status (83JR / Yoga 7 2-in-1 14AKP10 — Verified on CachyOS)

| Component | Status | Notes |
|---|---|---|
| Radeon 840M/860M GPU | ✅ Works | `libva-mesa-driver` required for HW accel |
| XDNA 2 NPU | ✅ Works | `amdxdna` driver via linux-cachyos |
| OLED touchscreen (10-point) | ✅ Works OOB | Verify: `libinput list-devices` |
| Stylus (Yoga Pen) | ✅ Works OOB | Pressure + tilt via evdev/libinput |
| Auto-rotate (tablet mode) | ✅ Works | `iio-sensor-proxy` is a GNOME dependency |
| Wi-Fi 7 (MT7925e) | ✅ Works | Disable powersave to fix flicker (see Phase 4) |
| Bluetooth 5.4 | ✅ Works OOB | Same MT7925e chip |
| IR camera / Howdy | ✅ Works | See Phase 5 |
| 4 speakers + Dolby Atmos | ✅ Works | Kernel 6.18+ native |
| Quad-mic array | ✅ Works | Two PipeWire sources (Mic1 + Mic2) |
| RNNoise (noise cancel) | ✅ Works | Via EasyEffects mic chain |
| microSD reader | ✅ Works OOB | Standard SDHCI |
| USB-C DisplayPort 2.1 | ✅ Works OOB | Via mesa + kernel |
| Fingerprint reader | ➖ N/A | Not present on all 83JR configs |

**Your post-install optimization is complete.**
