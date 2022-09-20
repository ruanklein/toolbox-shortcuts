# CLI options

source "${applicationroot}/lib/helpers.sh"

help() {
  echo -e "Usage: toolbox-shortcuts create /path/to/executable_name container_name"
  exit 0
}

create() {
  local biname="$1"
  local containername="$2"

  [[ -z "${biname}" || -z "${containername}" ]] && help
  [[ -f "${biname}" ]] && perror "'${biname}' exists"

  podman container exists "$containername" || perror "container '${containername}' does not exist"

  ln -sf "${applicationroot}/toolbox-shortcuts-handler" "${applicationroot}/containers/${containername}" \
    || perror "creating symlink to handler failed"

  ln -sf "${applicationroot}/containers/${containername}" "$biname" \
    || perror "creating symlink to executable name failed"

  echo "Shortcut created: $(basename $biname) [ ⬢ $containername ]"
}