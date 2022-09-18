# CLI options

help() {
  echo -e "Usage: toolbox-shortcuts create /path/to/binary_name container_name"
  exit 0
}

create() {
  local biname="$1"
  local containername="$2"

  [[ -z "${biname}" || -z "${containername}" ]] && help
  [[ -f "${biname}" ]] && perror "'${biname}' exists"

  ln -sf "${applicationroot}/toolbox-shortcuts-handler" "${applicationroot}/containers/${containername}" \
    || perror "creating symlink to handler failed"

  ln -sf "${applicationroot}/containers/${containername}" "$biname" \
    || perror "creating symlink to binary name failed"

  echo "Shortcut created: $(basename $biname) [ ⬢ $containername ]"
}