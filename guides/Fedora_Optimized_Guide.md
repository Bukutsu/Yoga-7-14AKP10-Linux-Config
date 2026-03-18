# Lenovo Yoga 7 (14AKP10) Long-Term Optimization Guide (v4.0)
**Goal:** Maximum Reliability (5+ Year Target) + Peak Hardware Optimization.
**Base OS:** Fedora Workstation (Official) | **Kernel:** Fedora Stock (Stable)

---

## 🛡️ Phase 1: The "Invincible" Core (Reliability & Safety)
We use Fedora's official vetted kernel but add a safety net to ensure you can always "undo" any change.

1. **Install Snapper & DNF Plugin:**
   ```bash
   sudo dnf install snapper grub-btrfs python3-dnf-plugin-snapper
   ```
2. **Configure Root Snapshots:**
   ```bash
   sudo snapper -c root create-config /
   sudo systemctl enable --now snapper-timeline.timer snapper-cleanup.timer
   ```
3. **Inject Snapshots into GRUB:**
   ```bash
   sudo grub2-mkconfig -o /boot/grub2/grub.cfg
   sudo systemctl enable --now grub-btrfsd.service
   ```
   *Benefit:* If an update ever glitches, reboot into a previous snapshot from the GRUB menu.

---

## ⚡ Phase 2: The "Performance Injection" (Optimization)
We gain the "CachyOS feel" without replacing the core system kernel.

1. **Enable Sched-EXT (scx) via COPR:**
   ```bash
   sudo dnf copr enable bieszczaders/kernel-cachyos-addons
   sudo dnf install scx-scheds scx-manager
   ```
2. **Enable the SCX Service:**
   ```bash
   sudo systemctl enable --now scx.service
   ```
3. **The "Bpfland" Setting:** Open `scx-manager` (GUI) and select **`scx_bpfland`**. 
   *Why:* This scheduler prioritizes UI/interactive tasks on your Zen 5 cores, giving you the snappiest possible desktop experience.

---

## 🔋 Phase 3: Hardware Longevity (Physical Health)
To make the laptop physically last 5+ years.

1. **Battery Health (Charge Limit):** 
   * **KDE:** System Settings -> Power Management -> Advanced -> Set Charge Limit to **80%**.
   * **GNOME:** Settings -> Power -> Battery Health.
   *Benefit:* Effectively doubles the lifecycle of your battery by preventing 100% "cooking."
2. **OLED Protection (PSR):** 
   ```bash
   sudo grubby --update-kernel=ALL --args="amdgpu.dcdebugmask=0x600"
   ```
   *Benefit:* Enables Panel Self Refresh (PSR) to save ~1W and reduce heat. 
   *Verification:* `sudo cat /sys/kernel/debug/dri/0000:04:00.0/eDP-1/psr_state` (Value 21/22 is success).

---

## 🧠 Phase 4: AMD Ryzen AI (NPU) & Development
Offloading AI tasks to the NPU to reduce CPU/GPU wear.

1. **Memlock Limits:**
   ```bash
   echo -e "* soft memlock unlimited\n* hard memlock unlimited" | sudo tee /etc/security/limits.d/99-npu-memlock.conf
   ```
2. **FastFlowLM (flm):**
   ```bash
   curl -fsSL https://fastflowlm.com/install.sh | sh
   ```
3. **Clean Development (Distrobox):** 
   *Instead of installing dev tools on your host, use containers:*
   ```bash
   sudo dnf install distrobox
   distrobox create -n dev-env -i fedora:latest
   ```

---

## 🎬 Phase 5: Hardware-Accelerated Multimedia
Ensure the 14AKP10 hardware is fully utilized for audio/video.

1. **Enable RPM Fusion & Codecs:**
   ```bash
   sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
   sudo dnf swap ffmpeg-free ffmpeg --allowerasing
   sudo dnf install mesa-va-drivers-freeworld
   ```
2. **Audio Presets:** Import your EasyEffects presets from `/audio/easyeffects/` for the 4-speaker Atmos profile.

---

## Phase 6: Verify
Run `fastfetch`. You have the **Official Fedora Logo** and **Stock Kernel**, but your system is powered by **`scx_bpfland`**, has a **Btrfs Safety Net**, and is physically protected for a long life.

**Your Yoga 7 is now a high-integrity professional workstation.**
