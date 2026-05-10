# AGENTS.md

**Hardware** — Lenovo Yoga 7 2-in-1 14AKP10 · AMD Ryzen AI 7 350 (Strix Point, 8C/16T) · 2.8K 120Hz OLED · Realtek RTL892AE · ALC3306 (4-speaker) · Arch Linux (CachyOS kernel) · Limine · GNOME Wayland · Fish · Ghostty

**Constraints** — Never enable USB debugging (banking app blocks dev options). Plan first before system-modifying commands. Anything touching `/boot/limine.conf`, bootloader, kernel, or removing critical packages needs explicit approval.

**Key commands (non-obvious)** — `sudo ./scripts/arch-fortify.py` (--dry, --restore, --skip hooks,limine, --list-backups). `./scripts/setup-flatpak-fonts.sh sync|state|unsync`. Kernel params in `/etc/default/limine` (not grub). Audio quirk: `/etc/modprobe.d/alc3306-yoga-fix.conf` → `options snd-hda-intel model=(null),alc287-yoga9-bass-spk-pin`. After any kernel/module change: `sudo mkinitcpio -P`.

**Gotchas** — No TLP (use power-profiles-daemon; TLP conflicts with AMD ACPI profiles). Screen recording broken on GNOME 49.x (wait for GNOME 50). limine-snapper-restore hardcodes terminal list missing Ghostty (fix: `~/.config/environment.d/override.conf`). UFW not needed (behind NAT).
