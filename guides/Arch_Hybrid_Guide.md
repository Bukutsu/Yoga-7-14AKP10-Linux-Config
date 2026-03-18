# The "Cachy-Arch" Post-Install Optimization Guide (v3.0)
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
   *(By default, this loads `scx_bpfland`. Use `scx-manager` (GUI) to monitor or switch schedulers).*

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

## Phase 4: Display & Power Optimization (PSR)

Enable Panel Self Refresh to save ~1W of power on the OLED panel.

1. **Add Kernel Parameter:** Append `amdgpu.dcdebugmask=0x600` to your bootloader's kernel command line.
   * **Limine:** Edit `/boot/limine.conf`.
   * **GRUB:** Edit `/etc/default/grub` and run `sudo grub-mkconfig -o /boot/grub/grub.cfg`.
2. **Auto-Brightness (wluma):**
   ```bash
   yay -S wluma
   sudo usermod -aG video $USER
   systemctl --user enable --now wluma.service
   ```
3. **Battery Longevity:** Set the 80% charge limit in your DE (KDE/GNOME) settings.

---

## Phase 5: Hardware-Accelerated Multimedia

1. **Video Acceleration:**
   ```bash
   sudo pacman -S libva-mesa-driver
   ```
2. **Audio (4-Speaker Support):** Native in Kernel 6.18+. Import the EasyEffects presets from the `/audio/easyeffects/` folder in this repo for the best 3D sound profile.

---

## Phase 6: Final Verification
Run `fastfetch`. You should see the **Arch Linux Logo** running on the `linux-cachyos` kernel. 

**Your post-install optimization is complete.**
