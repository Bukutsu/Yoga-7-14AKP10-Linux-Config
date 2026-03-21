# Yoga 7 Strix Point: Pure Arch + Limine Installation Guide

**Goal**: Maximum longevity + verified 3–4W idle power efficiency.

---

## Phase 1: Base Installation (archinstall)
1. Boot **[Arch Linux ISO](https://archlinux.org/download/)**.
2. Connect WiFi:
   ```bash
   iwctl
   # station wlan0 connect YourSSID
   ```
3. Run `archinstall` with these options:
   *   **Disk**: `Btrfs` (snapshots for safety).
   *   **Bootloader**: `Limine` (perfect for single kernel + Btrfs).
   *   **Kernel**: `linux`.
   *   **Graphics**: `AMD / ATI (open-source)`.
   *   **Audio**: `Pipewire`.
   *   **Network**: `NetworkManager`.
   *   Enable `multilib`.
4. **Reboot** into your new Arch system.

---

## Phase 2: Add CachyOS Hybrid Repository
**Follow the [Official CachyOS Wiki Guide](https://wiki.cachyos.org/features/optimized_repos/#adding-our-repositories-to-an-existing-arch-linux-install)** to safely add the CachyOS repository.

---

## Phase 3: Install Optimized Packages
```bash
sudo pacman -S \
    linux-cachyos \
    linux-cachyos-headers \
    scx-scheds \
    scx-tools \
    scx-manager \
    power-profiles-daemon \
    powertop \
    git
```

---

## Phase 4: Apply Kernel Parameters (Limine)
Edit your Limine configuration (typically `/etc/default/limine` or `/boot/limine/limine.conf` depending on how it was installed):
```bash
sudo micro /etc/default/limine
```
Find your kernel command line entry and append your verified flags:
```text
amd_pstate=active pcie_aspm=force
```
If using the wrapper script, update Limine:
```bash
sudo limine-update
```

---

## Phase 5: Enable Services
```bash
sudo systemctl enable --now power-profiles-daemon
sudo systemctl enable --now scx_loader
```

---

## Phase 6: Configure Scheduler (scx-manager)
1. Launch **`scx-manager`** from your application menu.
2. Select **`scx_lavd`** as the scheduler.
3. Configure modes with your verified flags:

| Mode | Flags |
| :--- | :--- |
| **Auto** | `--autopower --cpu-pref-order 4,12,6,14,0,8,2,10,1,3,5,7,9,11,13,15 --lb-low-util-pct 10` |
| **Performance** | `--performance --cpu-pref-order 4,12,6,14,0,8,2,10,1,3,5,7,9,11,13,15 --lb-low-util-pct 0` |
| **Balanced** | `--balanced --cpu-pref-order 4,12,6,14,0,8,2,10,1,3,5,7,9,11,13,15 --lb-low-util-pct 25` |
| **Power-Saver** | `--powersave --cpu-pref-order 4,12,6,14,0,8,2,10,1,3,5,7,9,11,13,15 --lb-low-util-pct 70` |

4. Set default to **`Auto`** (syncs with power-profiles-daemon).

---

## Phase 7: Optional: Deploy WiFi Stability Fix
```bash
git clone https://github.com/Bukutsu/Yoga-7-14AKP10-Linux-Config.git
sudo cp Yoga-7-14AKP10-Linux-Config/configs/system/network/disable-wifi-powersave.conf /etc/NetworkManager/conf.d/
```

---

## Phase 8: Verification
1. **Idle Power**: `sudo powertop` → **Target: 3–4W**
2. **YouTube**: Play 1080p video → **Target: 6–7W**
3. **Scheduler**: `scx_loader status` or check in `scx-manager`.

---

## Exit Strategy (If CachyOS Disappears)
1. Remove CachyOS repo from `/etc/pacman.conf`.
2. `scx-manager` stays installed (no updates, but keeps working).
3. Optionally install standard `linux` kernel: `sudo pacman -S linux linux-headers`.