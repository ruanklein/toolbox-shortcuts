from os import path, symlink

from lib.helpers import \
    check_command_exists, \
    check_container_exists, \
    is_container, \
    get_container_info, \
    print_error

from lib.constants import SCRIPT_HANDLER_NAME


def help(app_root: str, args: list[str]):
    print('Usage: toolbox-shortcuts create /path/to/executable_name container_name')
    return 0


def create(app_root: str, args: list[str]):
    if len(args) != 2:
        return help(app_root, args)

    command, container_name = args

    if path.exists(command):
        print_error(f"{command}: file exists")
        return 1

    if not check_command_exists('podman'):
        message_error = 'podman not found'

        if is_container():
            running_container = get_container_info('name')
            message_error += f" (you're in ⬢ {running_container})"

        print_error(message_error)
        return 1

    if not check_container_exists(container_name):
        print_error(f"container '{container_name}' does not exist")
        return 1

    try:
        container_path = f"{app_root}/containers/{container_name}"

        if not path.exists(container_path):
            symlink(f"{app_root}/{SCRIPT_HANDLER_NAME}", container_path)

        symlink(container_path, command)
    except Exception as e:
        print_error(str(e))
        return 1

    print(f"Shortcut created: {path.basename(command)} [ ⬢ {container_name} ]")
    return 0
