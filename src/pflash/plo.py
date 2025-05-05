"""
Plo bootloader management module
"""

import serial
import time
from loguru import logger


def boot_plo_naively(port: str, baud: int, dry: bool, total_timeout: int = 10):
    """Make sure target is stopped in plo bootloader"""

    if dry:
        logger.info("Dry run, skip driving target into plo...")
        return

    logger.info("Checking if target is locked in bootloader...")
    start = time.time()
    try:
        with serial.Serial(port, baudrate=baud, timeout=0.5) as ser:
            ser.reset_input_buffer()
            ser.write(b"\n")
            found_plo = False
            found_psh = False

            while time.time() - start < total_timeout:
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                logger.debug(f"Recv = {line}")
                if "(plo)%" in line:
                    found_plo = True
                    break
                if "psh" in line:
                    found_psh = True
                    break
                time.sleep(0.05)

        if found_plo:
            logger.info("Success: target is stopped in bootloader")
            return

        if not found_psh:
            logger.error("Cannot confirm if target is in bootloader or system")
            raise KeyError("Cannot confirm if target is in bootloader or system")

        # Reboot into plo
        logger.info("Target booted into the system, trying to reboot to bootloader")
        with serial.Serial(port, baudrate=baud, timeout=1) as ser:
            ser.write(b"reboot\n")

        # Wait for bootloader prompt after reboot
        start = time.time()
        while time.time() - start < total_timeout:
            with serial.Serial(port, baudrate=baud, timeout=0.5) as ser:
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                logger.debug(f"Recv = {line}")
                if "Waiting for input" in line:
                    ser.write(b"\n")
                    logger.info("Target locked in bootloader")
                    return
                time.sleep(0.05)

        logger.error("Timeout waiting for bootloader after reboot")
        raise TimeoutError("Timeout waiting for bootloader after reboot")

    except serial.SerialException as e:
        logger.error(f"Serial error: {e}")
        raise



def plo_copy(
    port: str,
    baud: int,
    size: int,
    alias: str,
    offset: int,
    dry: bool,
    total_timeout: int = 180,
):
    copy_command = f"copy ramdisk 0 {size} {alias} {offset} {size}"
    logger.info(f"Bootloader 'plo' copy command: {copy_command}")

    if dry:
        logger.info("Dry run, skip plo copy command")
        return

    start = time.time()
    try:
        with serial.Serial(port, baudrate=baud, timeout=0.5) as ser:
            ser.reset_input_buffer()  # Flush any old data

            # Send the copy command
            ser.write((copy_command + "\n").encode())
            logger.info("Waiting for bootloader to finish copy...")

            while True:
                if time.time() - start > total_timeout:
                    logger.error("Timeout waiting for (plo)% prompt after copy")
                    raise TimeoutError(
                        "plo_copy timed out waiting for (plo)% prompt after copy"
                    )
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                logger.debug(f"Recv = {line}")
                if line.startswith("(plo)%"):
                    break
                time.sleep(0.05)  # Prevent busy loop
    except serial.SerialException as e:
        logger.error(f"Serial error: {e}")
        raise

    duration = time.time() - start
    logger.info(f"Successfully copied image to flash in {duration:.2f}s")
