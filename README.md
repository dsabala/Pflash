# Pflash
Pflash is a simple yet powerful command-line tool you can use to flash devices
based on the Phoenix RTOS system.

Unlike low-level tools that work underneath, it doesn't require you
to closely monitor the flashing process. It automatically gathers information
from project files like `nvm.yaml` and the configuration file `~/.config/pflash/config.json`.

If something goes wrong, Pflash tries to exit gracefully with an informative error message.
It also has a dry-run mode that prints out the raw shell commands you can run yourself.

## Quickstart

### Manual installation from the repository
```bash
# Clone repository
git clone https://github.com/dsabala/pflash.git
cd pflash
# Install package with pipx
pipx install .
# Verify the installation and explore help message
pflash --help
pflash flash-via-ramdisk --help
```

## Development
Run `poetry install` to install all dependencies, including development dependencies,
this will create an isolated virtual environment for the project.
Run pflash with `poetry run pflash`, format code with `poetry run black .`, run linter with `poetry run pylint .`.
