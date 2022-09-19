# Handler functions

source "${applicationroot}/lib/helpers.sh"

get_container_info() {
  source /run/.containerenv
  eval echo \$${1}
}

run_as_native() {
  IFS=:
  for binpath in $PATH; do
     local fullpath="${binpath}/${biname}"
   
     # Avoid looping
     [[ -L "$fullpath" && $(readlink -f "$fullpath") =~ /toolbox-shortcuts-handler$ ]] && continue
     [[ -x "$fullpath" ]] && exec "$fullpath" $*
  done

  perror "$biname: command not found"
}

run_as_container() {
  local pkgmanagers=("dnf" "yum" "apt" "apt-get" "pacman" "zypper" "rpm" "dpkg")
  local sudo=

  # sudo is only enabled for package manager
  in_array "$biname" ${pkgmanagers[*]} && sudo=sudo

  exec toolbox run -c $containername $sudo "$biname" $*
}