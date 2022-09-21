from os import path, symlink

from lib.helpers import \
    check_command_exists, \
    check_container_exists, \
    is_container, \
    get_container_info


def help(app_root: str, args: list[str]):
    print('Usage: toolbox-shortcuts create /path/to/executable_name container_name')
    return 0


def create(app_root: str, args: list[str]):
    if len(args) != 2:
        return help(app_root, args)

    command, container_name = args

    if path.exists(command):
        print(f"{command}: file exists")
        return 1

    if not check_command_exists('podman'):
        message_error = 'podman not found'

        if is_container():
            running_container = get_container_info('name')
            message_error += f" (you're in ⬢ {running_container})"

        print(message_error)
        return 1

    if not check_container_exists(container_name):
        print(f"container '{container_name}' does not exist")
        return 1

    try:
        container_path = f"{app_root}/containers/{container_name}"

        if not path.exists(container_path):
            symlink(f"{app_root}/toolbox-shortcuts-handler", container_path)

        symlink(container_path, command)
    except Exception as e:
        print(str(e))
        return 1

    print(f"Shortcut created: {path.basename(command)} [ ⬢ {container_name} ]")
    return 0
