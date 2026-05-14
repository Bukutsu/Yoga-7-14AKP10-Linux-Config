# Biopass PAM Configuration (Arch + GNOME)

**Date:** 2026-05-14  
**System:** Arch Linux + GNOME  
**Status:** Working

## Problem

Following the official [biopass PAM setup guide](https://github.com/TickLabVN/biopass/blob/main/docs/PAM.md), the recommended configuration for `/etc/pam.d/system-auth` was:

```pam
auth    [success=2 default=ignore]      libbiopass_pam.so
auth    [success=1 default=ignore]      pam_unix.so nullok
auth    requisite                       pam_deny.so
```

**Symptom:** Biopass succeeds (camera light on, "Face authentication succeeded" in logs), but PAM still prompts for password instead of skipping to desktop.

## Root Cause

The control flag `[success=2 default=ignore]` is **distro-specific** and unreliable on Arch (as well as Fedora-family systems). The syntax doesn't reliably skip the correct number of modules across different PAM implementations.

## Solution

Replace the control flag with `sufficient`, which is a **portable POSIX-standard PAM control flag**:

```pam
auth    sufficient                      libbiopass_pam.so
auth    required                        pam_unix.so          nullok
auth    requisite                       pam_deny.so
```

### How it works:
- **biopass succeeds** → `sufficient` returns success immediately, skips remaining auth modules
- **biopass fails** → PAM falls through to `pam_unix.so` (password fallback)
- **password succeeds** → auth succeeds
- **password fails** → `pam_deny.so` denies access

## Complete Working Config

Full `/etc/pam.d/system-auth` for Arch + GNOME:

```pam
#%PAM-1.0

auth       required                    pam_faillock.so      preauth
-auth      [success=1 default=ignore]  pam_systemd_home.so

# Biopass (biometric authentication)
auth       sufficient                  libbiopass_pam.so
auth       required                    pam_unix.so          nullok
auth       requisite                   pam_deny.so

auth       optional                    pam_permit.so
auth       required                    pam_env.so
auth       required                    pam_faillock.so      authsucc

-account   [success=1 default=ignore]  pam_systemd_home.so
account    required                    pam_unix.so
account    optional                    pam_permit.so
account    required                    pam_time.so

-password  [success=1 default=ignore]  pam_systemd_home.so
password   required                    pam_unix.so          try_first_pass nullok shadow
password   optional                    pam_permit.so

-session   optional                    pam_systemd_home.so
session    required                    pam_limits.so
session    required                    pam_unix.so
session    optional                    pam_permit.so
```

## Installation (Arch Linux via AUR)

### 1. Install biopass from AUR

Use your AUR helper (e.g., `yay`, `paru`):

```bash
yay -S biopass
# or
paru -S biopass
```

Alternatively, manual AUR build:

```bash
git clone https://aur.archlinux.org/biopass.git
cd biopass
makepkg -si
```

### 2. Verify installation

```bash
ls -la /lib*/security/libbiopass_pam.so
```

Should output something like:
```
-rw-r--r-- 1 root root 12345 May 14 12:00 /usr/lib/security/libbiopass_pam.so
```

### 3. Enable biopass daemon

```bash
sudo systemctl enable --now biopass
sudo systemctl status biopass
```

Check that the service is running:
```bash
journal -u biopass -n 5
```

## PAM Configuration

### 1. Backup existing config

If you previously had fingerprint PAM setup (e.g., `pam_fprintd.so`), back it up first:

```bash
sudo cp /etc/pam.d/system-auth /etc/pam.d/system-auth.backup.$(date +%s)
```

### 2. Remove previous biometric PAM setup (if any)

If you were using fingerprint auth (e.g., `pam_fprintd.so`), remove it first:

```bash
# Check for fingerprint module
grep -n fprintd /etc/pam.d/system-auth

# If present, edit the file and remove the line
sudo nano /etc/pam.d/system-auth
# Then remove or comment out any line containing pam_fprintd.so
```

### 3. Keep root shell open as recovery

```bash
sudo -s
```

### 4. Apply PAM configuration (in another terminal)

Edit `/etc/pam.d/system-auth` to match the working config from above (replace the entire auth stack).

Or use `sudo nano /etc/pam.d/system-auth` and make these changes:
- Change `auth    [success=2 default=ignore]      libbiopass_pam.so` to `auth    sufficient                      libbiopass_pam.so`
- Replace `auth    [success=1 default=ignore]      pam_unix.so nullok` with `auth    required                        pam_unix.so          nullok`

### 5. Test authentication

```bash
sudo -k
sudo true
```

Should **not** prompt for password if biopass succeeds, or prompt for password as fallback if biopass fails.

### 6. Test GDM logout/login

Logout to GDM, attempt biopass unlock. Should skip password prompt on success.

## Verification & Testing

### Check biopass daemon logs

Confirm biopass is running and being called:
```bash
journalctl -u biopass -f
# or
sudo systemctl status biopass -l
```

You should see:
```
[debug] AuthManager: Trying Face authentication
[debug] FaceAuth: Anti-spoofing started
[debug] FaceAuth: AI anti-spoofing check passed
[debug] AuthManager: Face authentication succeeded
```

### Test sudo authentication

```bash
sudo -k          # Invalidate sudo session
sudo true        # Attempt auth (should use biopass, not password)
```

### Test GDM/desktop unlock

1. Lock your screen: `Super + L` or via GNOME Settings
2. On unlock screen, face the camera
3. Camera light should turn on, biopass runs silently
4. Desktop should unlock without password prompt
5. Fallback: If biopass fails, password prompt appears

## Known Issues

### Line 2: `[success=1 default=ignore]` on `pam_unix.so`

The backup password fallback line also uses `[success=n default=ignore]`, which technically works but is less portable. For consistency, it can be replaced with `required`, but testing is recommended before deploying widely.

### Biopass module not found

If biopass still prompts for password even with `sufficient`:

```bash
ls -la /lib*/security/libbiopass_pam.so
```

If not found, install/reinstall biopass first.

### Biopass daemon not running

```bash
systemctl status biopass
ps aux | grep biopass
```

## Reporting to Upstream

The official biopass PAM docs recommend `[success=2 default=ignore]` as the default but only mention Fedora-family systems as problematic. This should be reported:

- **Issue title:** `PAM control flag [success=2 default=ignore] fails on Arch; recommend sufficient as portable default`
- **Details:** Arch + GNOME with the documented config fails; `sufficient` works reliably
- **Suggestion:** Either recommend `sufficient` as universal default (most portable), or add Arch to the list of distros requiring the workaround

**Repository:** https://github.com/TickLabVN/biopass

## References

- [Biopass PAM Setup Guide](https://github.com/TickLabVN/biopass/blob/main/docs/PAM.md)
- PAM control flags: `sufficient` is POSIX-standard and portable across Linux distros
- Tested 2026-05-14 on Arch Linux + GNOME + biopass

