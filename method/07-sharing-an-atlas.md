# Sharing an Atlas

**Git is how an Atlas is shared.** When several people work in the same Atlas, its own files
live in a git repo of their own; a personal Atlas can skip it. Either way the sources keep
their own git — the Atlas never folds them into its history.

## What is versioned, and what is not

- **Versioned:** the Atlas's own files — the `.md` files, every `_` folder
  (`_archived/`, `_settings/`, …), `.vscode/` and `.gitignore`.
- **Never versioned:** the symlinks — their targets are paths on one machine, so a committed
  symlink is a dangling pointer on any other — and `.claude/settings.local.json`, which holds
  those same paths.

What the Atlas *shares* about its sources is their declaration in `_settings/atlas.toml`;
where each one lives is up to each person.

## The `.gitignore` — deny everything, allow the Atlas's files

```gitignore
/*
!/*.md
!/_*/
!/.vscode/
!/.gitignore
```

Every current or future symlink is ignored automatically, with no list of sources to
maintain. `.gitignore` can't select by file type (no "ignore symlinks"), so allowing the
known set of Atlas files is the form that never needs editing when a source is added.

## Cloning a shared Atlas

Clone it anywhere, then rebuild the sources on your machine: `atlas doctor` lists what is
missing or broken, with the exact commands to get each source, and `atlas link` wires it in.
`atlas doctor` also flags any orientation block still unwritten or with placeholders; the full
list of its findings is in [03-atlas-anatomy.md](03-atlas-anatomy.md).
