import click

@click.group()
def cli_entrypoint():
    """pflash - Phoenix RTOS flash utility"""
    pass

@cli_entrypoint.command()
@click.option("-s", "--serial", required=True, type=str)
@click.option("-c", "--config", required=True, type=str)
def flash_via_ramdisk(serial, config):
    """Flash board using plo RAMDISK, debugger and console"""
    click.echo(f"Flash via RAMDISK, serial = {serial}, config = {config}")
