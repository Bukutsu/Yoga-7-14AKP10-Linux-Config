#!/usr/bin/env python3
"""arch-fortify.py — Persistent CachyOS de-branding.

Usage:
  sudo python3 arch-fortify.py          # Apply changes
  sudo python3 arch-fortify.py --dry    # Preview only
  sudo python3 arch-fortify.py --restore  # Roll back latest backup
"""

import os, re, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path(f"/var/lib/arch-fortify/backups/{datetime.now():%Y%m%d_%H%M%S}")
BACKUP_ROOT = Path("/var/lib/arch-fortify/backups")

DRY_RUN = False
VERBOSE = False

# ── Utilities ─────────────────────────────────────────────────────────

def info(msg):  print(f"  [INFO] {msg}")
def ok(msg):    print(f"  [OK]   {msg}")
def warn(msg):  print(f"  [WARN] {msg}")
def fail(msg):  print(f"  [FAIL] {msg}"); sys.exit(1)


def safe_symlink(target: str, link: str):
    link_p = Path(link)
    target_p = Path(target)
    if link_p.is_symlink() and link_p.readlink() == target_p:
        ok(f"Symlink {link} already correct")
        return
    if DRY_RUN:
        info(f"Would symlink {link} -> {target}")
        return
    link_p.unlink(missing_ok=True)
    link_p.symlink_to(target_p)
    ok(f"Symlinked {link} -> {target}")


