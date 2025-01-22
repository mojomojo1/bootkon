#!/bin/bash
# Bootkon init script. Executing it will clone bootkon,
# open it in Cloud Shell, and launch the tutorial.
#
# Author: Fabian Hirschmann
#
# You can run this command directly from GitHub:
#    BK_REPO=fhirschmann/bootkon; . <(wget -qO- https://raw.githubusercontent.com/${BK_REPO}/refs/heads/main/bk.sh)
# or locally:
#    BK_REPO=fhirschmann/bootkon . bootkon/bk.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

cat << "EOF"
         __                 --------------------------------------------------------
 _(\    |@@|                | Welcome to the Data & AI Bootkon!                    |
(__/\__ \--/ __             |                                                      |
   \___|----|  |   __       | We're getting things ready for you, please stand by. |
       \ }{ /\ )_ / _\      --------------------------------------------------------
       /\__/\ \__O (__
      (--/\--)    \__/
      _)(  )(_
     `---''---`
EOF



err() {
  echo -e "${RED}Error: $1${NC}" >&2
}

echo -e "${YELLOW}Running bootkon init script $(readlink -f ${BASH_SOURCE[0]})...${NC}"


if [ "${BASH_SOURCE[0]}" == "$0" ]; then
    err 'Script is not sourced. Please source it.'
    err 'Example: BK_REPO=fhirschmann/bootkon . bk.sh'
    exit 1
fi

if [ -z $BK_REPO ]; then
    err 'Variable BK_REPO is not set. Please set it to a GitHub username and repository'
    err 'Example: BK_REPO=fhirschmann/bootkon . bk.sh'
    return 1
fi

BK_GITHUB_USERNAME=$(echo $BK_REPO | cut -d/ -f1) # first part of fhirschmann/bootkon
BK_GITHUB_REPOSITORY=$(echo $BK_REPO | cut -d/ -f2) # second part of fhirschmann/bootkon
BK_REPO_URL="https://github.com/${BK_REPO}.git"
BK_TUTORIAL="${BK_TUTORIAL:-.TUTORIAL.md}" # defaults to .TUTORIAL.md; can be overwritten

cd ~/

if [ -d $BK_GITHUB_REPOSITORY ]; then
    echo -e "${GREEN}Not cloning $BK_REPO_URL because folder ~/$BK_GITHUB_REPOSITORY already exists.${NC}"
else
    echo -e "Cloning $BK_REPO_URL into $BK_GITHUB_REPOSITORY..."
    git clone https://github.com/${BK_REPO}.git
fi

cd $BK_GITHUB_REPOSITORY

echo -e "${MAGENTA}Loading tutorial from ${BK_TUTORIAL}${NC}"

teachme $BK_TUTORIAL
# Run it twice due to bug in pantheon
teachme $BK_TUTORIAL

NEW_PATH=~/${BK_GITHUB_REPOSITORY}/docs/scripts

# Check if the new path is already in the PATH
if [[ ":$PATH:" != *":$NEW_PATH:"* ]]; then
echo -e "${MAGENTA}Adding $NEW_PATH to your PATH${NC}"
    export PATH=${NEW_PATH}:$PATH
else
    echo -e "${GREEN}Your PATH already contains $NEW_PATH. Not adding it again.${NC}"
fi

source vars.sh
if [ -f vars.local.sh ]; then
    echo -e "${MAGENTA}vars.local.sh exists -- sourcing${NC}"
    source vars.local.sh
fi

if [ -z $PROJECT_ID ]; then
    echo -e "The variable PROJECT_ID is empty. Not setting the default Google Cloud project."
else
    echo -e "${MAGENTA}Setting Google Cloud project to ${PROJECT_ID}...${NC}"
    gcloud config set project $PROJECT_ID
fi

line="export BK_REPO=$BK_REPO"
grep -qxF "$line" ~/.bashrc || echo "$line" >> ~/.bashrc

line="if [ -f ~/${BK_GITHUB_REPOSITORY}/bk.sh ]; then source ~/${BK_GITHUB_REPOSITORY}/bk.sh; fi"
grep -qxF "$line" ~/.bashrc || echo "$line" >> ~/.bashrc

if [ "$(basename $PWD)" == $BK_GITHUB_REPOSITORY ]; then
    if [ -z $BK_NO_WORKSPACE_OPEN ]; then
        echo -e "${RED}Warning: Force-opening workspace $PWD. Press CTRL+C to cancel."
        echo -e "${RED}If this is unintended, add the following to ~/.bashrc just above bk.sh${NC}:"
        echo -e "${BLUE}export BK_NO_WORKSPACE_OPEN=1${NC}"
        sleep 3
        cloudshell open-workspace .
        cloudshell edit-file WELCOME.txt
    fi
fi