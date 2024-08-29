#! /usr/bin/env bash

usage() {
   echo "Gandi installation & development script."
   echo
   echo "Syntax: install.sh [-d|h]"
   echo "options:"
   echo "i     Initialize gandi and github remote repositories."
   echo "p     Push to remote repositories."
   echo "d     Deploy to gandi instance."
   echo "u     Print this help for usage."
   echo
}

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
  echo "Added gandi remote repository."
  git remote add github git@github.com:${GITHUB_USER}/${APP_NAME}_app.git
  echo "Added github remote repository."
}

push() {
  git push --force gandi master
  echo "Push to git gandi remote."
  git push --force github master
  echo "Push to git github remote."
}

deploy() {
  ssh ${GANDI_USER}@${GANDI_SERVER} deploy default.git
  echo "Deployed to Gandi."
  ssh ${GANDI_USER}@${GANDI_SERVER} clean default.git
  echo "Cleaned untracked files in repository."
}

source .env; # get environment variables

while getopts ":ipdu" option; do
    case $option in
        i) #
            init;
            add_remotes;;
        p) #
            push;;
        d) #
            deploy;;
        u) # display help
            usage;
            exit;;
        \?) # Invalid option
            echo "Error: Invalid option";
            exit;;
   esac
done
