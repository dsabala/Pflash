"""
This module checks environment conditions
"""

import os
import pathlib
from dataclasses import dataclass
import yaml


def get_inv_directory(rootdir: str):
    """Return the directory where the script was invoked."""
    if rootdir:
        return rootdir

    return os.getcwd()


@dataclass
class Partition:
    """
    Represents a partition with its attributes and parent device information.
    """

    name: str
    filename: str
    offs: int
    block_device: str
    block_size: int
    device_size: int
    size: int


def parse_value(value):
    """Convert hexadecimal strings to integers."""
    if isinstance(value, str) and value.startswith("0x"):
        return int(value, 16)
    return value


def get_flash_jobs_list(
    prj: str,
    root: str,
    parts: tuple[str, ...],
) -> list:
    """
    Get a list of jobs to do during typical flashing job:
        - read basic partition knowledge from nvm.yaml file
        - confront partitions from nvm.yaml with passed parts argument
        - collect essential info
    """

    # Load nvm.yaml file from project subdir
    try:
        nvm_yaml_path = pathlib.Path(root) / "_projects" / prj / "nvm.yaml"
        with open(nvm_yaml_path, "r", encoding="utf-8") as file:
            data = yaml.load(file, Loader=yaml.Loader)
    except Exception as e:
        raise ValueError("Error decoding YAML configuration file") from e

    # Parse partitions list
    partitions = []
    for device_name, device_info in data.items():
        device_size = parse_value(device_info.get("size"))
        for part_info in device_info.get("partitions", []):
            partition = Partition(
                name=part_info.get("name"),
                filename="part_" + part_info.get("name") + ".img",
                offs=parse_value(part_info.get("offs")),
                size=parse_value(part_info.get("size")),
                block_device=device_name,
                block_size=parse_value(device_info.get("block_size")),
                device_size=device_size,
            )
            partitions.append(partition)

    # Sort partitions by offset
    partitions.sort(key=lambda p: p.offs)

    # Calculate sizes for partitions with undefined size
    for i, partition in enumerate(partitions):
        if partition.size is None:
            if i < len(partitions) - 1:
                partition.size = partitions[i + 1].offs - partition.offs
            else:
                partition.size = partition.device_size - partition.offs

    # Filter partitions based on the provided names
    filtered_partitions = [p for p in partitions if p.name in parts]

    return filtered_partitions
