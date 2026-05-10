#!/usr/bin/env python3
"""arch-fortify.py — Persistent CachyOS de-branding.

Usage:
  sudo python3 arch-fortify.py              # Apply changes
  sudo python3 arch-fortify.py -v           # Verbose (stream command output)
  sudo python3 arch-fortify.py --dry        # Preview only
  sudo python3 arch-fortify.py --restore    # Roll back latest backup
  sudo python3 arch-fortify.py --restore 20260509_182622  # Specific backup
"""

import fcntl
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

__version__ = "2.0.0"

BACKUP_DIR = Path(f"/var/lib/arch-fortify/backups/{datetime.now():%Y%m%d_%H%M%S}")
BACKUP_ROOT = Path("/var/lib/arch-fortify/backups")
LOCK_FILE = Path("/var/lib/arch-fortify/lock")

DRY_RUN = False
VERBOSE = False
HAD_ERRORS = False
ROLLBACK_STEPS = []

# ── Utilities ─────────────────────────────────────────────────────────

def info(msg):  print(f"  [INFO] {msg}")
def ok(msg):    print(f"  [OK]   {msg}")
def warn(msg):  print(f"  [WARN] {msg}")
def fail(msg):  print(f"  [FAIL] {msg}"); sys.exit(1)
def err(msg):   global HAD_ERRORS; HAD_ERRORS = True; print(f"  [ERROR] {msg}")


def acquire_lock():
    """Prevent concurrent runs."""
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_RDWR, 0o644)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (IOError, OSError):
        fail("Another instance is already running (lock held).")


def release_lock():
    LOCK_FILE.unlink(missing_ok=True)


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


def run(args, check=True, optional=False):
    """Run a command.  If *optional*, warn on missing binary instead of failing."""
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
        result = subprocess.run(args, check=check, capture_output=True, text=True)
        out = result.stdout.strip()
        if out:
            print(f"  {out}")
        return result
    except subprocess.CalledProcessError as e:
        if not VERBOSE:
            print(f"  stderr: {e.stderr.strip()}")
        if check:
            sys.exit(1)
        return e


def safe_write(path: Path, content: str, desc: str = ""):
    """Write *content* to *path*, avoiding partial writes on crash."""
    if DRY_RUN:
        info(f"Would write {path}" + (f"  ({desc})" if desc else ""))
        return
    tmp = path.with_suffix(".tmp")
    tmp.write_text(content)
    tmp.rename(path)
    ok(f"Wrote {path}" + (f"  ({desc})" if desc else ""))


# ── Backup / Restore ──────────────────────────────────────────────────

def backup_file(path: Path) -> Path | None:
    """Copy *path* into the backup directory.  Returns the backup path."""
    if not path.exists():
        return None
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    dst = BACKUP_DIR / f"{path.name}.bak"
    if DRY_RUN:
        info(f"Would backup {path} -> {dst}")
        return dst
    shutil.copy2(path, dst)
    ROLLBACK_STEPS.append(("restore", str(path), str(dst)))
    info(f"Backed up {path}")
    return dst


