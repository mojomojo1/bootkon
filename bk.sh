#!/bin/bash
# This script initializes the Data & AI Bootkon environment in Cloud Shell.
# It clones the Bootkon repository (or uses an existing one), sets up necessary
# environment variables, installs required packages, renders the tutorial markdown file,
# and finally opens the tutorial in Cloud Shell. It also adds helpful aliases and
# configurations to the .bashrc file for easier future access and customization.
#
# Author: Fabian Hirschmann
#
# Usage:
#   From GitHub (replace <username/repo>):
#     BK_REPO=<username/repo> BK_TUTORIAL=<tutorial.md> . <(wget -qO- https://raw.githubusercontent.com/<username/repo>/main/bk.sh)
#   Locally:
#     BK_REPO=<username/repo> BK_TUTORIAL=<tutorial.md> . bk.sh
#   Defaults, repo as argument:
#     . bk.sh <username/repo>
#
#   Skip workspace opening (add to ~/.bashrc above bk.sh):
#     export BK_NO_WORKSPACE_OPEN=1
#
# Environment variables:
#   BK_REPO: GitHub repository (<username/repo>). Defaults to fhirschmann/bootkon.
#   BK_TUTORIAL: Path to tutorial markdown (relative to repo root). Defaults to .TUTORIAL.md.
#   BK_NO_WORKSPACE_OPEN: Prevents workspace auto-opening.

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

err() {
  echo -e "${RED}Error: $1${NC}" >&2
}

echo -e "${YELLOW}Running bootkon init script $(readlink -f ${BASH_SOURCE[0]})...${NC}"

if [ -z $CLOUD_SHELL ]; then
    err 'Please run this script in Cloud Shell.'
    return 1
fi

if [ "${BASH_SOURCE[0]}" == "$0" ]; then
    err 'Script is not sourced. Please source it.'
    err 'Example: BK_REPO=fhirschmann/bootkon . bk.sh'
    exit 1
fi

if [ -z "$1" ]; then
    if [ -z $BK_REPO ]; then
        err 'Variable BK_REPO is not set. Please set it to a GitHub username and repository'
        err 'Example: BK_REPO=fhirschmann/bootkon . bk.sh'
        return 1
    fi
else
    export BK_REPO=$1
    echo -e "Setting BK_REPO to $BK_REPO based on first argument to this script."
fi


export BK_GITHUB_USERNAME=$(echo $BK_REPO | cut -d/ -f1) # first part of fhirschmann/bootkon
export BK_GITHUB_REPOSITORY=$(echo $BK_REPO | cut -d/ -f2) # second part of fhirschmann/bootkon
export BK_REPO_URL="https://github.com/${BK_REPO}.git"
export BK_TUTORIAL="${BK_TUTORIAL:-.TUTORIAL.md}" # defaults to .TUTORIAL.md; can be overwritten
export BK_DIR="~/${BK_GITHUB_REPOSITORY}"
export BK_INIT_SCRIPT=~/${BK_GITHUB_REPOSITORY}/bk.sh


cd ~/

if [ -d $BK_GITHUB_REPOSITORY ]; then
    echo -e "${GREEN}Not cloning $BK_REPO_URL because folder ~/$BK_GITHUB_REPOSITORY already exists.${NC}"
else
    echo -e "Cloning $BK_REPO_URL into $BK_GITHUB_REPOSITORY..."
    git clone https://github.com/${BK_REPO}.git
fi

cd $BK_GITHUB_REPOSITORY

echo -e "${MAGENTA}Loading tutorial from ${BK_TUTORIAL}${NC}"

NEW_PATH=~/${BK_GITHUB_REPOSITORY}/.scripts

# Check if the new path is already in the PATH
if [[ ":$PATH:" != *":$NEW_PATH:"* ]]; then
echo -e "${MAGENTA}Adding $NEW_PATH to your PATH${NC}"
    export PATH=${NEW_PATH}:$PATH
else
    echo -e "${GREEN}Your PATH already contains $NEW_PATH. Not adding it again.${NC}"
fi

echo -e "Sourcing $(readlink -f vars.sh)"
source vars.sh

if [ -f vars.local.sh ]; then
    echo -e "Sourcing $(readlink -f vars.local.sh)"
    source vars.local.sh
fi

echo -e "Variables: PROJECT_ID=${YELLOW}$PROJECT_ID${NC} GCP_USERNAME=${YELLOW}$GCP_USERNAME${NC} REGION=${YELLOW}$REGION${NC}"


if [ -z $PROJECT_ID ]; then
    echo -e "The variable PROJECT_ID is empty. Not setting the default Google Cloud project."
else
    echo -e "Setting Google Cloud project to ${PROJECT_ID}..."
    gcloud config set project $PROJECT_ID
fi

## Set or update $BK_REPO in ~/.bashrc
line="export BK_REPO=${BK_REPO}"
if grep -q '^export BK_REPO=' ~/.bashrc; then
    # If the line exists but differs, update it
    if ! grep -Fxq "$line" ~/.bashrc; then
        sed -i "s|^export BK_REPO=.*|$line|" ~/.bashrc
        echo "Updated the existing BK_REPO line in ~/.bashrc."
    fi
else
    echo "Adding BK_REPO to .bashrc"
    echo "$line" >> ~/.bashrc
fi

## Set or update $BK_INIT_SCRIPT in ~/.bashrc
line="export BK_INIT_SCRIPT=~/${BK_GITHUB_REPOSITORY}/bk.sh"
if grep -q '^export BK_INIT_SCRIPT=' ~/.bashrc; then
    # If the line exists but differs, update it
    if ! grep -Fxq "$line" ~/.bashrc; then
        sed -i "s|^export BK_INIT_SCRIPT=.*|$line|" ~/.bashrc
        echo "Updated the existing BK_INIT_SCRIPT line in ~/.bashrc."
    fi
else
    echo "$line" >> ~/.bashrc
fi

## Load $BK_INIT_SCRIPT in ~/.bashrc
line='if [ -f ${BK_INIT_SCRIPT} ]; then source ${BK_INIT_SCRIPT}; fi'
grep -qxF "$line" ~/.bashrc || echo "$line" >> ~/.bashrc

mkdir -p docs/output
bk-render-jinja2 docs/TUTORIAL.md docs/output/TUTORIAL.md

bk-tutorial $BK_TUTORIAL
# Run it twice due to bug in pantheon
bk-tutorial $BK_TUTORIAL

if [ "$(basename $PWD)" == $BK_GITHUB_REPOSITORY ]; then
    if [ -z $BK_NO_WORKSPACE_OPEN ]; then
        echo -e "${RED}Warning: Force-opening workspace $PWD. Press CTRL+C to cancel."
        echo -e "${RED}If this is unintended, add the following to ~/.bashrc just above BK_REPO:${NC}"
        echo -e "${BLUE}export BK_NO_WORKSPACE_OPEN=1${NC}"
        sleep 3
        cloudshell open-workspace .
    fi
fi

echo

cat << "EOF"
         __                 --------------------------------------------------------
 _(\    |@@|                |                                                      |
(__/\__ \--/ __             |          Welcome to the Data & AI Bootkon!           |
   \___|----|  |   __       |                                                      |
       \ }{ /\ )_ / _\      --------------------------------------------------------
       /\__/\ \__O (__
      (--/\--)    \__/
      _)(  )(_
     `---''---`
EOF
echo