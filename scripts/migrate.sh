#!/usr/bin/env bash

init() {
  flask db init
}

history() {
  flask db history
}

downgrade() {
  flask db downgrade
}

migrate_and_upgrade() {
  echo flask db migrate -m \""${1}"\"
  flask db migrate -m \""${1}"\"
  echo flask db upgrade
  flask db upgrade
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  # Activate the virtual environment if present
  if [ -d venv ]; then
    source venv/bin/activate;
  fi
  # Run 
  if [[ "$1" == "init" ]]; then
    init
  else
    migrate_and_upgrade "${1}"
  fi
fi