def restore_backup(timestamp: str | None = None):
    """Restore the most recent (or specified) backup."""
    if timestamp:
        src_dir = BACKUP_ROOT / timestamp
    else:
        snaps = sorted(BACKUP_ROOT.iterdir())
        if not snaps:
            fail("No backups found.")
        src_dir = snaps[-1]
    if not src_dir.is_dir():
        fail(f"Backup directory {src_dir} not found.")

    for bak in sorted(src_dir.glob("*.bak")):
        original_name = bak.name.removesuffix(".bak")
        dest = Path("/boot" if original_name == "limine.conf" else "/etc") / original_name
        if DRY_RUN:
            info(f"Would restore {bak} -> {dest}")
            continue
        shutil.copy2(bak, dest)
        ok(f"Restored {bak.name} -> {dest}")
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

        # Catch hooks targeting identity packages OR executing branding scripts
        targets_identity = any(t in content for t in [
            "os-release", "lsb-release", "issue", "filesystem",
        ])
        runs_branding = "Exec" in content and (
            "cachyos-branding" in content or "branding" in content.lower()
        )

        if not (targets_identity or runs_branding):
            continue

        found = True
        safe_symlink("/dev/null", str(target_dir / hook.name))

    if not found:
        ok("No CachyOS branding hooks detected.")

    # Clean up orphaned masks (hook was removed upstream)
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

    backup_file(Path("/etc/os-release"))
    backup_file(Path("/etc/lsb-release"))
    backup_file(Path("/etc/issue"))

    run(["pacman", "-S", "--noconfirm", "--needed", "filesystem", "lsb-release"])

    for name in ("os-release", "lsb-release"):
        safe_symlink(f"/usr/lib/{name}", f"/etc/{name}")

    # Restore /etc/issue (also trampled by cachyos-branding)
    etc_issue = Path("/etc/issue")
    if etc_issue.exists():
        content = etc_issue.read_text()
        # Replace any "CachyOS" remnants with the Arch default template
        cleaned = content.replace("CachyOS Linux", "\\S{PRETTY_NAME}")
        cleaned = cleaned.replace("CachyOS", "\\S{PRETTY_NAME}")
        if cleaned != content:
            safe_write(etc_issue, cleaned, desc="purged CachyOS from /etc/issue")
        else:
            ok("/etc/issue already clean")
    else:
        # Re-create from the factory default
        factory = Path("/usr/share/factory/etc/issue")
        if factory.exists():
            safe_write(etc_issue, factory.read_text(), desc="restored from factory default")

    # Same for the factory copy
    factory_issue = Path("/usr/share/factory/etc/issue")
    if factory_issue.exists():
        content = factory_issue.read_text()
        cleaned = content.replace("CachyOS Linux", "\\S{PRETTY_NAME}")
        cleaned = cleaned.replace("CachyOS", "\\S{PRETTY_NAME}")
        if cleaned != content:
            safe_write(factory_issue, cleaned, desc="purged CachyOS from factory /etc/issue")

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

    backup_file(override)
    safe_write(override, content, desc="GDM logo schema override")
    run(["glib-compile-schemas", "/usr/share/glib-2.0/schemas/"])
    ok("GDM schema override installed.")


# ── 4. Limine ────────────────────────────────────────────────────────

def _detect_indent(lines: list[str], default: int = 5) -> int:
    for ln in lines:
        if ln.strip():
            return len(ln) - len(ln.lstrip())
    return default


