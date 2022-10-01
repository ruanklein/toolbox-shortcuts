import sys
import subprocess
import os

from lib.constants import CONTAINER_FILE


def shell_run(command: str):
    return_code = subprocess.call(command, shell=True)
    return return_code


def print_error(error: str):
    print(f"Error: {error}", file=sys.stderr)


def is_container():
    return os.path.exists(CONTAINER_FILE)


def get_container_info(field: str):
    with open(CONTAINER_FILE) as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            if key == field:
                return value.replace('"', "")
    return None


def check_command_exists(command: str):
    exec = shell_run(f"command -v {command} >/dev/null")
    return exec == 0


def check_container_exists(container_name: str):
    exec = shell_run(f"podman container exists {container_name}")
    return exec == 0
