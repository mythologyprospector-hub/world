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

## Rule

Machine details are operational context, not project architecture.

Do not move project decisions into this file merely because they involve the local machine.
