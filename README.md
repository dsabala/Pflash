# Pflash
Pflash is the unofficial Phoenix RTOS flash utility.

## Installation

### 1. Manual Installation from the Repository with `pipx`
To install Pflash directly from the repository:

1. Clone the repository:
```bash
git clone https://github.com/dsabala/pflash.git
cd pflash
```

2. Install the application using `pipx`:
```bash
pipx install .
```

3. Verify the installation:
```bash
pflash --help
```

## Usage

To see the available commands and options, run:
```bash
pflash --help
pflash flash-via-ramdisk --help
```

Example usage:
```bash
pflash -v flash-via-ramdisk -p aarch64a53-zynqmp-som -c /dev/ttyUSB0 plo kernel
```
