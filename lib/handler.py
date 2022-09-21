from os import path, environ, access, X_OK

from lib.helpers import print_error, run_program, check_command_exists
from lib import cli_options


def run_as_native(command_name: str, args: list[str]):
    env_path = environ['PATH']
    exec = None

    for bin_path in env_path.split(":"):
        full_bin_path = f"{bin_path}/{command_name}"

        if path.islink(full_bin_path):
            real_binary_name = path.basename(
                path.realpath(full_bin_path))

            if real_binary_name == 'toolbox-shortcuts-handler':
                continue

        if access(full_bin_path, X_OK):
            exec = f"{full_bin_path} {' '.join(args)}"
            break

    if not exec:
        print_error(f"{command_name}: command not found")

    run_program(exec=exec)


def run_as_container(command_name: str, container_name: str, args: list[str]):
    if not check_command_exists('toolbox'):
        print_error('toolbox not found')

    pkg_managers = ['dnf', 'yum', 'apt', 'apt-get',
                    'pacman', 'zypper', 'rpm', 'dpkg']

    sudo = 'sudo' if command_name in pkg_managers else ''
    exec = f"toolbox run -c {container_name} {sudo} {command_name} {' '.join(args)}"

    run_program(exec=exec)


def run_as_cli(app_root: str, args: list[str]):
    option_name = args[0] if len(args) > 1 else 'help'
    option_args = args[1:]

    is_option_exists = hasattr(cli_options, option_name)

    if is_option_exists:
        option = getattr(cli_options, option_name)
        return option(app_root, option_args)

    return cli_options.help(app_root, option_args)
