from loguru import logger

def ramdisk_flash(partition: tuple[str, ...], serial: str, config: str, root: str):
    pass
    # Emit some nice log
    #partition_list = ', '.join(partition) if len(partition) > 1 else partition[0]
    #partition_label = 'partitions' if len(partition) > 1 else 'partition'
    #logger.info(
    #    f"Request to flash {partition_list} {partition_label} "
    #    f"using ramdisk, serial = {serial}, config = {config}"
    #)