def run(args, check=True, optional=False, input_data=None):
    """Run a command. If optional, warn and return None on missing binary."""
    binary = args[0]
    if not shutil.which(binary):
        msg = f"Binary '{binary}' not found, skipping."
        if optional:
            warn(msg)
            return None
        fail(msg)
    if DRY_RUN:
        info(f"Would run: {' '.join(args)}")
        return None
    try:
        if VERBOSE:
            info(f"Running: {' '.join(args)}")
            return subprocess.run(args, check=check)
        result = subprocess.run(args, check=check, capture_output=True, text=True, input=input_data)
        if result.stdout.strip():
            print(f"  {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        if not VERBOSE:
            print(f"  stderr: {e.stderr.strip()}")
        if check:
            sys.exit(1)
        return e


def restore_backup(timestamp: str | None = None):
    """Restore the most recent (or specified) backup of limine.conf."""
    if timestamp:
        src_dir = BACKUP_ROOT / timestamp
    else:
        snaps = sorted(BACKUP_ROOT.iterdir())
        if not snaps:
            fail("No backups found.")
        src_dir = snaps[-1]

    bak = src_dir / "limine.conf.bak"
    if not bak.exists():
        fail(f"No backup found at {bak}")

    if DRY_RUN:
        info(f"Would restore {bak} -> /boot/limine.conf")
        return

    shutil.copy2(bak, "/boot/limine.conf")
    ok(f"Restored {bak} -> /boot/limine.conf")

    # Also restore os-release if backup exists
    os_bak = src_dir / "os-release.bak"
    if os_bak.exists():
        shutil.copy2(os_bak, "/etc/os-release")
        ok(f"Restored {os_bak} -> /etc/os-release")

    run(["limine-update"], optional=True)


# ── 1. Identity Guard ─────────────────────────────────────────────────

def mask_branding_hooks():
    print("\n── 1. Identity Guard ──")
    hook_dir = Path("/usr/share/libalpm/hooks/")
    target_dir = Path("/etc/libalpm/hooks/")

    if not hook_dir.is_dir():
        info("No hooks directory, skipping.")
        return

    target_dir.mkdir(parents=True, exist_ok=True)
    found = False

    for hook in sorted(hook_dir.glob("*.hook")):
        content = hook.read_text()
        if "cachyos" not in content:
            continue
        targets = ["os-release", "lsb-release", "issue", "filesystem"]
        if not any(t in content for t in targets):
            continue
        found = True
        safe_symlink("/dev/null", str(target_dir / hook.name))

    if not found:
        ok("No CachyOS branding hooks detected.")

    # Clean up orphaned masks for hooks that no longer exist
    for mask in sorted(target_dir.glob("*.hook")):
        if not (hook_dir / mask.name).exists():
            if DRY_RUN:
                info(f"Would remove orphaned mask: {mask}")
            else:
                mask.unlink()
                ok(f"Removed orphaned mask: {mask.name}")


# ── 2. Identity Restoration ──────────────────────────────────────────

def restore_identity():
    print("\n── 2. Identity Restoration ──")

    # Backup current os-release
    os_rel = Path("/etc/os-release")
    if os_rel.exists():
        bak_root = BACKUP_DIR if not DRY_RUN else BACKUP_ROOT / "preview"
        bak_root.mkdir(parents=True, exist_ok=True)
        if not DRY_RUN:
            shutil.copy2(os_rel, bak_root / "os-release.bak")

    run(["pacman", "-S", "--noconfirm", "--needed", "filesystem", "lsb-release"])

    for name in ("os-release", "lsb-release"):
        safe_symlink(f"/usr/lib/{name}", f"/etc/{name}")

    # Verify
    if not DRY_RUN:
        for line in Path("/etc/os-release").read_text().splitlines():
            if line.startswith("NAME="):
                ok(f"/etc/os-release says: {line}")


# ── 3. GDM Logo ──────────────────────────────────────────────────────

def hide_gdm_logo():
    print("\n── 3. GDM Logo ──")

    if not shutil.which("glib-compile-schemas"):
        warn("glib-compile-schemas not found, skipping GDM step.")
        return

    override = Path("/usr/share/glib-2.0/schemas/zzzz_arch-fix.gschema.override")
    content = "[org.gnome.login-screen]\nlogo=''\n"

    if override.exists() and override.read_text() == content:
        ok("GDM schema override already correct.")
        return

    if DRY_RUN:
        info(f"Would write {override}")
        info("Would run: glib-compile-schemas /usr/share/glib-2.0/schemas/")
        return

    override.write_text(content)
    run(["glib-compile-schemas", "/usr/share/glib-2.0/schemas/"])
    ok("GDM schema override installed.")


# ── 4. Limine ────────────────────────────────────────────────────────

def clean_limine():
    print("\n── 4. Limine ──")

    conf = Path("/boot/limine.conf")
    if not conf.exists():
        info("/boot/limine.conf not found, skipping.")
        return

    if not DRY_RUN:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(conf, BACKUP_DIR / "limine.conf.bak")
        info(f"Backed up to {BACKUP_DIR / 'limine.conf.bak'}")

    lines = conf.read_text().splitlines(keepends=True)

    # ── Multi-scenario state machine ──────────────────────────────
    # header → /+CachyOS → skip → //Snapshots → /+Arch Linux → /EFI
    # header → //Snapshots (orphaned) → /+Arch Linux → /EFI
    # header → /+Arch Linux → /EFI  (already clean — no-op)
    # header only (no entries at all — no-op)

    hs, sk, sn, ar, ef = [], [], [], [], []
    state = "header"

    def flush_skipping():
        """Trim trailing blanks/comments from header before skipping."""
        while hs and not hs[-1].strip():
            hs.pop()
        if hs and "comment:" in hs[-1]:
            hs.pop()
        while hs and not hs[-1].strip():
            hs.pop()

    for idx, line in enumerate(lines):
        s = line.strip()

        # ── State transitions (highest priority first) ────────────
        if s.startswith("/+Arch Linux"):
            state = "arch_linux"

        elif s.startswith("/EFI") or s.startswith("//EFI"):
            state = "efi"

        elif s == "/+CachyOS" and state in ("header",):
            flush_skipping()
            state = "skip_cachyos"
            continue

        elif state == "header" and s.startswith("//Snapshots"):
            state = "snapshots"   # orphan recovery

        elif state == "skip_cachyos" and s.startswith("//Snapshots"):
            state = "snapshots"

        elif state == "skip_cachyos" and s.startswith("/+"):
            state = "arch_linux"
            # fall through to append

        # ── Append to current section ─────────────────────────────
        if state == "header":
            hs.append(line)
        elif state == "skip_cachyos":
            sk.append(line)
        elif state == "snapshots":
            sn.append(line)
        elif state == "arch_linux":
            ar.append(line)
        elif state == "efi":
            ef.append(line)

    # ── Diagnostics ───────────────────────────────────────────────
    if DRY_RUN:
        print(f"  header:       {len(hs)} lines")
        print(f"  skip/kernels: {len(sk)} lines (will be removed)")
        print(f"  snapshots:    {len(sn)} lines (will be moved inside Arch Linux)")
        print(f"  arch_linux:   {len(ar)} lines")
        print(f"  efi/other:    {len(ef)} lines")

    # Nothing to do if no snapshots and no CachyOS entry
    if not sn and not sk:
        ok("Limine already clean, nothing to change.")
        return

    # ── Re-indent snapshots for nesting under /+Arch Linux ─────────
    base = 5
    for ln in sn:
        if ln.strip():
            base = len(ln) - len(ln.lstrip())
            break

    reindented = []
    for ln in sn:
        if ln.strip():
            cur_indent = len(ln) - len(ln.lstrip())
            rel = cur_indent - base
            reindented.append(" " * max(0, 2 + rel) + ln.lstrip())
        else:
            reindented.append("\n")

    # ── Insert snapshots inside Arch Linux entry ──────────────────
    # Place after the last kernel line (starts with "//") before trailing blanks
    insert_at = len(ar)
    for i in range(len(ar) - 1, -1, -1):
        t = ar[i].strip()
        if t.startswith("//") and not t.startswith("//+"):
            insert_at = i + 1
            break

    # Trim trailing blank lines from the Arch section tail
    while insert_at < len(ar) and not ar[-1].strip():
        ar.pop()

    before = ar[:insert_at]
    after = ar[insert_at:]

    arch_with = before + ["\n"] + reindented + ["\n"] + after

    # ── Compose output ────────────────────────────────────────────
    out = hs + ["\n"] + arch_with + ef

    if DRY_RUN:
        info("Would write updated /boot/limine.conf")
        print("  Preview of structural changes:")
        print(f"    Lines before: {len(lines)}")
        print(f"    Lines after:  {len(out)}")
        # Show diff-like summary
        removed = len(lines) - len(out)
        print(f"    Lines removed: {removed} (stale CachyOS kernel entries)")
        return

    conf.write_text("".join(out))
    ok("CachyOS entry removed, snapshots moved under /+Arch Linux.")

    # ── Update default_entry ──────────────────────────────────────
    entry_num = 0
    arch_no = None
    for ln in out:
        if ln.strip().startswith("/+"):
            entry_num += 1
            if ln.strip() == "/+Arch Linux":
                arch_no = entry_num

    if arch_no is not None:
        content = conf.read_text()
        content = re.sub(r"^default_entry:\s*\d+.*", f"default_entry: {arch_no}", content, flags=re.MULTILINE)
        conf.write_text(content)
        ok(f"default_entry set to {arch_no} (Arch Linux).")

    # ── Regenerate ────────────────────────────────────────────────
    run(["limine-mkinitcpio"], optional=True)
    run(["limine-update"], optional=True)
    ok("Boot menu regenerated.")


# ── 5. Plymouth ──────────────────────────────────────────────────────

def restore_plymouth():
    print("\n── 5. Plymouth ──")
    if not shutil.which("plymouth-set-default-theme"):
        info("plymouth not installed, skipping.")
        return
    # Check current theme
    theme_conf = Path("/etc/plymouth/plymouthd.conf")
    if theme_conf.exists():
        for line in theme_conf.read_text().splitlines():
            if line.strip() == "Theme=bgrt":
                ok("Plymouth already set to bgrt.")
                return

    run(["plymouth-set-default-theme", "bgrt"])
    run(["mkinitcpio", "-P"])
    ok("Plymouth theme reset to bgrt.")


# ── 6. Verify ────────────────────────────────────────────────────────

def verify():
    print("\n── 6. Verification ──")
    if DRY_RUN:
        info("Dry run — no changes applied. Run without --dry to apply.")
        return

    print(f"  NAME=$(grep ^NAME= /etc/os-release | cut -d= -f2)")
    for line in Path("/etc/os-release").read_text().splitlines():
        if line.startswith(("NAME=", "PRETTY_NAME=")):
            print(f"  {line}")

    # Check hook masks
    hook_dir = Path("/etc/libalpm/hooks/")
    masked = sorted(hook_dir.glob("*.hook")) if hook_dir.exists() else []
    if masked:
        for m in masked:
            if m.is_symlink() and m.readlink() == Path("/dev/null"):
                print(f"  HOOK: {m.name} → masked")
    else:
        print("  HOOK: none masked (all clean)")

    # Check Limine
    conf = Path("/boot/limine.conf")
    if conf.exists():
        content = conf.read_text()
        if "/+CachyOS" in content:
            warn("  LIMINE: stale /+CachyOS entry still present!")
        else:
            ok("LIMINE: no stale CachyOS entries.")
        if "//Snapshots" in content:
            ok("LIMINE: snapshots section present.")
    else:
        warn("LIMINE: /boot/limine.conf not found.")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    global DRY_RUN, VERBOSE

    if "--restore" in sys.argv:
        ts = None
        for i, a in enumerate(sys.argv):
            if a == "--restore" and i + 1 < len(sys.argv) and not sys.argv[i+1].startswith("-"):
                ts = sys.argv[i+1]
        restore_backup(ts)
        return

    if "--dry" in sys.argv or "--dry-run" in sys.argv or "-n" in sys.argv:
        DRY_RUN = True
        print("═══ DRY RUN — no changes will be written ═══\n")

    if "-v" in sys.argv or "--verbose" in sys.argv:
        VERBOSE = True

    if os.geteuid() != 0:
        fail("Must run as root (sudo).")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    mask_branding_hooks()
    restore_identity()
    hide_gdm_logo()
    clean_limine()
    restore_plymouth()
    verify()

    print()
    if DRY_RUN:
        print("═══ Dry run complete. Run without --dry to apply. ═══")
    else:
        ok("De-branding complete. Your system is now persistently Arch Linux.")
        warn("A reboot is recommended to see all changes take effect.")


if __name__ == "__main__":
    main()
