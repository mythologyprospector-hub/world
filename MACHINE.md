# Machine

## Local development layout

The standard local clone location for every project repository is:

```
~/projects/<repo-name>
```

Examples:

```
~/projects/renaissance
~/projects/episteme
~/projects/organs
```

**Rule:** When working with a project repository locally, assume its Git clone is under `~/projects/<repo-name>` unless the machine's repository state explicitly shows otherwise.

This is the standard clone location for the user's project repositories. Do not substitute `~/<repo-name>`.

## Organs installation

Organs is installed at:

```
/srv/organs
```

This is the runtime/install location, not the normal Git clone location.

## Development host

The primary development machine is known as **Bucky**.

Do not infer additional filesystem paths from this document. If a path matters and is not explicitly documented here, inspect the machine or repository state before using it.

## Git working routine

The user is still learning Linux and Git and does **not** reliably remember the routine commands `git switch` and `git pull`. This is expected and should not be treated as user error.

When the user is told to update a local project checkout before continuing work, provide the complete routine rather than assuming they remember the individual Git commands.

For a normal project checkout, the routine is:

```bash
cd ~/projects/<repo-name>
git switch main
git pull --ff-only origin main
```

For example, for Episteme:

```bash
cd ~/projects/episteme
git switch main
git pull --ff-only origin main
```

When giving the user a local Git command sequence, prefer giving the whole copy/paste block. Do not rely on the user remembering that `git pull` updates the checkout or that `git switch main` gets them back onto the main branch.

If a repository is intentionally being worked on from a feature branch, give the exact branch-switch command needed instead of the generic main routine.

## Rule

Machine details are operational context, not project architecture.

Do not move project decisions into this file merely because they involve the local machine.
