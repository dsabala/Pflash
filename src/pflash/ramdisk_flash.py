"""
This module implements flash-via-ramdisk functionality
"""

import sys
import pflash.config as config
import pflash.project as project
from loguru import logger


def ramdisk_flash(parts: tuple[str, ...], ser: str, prj: str, root: str):
   """Flash-via-ramdisk functionality main function"""

   logger.info("Command line request to flash via ramdisk")
   logger.info(f"Project name: {prj}")

   # 1. Find configuration
   try:
      config_entry = config.load_config_entry(prj)
   except (FileNotFoundError, KeyError, ValueError) as e:
      logger.error(e)
      sys.exit(1)

   # 2. Find out project directory
   dir = project.get_inv_directory(root)
   logger.info(f"Project root: {dir}")

   # partition_list = ', '.join(partition) if len(partition) > 1 else partition[0]
   # partition_label = 'partitions' if len(partition) > 1 else 'partition'
   # logger.info(
   #   f"Request to flash {partition_list} {partition_label} "
   #   f"using ramdisk, serial = {serial}, config = {config} "
   #   f"root = {root}"
   # )
