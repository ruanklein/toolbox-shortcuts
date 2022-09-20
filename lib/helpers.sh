# Helper functions

in_array() {
  local currentvalue=
  local value="$1"
  shift 1

  for currentvalue; do
    [[ "$value" == "$currentvalue" ]] && return 0
  done

  return 1
}

get_option() {
  local currentvalue=
  local value="$1"
  shift 1

  for currentvalue; do
    [[ "$value" == "$currentvalue" ]] && break
  done

  echo $currentvalue
}

perror() {
  echo -e "error: $*" >&2
  exit 1
}

check_dep() {
  local dep="$1"

  command -v "$dep" >/dev/null && return 0
  return 1
}

is_container() {
  [[ -f "/run/.containerenv" ]] && return 0
  return 1
}

get_container_info() {
  source "/run/.containerenv"
  eval echo \$${1}
}