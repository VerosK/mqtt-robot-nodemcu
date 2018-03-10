#! /usr/bin/env python3

from pathlib import Path
import subprocess
import time
import pprint
import re

import click
import requests


SPEED = 115200
DEFAULT_FILENAME = 'esp8266-20171101-v1.9.3.bin'
DEFAULT_URL = 'http://micropython.org/resources/firmware/' + DEFAULT_FILENAME

BASE_PATH = Path(__file__).parent.parent


def shell_escape(string):
    if re.match('^[-_./a-zA-Z0-9]*$', string):
        return string
    else:
        return "'" + string.replace("'", r"'\''") + "'"


def run(args, **kwargs):
    click.secho('RUN: ' + ' '.join(shell_escape(a) for a in args), fg='blue')
    kwargs.setdefault('check', True)
    return subprocess.run(args, **kwargs)


@click.command()
@click.option('-p', '--port', default='/dev/ttyUSB0',
              help='Device on which MicroPython is connected '
                '(use e.g. COM3 for Windows)')
@click.option('-f', '--firmware-file', default=DEFAULT_FILENAME,
              type=click.Path(dir_okay=False),
              help='File with firmware (downloaded if missing)')
@click.option('-U', '--firmware-url', default=DEFAULT_URL,
              help='URL from which firmware is downloaded if missing')
@click.option('--flash-mode', 'flash_mode', default='dio',
              help='Flash mode (see esptool --help)')
@click.option('-x/-X', '--flash/--no-flash', default=True,
              help='Flash firmware. (Use -X if only updating files)')
@click.option('-c/-C', '--common-files/--no-common-files', default=True,
              help='Upload common files.')
@click.argument('code_dir', nargs=-1, required=True)
def flash_me(port, firmware_file, firmware_url, flash, flash_mode,
             common_files, code_dir):
    """Flash firmware and scripts to a NodeMCU board

    Pass CODE_DIR to get the behavior you want:

        - 'mqtt': Robot controlled over a MQTT server

        - 'autonomous': autonomous robot (with bumper switches)
    """
    pprint.pprint(vars())
    firmware_path = Path(firmware_file)
    run(['ampy', '--version'])
    if flash:
        if not firmware_path.exists():
            # Download firmware
            response = requests.get(firmware_url)
            response.raise_for_status()
            firmware_path.write_bytes(response.content)
        run(['esptool.py',
            '--port', str(port),
            'erase_flash'])
        run(['esptool.py',
            '--port', str(port),
            '--baud', str(SPEED),
            'write_flash',
            '--flash_size=detect',
            '--flash_mode=' + flash_mode,
            '0',
            firmware_file])
        click.secho('== Reset board now; press enter ==', fg='yellow')
        click.pause()

    directories = list(code_dir)
    if common_files:
        directories.insert(0, BASE_PATH / 'common')

    for directory in directories:
        path = BASE_PATH / directory
        for filepath in path.glob('*.py'):
            click.secho('Uploading ' + str(filepath))
            run(['ampy',
                 '--port', port,
                 'put', str(filepath), str(filepath.name)])


if __name__ == '__main__':
    flash_me()