def clean_limine():
    print("\n── 4. Limine ──")

    conf = Path("/boot/limine.conf")
    if not conf.exists():
        info("/boot/limine.conf not found, skipping.")
        return

    backup_file(conf)
    content = conf.read_text()

    # ── Phase A: Ensure /+Arch Linux entry exists ────────────────
    if "/+Arch Linux" not in content and "/+CachyOS" in content:
        info("No /+Arch Linux entry found; /+CachyOS present. Renaming...")
        if not DRY_RUN:
            run(["limine-mkinitcpio"], optional=True)
            run(["limine-update"], optional=True)
            content = conf.read_text()
        content = content.replace("/+CachyOS", "/+Arch Linux")
        content = re.sub(r"^comment: CachyOS$", "comment: Arch Linux", content, flags=re.MULTILINE)
        if not DRY_RUN:
            safe_write(conf, content, desc="renamed /+CachyOS → /+Arch Linux")
        ok("Entry renamed to /+Arch Linux.")
    elif "/+CachyOS" in content:
        # Already has /+Arch Linux but stale CachyOS also present
        warn("Both /+CachyOS and /+Arch Linux found — stale entry will be removed.")

    lines = conf.read_text().splitlines(keepends=True)

    # ── Multi-scenario state machine ──────────────────────────────
    # Clean install:    header → /+Arch Linux → //kernels → //Snapshots → /+Windows → /EFI
    # Orphan recovery:  header → //Snapshots → /+Arch Linux → /EFI
    # Already clean:    header → /+Arch Linux → /EFI
    # Dual-boot:        ... → /+Windows → /EFI

    hs, sk, sn, ar, oe, ef = [], [], [], [], [], []
    state = "header"

    def flush_skipping():
        while hs and not hs[-1].strip():
            hs.pop()
        if hs and "comment:" in hs[-1]:
            hs.pop()
        while hs and not hs[-1].strip():
            hs.pop()

    for line in lines:
        s = line.strip()

        # ── State transitions ─────────────────────────────────────
        if s.startswith("/+Arch Linux"):
            state = "arch_linux"
        elif state == "arch_linux" and s.startswith("/+") and "/+Arch" not in s:
            state = "other"       # dual-boot entry like /+Windows
        elif s.startswith("/EFI") or s.startswith("//EFI"):
            state = "efi"
        elif s == "/+CachyOS" and state == "header":
            flush_skipping()
            state = "skip_cachyos"
            continue
        elif state in ("header", "skip_cachyos") and s.startswith("//Snapshots"):
            state = "snapshots"
        elif state == "skip_cachyos" and s.startswith("/+"):
            state = "arch_linux"

        # ── Append ────────────────────────────────────────────────
        if state == "header":
            hs.append(line)
        elif state == "skip_cachyos":
            sk.append(line)
        elif state == "snapshots":
            sn.append(line)
        elif state == "arch_linux":
            ar.append(line)
        elif state == "other":
            oe.append(line)
        elif state == "efi":
            ef.append(line)

    if DRY_RUN:
        print(f"  header:       {len(hs)} lines")
        print(f"  skip/kernels: {len(sk)} lines (stale CachyOS → removed)")
        print(f"  snapshots:    {len(sn)} lines (will be moved inside Arch Linux)")
        print(f"  arch_linux:   {len(ar)} lines")
        print(f"  other_entries:{len(oe)} lines (dual-boot etc. — preserved)")
        print(f"  efi/other:    {len(ef)} lines")

    # ── If nothing to do, still validate then return ──────────────
    if not sn and not sk:
        ok("Limine already clean, nothing to change.")
        _validate_limine(conf, lines)
        return

    # ── Re-indent orphaned snapshots for nesting under /+Arch Linux ──
    if sn:
        base_indent = _detect_indent(sn, 5)
        reindented = []
        for ln in sn:
            if ln.strip():
                cur = len(ln) - len(ln.lstrip())
                rel = cur - base_indent
                reindented.append(" " * max(0, 2 + rel) + ln.lstrip())
            else:
                reindented.append("\n")

        # Insert after the last kernel line
        insert_at = len(ar)
        for i in range(len(ar) - 1, -1, -1):
            t = ar[i].strip()
            if t.startswith("//") and not t.startswith("//+"):
                insert_at = i + 1
                break
        while insert_at < len(ar) and not ar[-1].strip():
            ar.pop()

        ar = ar[:insert_at] + ["\n"] + reindented + ["\n"] + ar[insert_at:]

    # ── Compose output ────────────────────────────────────────────
    out_lines = hs + ["\n"] + ar + oe + ef

    if DRY_RUN:
        info("Would write updated /boot/limine.conf")
        print(f"    Lines before: {len(lines)}  after: {len(out_lines)}")
        return

    safe_write(conf, "".join(out_lines), desc="limine.conf (scrubbed)")

    # ── Update default_entry ──────────────────────────────────────
    entry_num = 0
    arch_no = None
    for ln in out_lines:
        if ln.strip().startswith("/+"):
            entry_num += 1
            if "/+Arch Linux" in ln:
                arch_no = entry_num

    if arch_no is not None:
        cur = conf.read_text()
        newc = re.sub(r"^default_entry:\s*\d+.*", f"default_entry: {arch_no}", cur, flags=re.MULTILINE)
        if newc != cur:
            safe_write(conf, newc, desc="default_entry -> Arch Linux")
        else:
            ok("default_entry already points to Arch Linux.")
    """ else: warn, don't fail — dual-boot user may have set it deliberately """
    if arch_no is None:
        warn("Could not determine Arch Linux entry number — default_entry left as-is.")

    # ── Validate ──────────────────────────────────────────────────
    _validate_limine(conf, out_lines)

    # ── Regenerate ────────────────────────────────────────────────
    run(["limine-mkinitcpio"], optional=True)
    run(["limine-update"], optional=True)
    ok("Boot menu regenerated.")


