# mdadm-fix

Patch for **mdadm-4.4** to gracefully handle missing sysfs module parameters on older kernels.

## Problem

On kernels that pre-date the `legacy_async_del_gendisk` sysfs parameter (e.g. RHEL 9.6 / `5.14.0-570.32.1.el9_6`), `mdadm-4.4` aborts array assembly with:

```
mdadm: Can't open /sys/module/md_mod/parameters/legacy_async_del_gendisk
```

The `legacy_async_del_gendisk` knob was introduced in kernel 5.18 as a backward-compatibility toggle. Kernels that shipped before that commit simply don't have it in sysfs — but `mdadm-4.4` assumes it must be present and hard-fails.

## Copr — quickest fix

A pre-built RPM is available for **RHEL 9 / CentOS Stream 9 / EL9**:

```bash
sudo dnf copr enable sisyphuscode/mdadm-fix
sudo dnf update mdadm
```

To verify the installed version:
```bash
rpm -q mdadm
# Expected: mdadm-4.4-4.1.sisyphuscode.el9
```

To revert to the stock distro package at any time:
```bash
sudo dnf copr disable sisyphuscode/mdadm-fix
sudo dnf distro-sync mdadm
```

**Copr project:** https://copr.fedorainfracloud.org/coprs/sisyphuscode/mdadm-fix/

## Applying the patch manually

```sh
# Against the mdadm source tree
git apply 0044-mdadm-skip-missing-legacy_async-del-gendisk.patch

# Or via patch(1) in an RPM build directory
patch -p1 < 0044-mdadm-skip-missing-legacy_async-del-gendisk.patch
```

## What the fix does

**`0044-mdadm-skip-missing-legacy_async-del-gendisk.patch`**

Instead of a racy `access(F_OK)` pre-check (which introduces a TOCTOU window and conflates `ENOENT` with `EACCES`), the patch inspects `errno` directly after `open(2)` fails:

| `errno` | Meaning | Action |
|---|---|---|
| `ENOENT` | Parameter doesn't exist on this kernel | Return `true` silently — the old behaviour is in effect by definition |
| Anything else | Real error (permissions, I/O, ...) | Log `path: strerror(errno)` and return `false` |

The `write(2)` failure path is also improved to emit `strerror(errno)` (or `"short write"` on a partial write) instead of a bare path string.

## Affected versions

- **mdadm**: 4.4 (el9_7 build)
- **Kernel**: any release before 5.18 that lacks `legacy_async_del_gendisk`
