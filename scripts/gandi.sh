#!/usr/bin/env bash

# Install script for a Python project

# App location (https://${GANDI_USER}.admin.sd6.gpaas.net/git/default.git):
# ls /srv/data/web/vhosts/default/

init() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Git repository already exists."
  else
    git init
    echo "Git repository initialized."
  fi
}

add_remotes(){
  git remote add gandi git+ssh://${GANDI_USER}@${GANDI_SERVER}/${GANDI_REPO}
  git remote add github git@github.com:${GITHUB_USER}/${APP_NAME}_app.git
  echo "Git repository remotes added."
}


push() {
  git push --force gandi master
  git push --force github master
}

deploy() {
  ssh ${GANDI_USER}@${GANDI_SERVER} deploy default.git
  ssh ${GANDI_USER}@${GANDI_SERVER} clean default.git
}

backup_db() {
  # mysqldump -u root -p ${APP_NAME}_db > ${APP_NAME}_db.sql
}

reset_log() {
  # App log file (https://${GANDI_USER}.admin.sd6.gpaas.net/log/www/uwsgi.log):
  # echo "" > /srv/data/var/log/www/uwsgi.log
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  if [[ "$1" == "init" ]]; then
    init
  else
    deploy
  fi
fi
