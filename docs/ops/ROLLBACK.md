# Zor-El Rollback Guide

This guide restores the known-good frozen baseline quickly.

## Frozen baseline references

- Tag: `zorel-polish-freeze-20260228T020935Z`
- Branch: `freeze/zorel-polish-20260228T020935Z`

## One-command local rollback (hard reset to freeze tag)

```bash
git fetch origin --tags
git checkout main
git reset --hard zorel-polish-freeze-20260228T020935Z
```

## Restore from freeze branch (non-destructive)

```bash
git fetch origin
git checkout -B restore/zorel-polish-freeze origin/freeze/zorel-polish-20260228T020935Z
```

## Re-apply freeze state to GitHub main (explicit operator action)

```bash
git checkout main
git reset --hard zorel-polish-freeze-20260228T020935Z
git push origin main --force-with-lease
```

Use the final command only when a rollback to public `main` is intentionally approved.