def _validate_limine(conf: Path, final_lines: list[str] | None = None):
    """Non-fatal sanity checks on the written limine.conf."""
    if not conf.exists():
        err("limine.conf missing after write!")
        return
    content = conf.read_text()

    if "/+Arch Linux" not in content:
        warn("  LIMINE: /+Arch Linux entry not found — is this a pre-identity-restore run?")
    elif "/+CachyOS" in content:
        warn("  LIMINE: stale /+CachyOS entry still present.")

    m = re.search(r"^default_entry:\s*(\d+)", content, re.MULTILINE)
    if not m:
        warn("  LIMINE: default_entry not found — using Limine's internal default.")
    elif final_lines:
        entry_list = [ln for ln in final_lines if ln.strip().startswith("/+")]
        entry_count = len(entry_list)
        entry_no = int(m.group(1))
        if entry_no > entry_count and entry_count > 0:
            warn(f"  LIMINE: default_entry ({entry_no}) > entry count ({entry_count}) — likely dual-boot.")
        elif entry_no <= entry_count and entry_count > 0:
            ok(f"  LIMINE: default_entry = {entry_no} (valid among {entry_count} entries).")


# ── 5. Plymouth ──────────────────────────────────────────────────────

def restore_plymouth():
    print("\n── 5. Plymouth ──")
    if not shutil.which("plymouth-set-default-theme"):
        info("plymouth not installed, skipping.")
        return

    # Check current theme via the official tool (more reliable than grepping config)
    try:
        out = subprocess.run(
            ["plymouth-set-default-theme"],
            capture_output=True, text=True, check=False,
        ).stdout.strip()
    except Exception:
        out = ""

    if out == "bgrt":
        ok("Plymouth already set to bgrt.")
        return

    if DRY_RUN:
        info("Would run: plymouth-set-default-theme bgrt && mkinitcpio -P")
        return

    backup_file(Path("/etc/plymouth/plymouthd.conf"))
    run(["plymouth-set-default-theme", "bgrt"])
    run(["mkinitcpio", "-P"])
    ok("Plymouth theme reset to bgrt.")


# ── 6. Verify ────────────────────────────────────────────────────────

def verify():
    print("\n── 6. Verification ──")
    if DRY_RUN:
        info("Dry run — no changes applied.")
        return

    # OS identity
    for line in Path("/etc/os-release").read_text().splitlines():
        if line.startswith(("NAME=", "PRETTY_NAME=")):
            print(f"  {line}")

    # Hook masks
    hook_dir = Path("/etc/libalpm/hooks/")
    masked = sorted(hook_dir.glob("*.hook")) if hook_dir.exists() else []
    if masked:
        for m in masked:
            if m.is_symlink() and m.readlink() == Path("/dev/null"):
                print(f"  HOOK: {m.name} → masked")
    else:
        print("  HOOK: none masked (all clean, no branding hooks found)")

    # Limine
    conf = Path("/boot/limine.conf")
    if conf.exists():
        content = conf.read_text()
        if "/+CachyOS" in content:
            warn("  LIMINE: stale /+CachyOS entry still present!")
        else:
            ok("  LIMINE: no stale CachyOS entries.")
        if "//Snapshots" in content:
            ok("  LIMINE: snapshots section present.")

    # Scan /etc/ for any remaining "CachyOS" strings in UI-relevant files
    ui_files = [
        "/etc/os-release",
        "/etc/lsb-release",
        "/etc/issue",
    ]
    cachyos_found = False
    for f in ui_files:
        p = Path(f)
        if p.exists() and "CachyOS" in p.read_text():
            warn(f"  REMAINING: 'CachyOS' found in {f}")
            cachyos_found = True
    if not cachyos_found:
        ok("  No CachyOS branding found in identity files.")

    # Report any accumulated errors
    if HAD_ERRORS:
        warn("Some steps had errors — review the output above.")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    global DRY_RUN, VERBOSE

    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"arch-fortify.py v{__version__}")
        return 0

    if "--restore" in sys.argv:
        ts = None
        for i, a in enumerate(sys.argv):
            if a == "--restore" and i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("-"):
                ts = sys.argv[i + 1]
        restore_backup(ts)
        return 0 if not HAD_ERRORS else 1

    if "--dry" in sys.argv or "--dry-run" in sys.argv or "-n" in sys.argv:
        DRY_RUN = True
        print("═══ DRY RUN — no changes will be written ═══\n")

    if "-v" in sys.argv or "--verbose" in sys.argv:
        VERBOSE = True

    if os.geteuid() != 0:
        fail("Must run as root (sudo).")

    acquire_lock()
    try:
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
    finally:
        release_lock()

    return 1 if HAD_ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
