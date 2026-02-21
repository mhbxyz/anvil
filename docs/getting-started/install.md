# Install PyQuick CLI

[Project README](../../README.md) · [Docs Index](../README.md) · [Getting Started](README.md)

Goal: install `pyqck` and verify `pyqck --help` works in your shell.

## Choose an install mode

- **Global CLI (`pipx`)**: best for running `pyqck` from anywhere in your shell `PATH`
- **Project-local (`venv` + `pip`)**: best when each repository should pin its own tool version
- **Experimental Linux binary**: best for trying a direct standalone executable from GitHub Releases

## Option A) Global install with `pipx`

Use this when you want one shared `pyqck` command across projects.

### Prerequisites

- Python 3.12+
- `pipx` installed

### Install

```bash
pipx install pyqck
```

### Verify

```bash
pyqck --help
```

Expected result:

- help output prints successfully
- `pyqck` is available directly from your shell

## Option B) Project-local install with `venv` and `pip`

Use this when you want a per-project CLI installation.

### Prerequisites

- Python 3.12+

### Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install

```bash
pip install pyqck
```

### Verify

```bash
pyqck --help
```

Expected result:

- help output prints successfully
- `pyqck` resolves from active virtual environment

## Option C) Experimental Linux binary from GitHub Releases

Use this when you want to try the standalone Linux executable build.

### Prerequisites

- Linux x86_64
- `uv` installed for project environment commands such as `pyqck install` and `pyqck test`

### Download and verify

1. Open the latest release page and download these assets:
   - `pyqck-<version>-linux-x86_64-experimental`
   - `pyqck-<version>-linux-x86_64-experimental.sha256`
2. verify checksum:

```bash
sha256sum -c pyqck-<version>-linux-x86_64-experimental.sha256
```

### Run

```bash
chmod +x pyqck-<version>-linux-x86_64-experimental
./pyqck-<version>-linux-x86_64-experimental --help
```

Expected result:

- help output prints successfully
- no Python installation is required to launch the CLI itself

Note: binary distribution is experimental in alpha; `pipx` remains the primary supported install mode.

## Upgrade

Global (`pipx`):

```bash
pipx upgrade pyqck
```

Project-local (`venv`):

```bash
pip install --upgrade pyqck
```

## Uninstall

Global (`pipx`):

```bash
pipx uninstall pyqck
```

Project-local (`venv`):

```bash
pip uninstall pyqck
```

## Troubleshooting

### `pyqck: command not found`

Common causes:

- `pipx` binary path is not exported in your shell
- venv is not activated for project-local usage

Fix:

1. run `pipx ensurepath`
2. restart your shell session
3. for local installs, run `source .venv/bin/activate`
4. retry `pyqck --help`

### Wrong Python version

Symptom:

- install or runtime errors mentioning unsupported Python

Fix:

1. run `python --version`
2. use Python 3.12+
3. reinstall after switching interpreter

### Installed but command still unavailable

Fix:

1. confirm install state (`pipx list` or `pip show pyqck` in active venv)
2. verify your active shell and environment activation
3. rerun verification: `pyqck --help`

## Next step

After install succeeds, continue with [Alpha quickstart](quickstart-alpha.md).
