# Transforming CachyOS to Pure Arch Linux

This guide details how to fully migrate away from CachyOS repositories if you decide to go back to a pure Arch setup for maximum longevity.

## Complete Migration to Pure Arch (The "Exit Strategy")

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

**3. Swap the Kernel and Clean up Bootloader**
Move back to the standard Arch kernel and remove the CachyOS kernel to prevent duplicate menu entries:
```bash
sudo pacman -S linux linux-headers
sudo pacman -Rs linux-cachyos linux-cachyos-headers
```
Update your Limine configuration (usually `/etc/default/limine`) to ensure your kernel parameters (like `amd_pstate=active pcie_aspm=force`) are preserved for the new kernel, then regenerate the bootloader config:
```bash
sudo limine-mkinitcpio
sudo limine-update
```
*(Note: If a CachyOS entry still appears in the boot menu, you may need to manually remove its `ENTRY` block from `/boot/limine/limine.conf` and run `limine-update` again.)*

**4. Replace Scheduler Tools**
Install the official upstream versions of the schedulers from the Arch `extra` repository:
```bash
sudo pacman -S extra/scx-scheds extra/scx-tools
```
*(If you were using `scx-manager`, it will stop receiving updates as it is CachyOS-specific, but your `/etc/scx_loader.toml` will continue to work perfectly with the upstream `scx_loader`)*

**5. Clean Up Leftovers & Branding**
List any remaining packages that are no longer in standard repositories and purge any remaining CachyOS branding:
```bash
# 1. Identify foreign packages
pacman -Qm

# 2. Purge branding and settings packages to ensure persistence
sudo pacman -Rs cachyos-hooks cachyos-settings cachyos-hello
```
Review the list from `pacman -Qm` and remove any other CachyOS-specific utilities that you no longer need.
