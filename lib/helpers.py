import sys
import subprocess
import os


def run_program(exec: str):
    return_code = subprocess.call(exec, shell=True)
    sys.exit(return_code)


def print_error(error: str):
    print(f"Error: {error}", file=sys.stderr)
    sys.exit(1)


def is_container():
    container_file = '/run/.containerenv'
    return True if os.path.exists(container_file) else False


def get_container_info(field: str):
    container_file = '/run/.containerenv'
    with open(container_file) as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            if key == field:
                return value.replace('"', "")
    return None


def check_command_exists(command: str):
    return_code = subprocess.call(
        f"command -v {command} >/dev/null", shell=True)

    return True if return_code == 0 else False


def check_container_exists(container_name: str):
    return_code = subprocess.call(
        f"podman container exists {container_name}", shell=True)

    return True if return_code == 0 else False
