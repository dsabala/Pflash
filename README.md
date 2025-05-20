# Pflash
Pflash is a simple yet powerful command-line tool you can use to flash devices
based on the Phoenix RTOS system.

Unlike low-level tools that work underneath, it doesn't require you
to closely monitor the flashing process. It automatically gathers information
from project files like `nvm.yaml` and the configuration file `~/.config/pflash/config.json`.

If something goes wrong, Pflash tries to exit gracefully with an informative error message.
It also has a dry-run mode that prints out the raw shell commands you can run yourself.

[![asciicast](https://asciinema.org/a/720195.svg)](https://asciinema.org/a/720195)

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

## TODO
- my Python skills are not very advanced, so I focused on isolating abstractions and making this tool attractive to use and co-create,
  there are certainly some Pythonic improvements to be made
- fix the function that enters the target into PLO if it discovers that the target is in the system (its buggy, I dont use it often)
- add flash-via-PLO (using 2 serial connections)
- consider adding flash-via-ethernet or other functionalities like for example flash-single-program functionality in the future
- add a changelog and version information to the program
- distribute the program with Pip
