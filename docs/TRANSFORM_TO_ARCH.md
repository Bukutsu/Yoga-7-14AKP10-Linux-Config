# Transforming CachyOS to Pure Arch Linux

This guide details how to reclaim your system's identity as "Arch Linux" and how to fully migrate away from CachyOS repositories if you decide to go back to a pure Arch setup for maximum longevity.

## Part 1: Reclaiming the Arch Identity (`/etc/os-release`)

CachyOS uses a package called `cachyos-hooks` to overwrite the system identity during package updates. To permanently stop this and return your system to identifying as Arch Linux:

**1. Remove the CachyOS branding hooks**
Since this package isn't a hard dependency for the system, it can be safely removed:
```bash
sudo pacman -Rs cachyos-hooks
```

**2. Reinstall the base filesystem**
This restores the official Arch Linux `/usr/lib/os-release` file that might have been modified:
```bash
sudo pacman -S filesystem
```

**3. Restore the symlink**
Standard Arch Linux links `/etc/os-release` to the file in `/usr/lib`:
```bash
sudo ln -sf /usr/lib/os-release /etc/os-release
```

**Verification:**
Run `cat /etc/os-release`. It should now report `NAME="Arch Linux"`.

---

## Part 2: Complete Migration to Pure Arch (The "Exit Strategy")

If you ever want to completely drop CachyOS and return to 100% upstream Arch Linux (e.g., if CachyOS stops being maintained):

**1. Remove the CachyOS Repositories**
Edit your pacman configuration:
```bash
sudo micro /etc/pacman.conf
```
Remove or comment out the `[cachyos]` repository blocks (and their `Include` lines) located above `[core]`.

**2. Refresh Pacman Databases**
```bash
sudo pacman -Syy
```
*(Your installed CachyOS packages are now considered "foreign" or local packages.)*

**3. Swap the Kernel**
Move back to the standard Arch kernel to ensure future compatibility:
```bash
sudo pacman -S linux linux-headers
```
*Note: Remember to update your Limine bootloader configuration (`/etc/default/limine`) to point to the new `vmlinuz-linux` kernel and run `sudo limine-update`.*

**4. Replace Scheduler Tools**
Install the official upstream versions of the schedulers from the Arch `extra` repository:
```bash
sudo pacman -S extra/scx-scheds extra/scx-tools
```
*(If you were using `scx-manager`, it will stop receiving updates as it is CachyOS-specific, but your `/etc/scx_loader.toml` will continue to work perfectly with the upstream `scx_loader`)*

**5. Clean Up Leftovers**
List any remaining packages that are no longer in standard repositories:
```bash
pacman -Qm
```
Review the list and remove any CachyOS-specific utilities that you no longer need.