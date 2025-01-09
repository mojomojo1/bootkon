# Contributing

## Rationale

This document describes how to set up your environment in order to modify and extend the the bootkon code labs. You can use the Cloud Shell IDE directly to do this. This has the advantage that the tutorial markdown can be rendered without having to commit to GitHub or reloading Cloud Shell, drastically reducing the feedback time.

First, [open `CONTRIBUTING.md` in Cloud Shell](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/fhirschmann/bootkon-ng&page=editor&tutorial=CONTRIBUTING.md&show=ide&cloudshell_workspace=) in tutorial mode and follow the next steps directly in Cloud Shell.

## Create SSH keys and add them to GitHub

In order to commit and push changes to GitHub, perform the following steps.

Create SSH keys if they don't exist yet (just hit return when it asks for passphrases):
```bash
test -f ~/.ssh/id_rsa.pub || ssh-keygen -t rsa
```

Display your newly created SSH key and [add it to your GitHub account](https://github.com/settings/keys):
```bash
cat ~/.ssh/id_rsa.pub
```

## Set up Git

Overwrite the remote URL to use the SSH protocol insead of HTTPS. Adjust the command in case you are working on your personal fork:
```bash
git remote set-url origin git@github.com:fhirschmann/bootkon-ng.git
```

```bash
git config --global user.name "John Doe"
```
```bash
git config --global user.email johndoe@example.com  
```

Check your git config:
```bash
cat ~/.gitconfig
```

## Pushing to GitHub

You can now commit changes and push them to GitHub. You can either use the version control of the Cloud Shell IDE (tree icon on the left hand side) or the command line:

```bash
git status
```

## Set up your development environment

During the first lab, participants are asked to edit `vars.sh`. It is suggested to make a copy of this file and not touch the original in order not to accidently commit it to git.

First, make a copy:
```bash
cp vars.sh vars.local.sh
```

And <walkthrough-editor-open-file filePath="vars.local.sh">edit it</walkthrough-editor-open-file>. It also runs on Argolis (for Google employees).
Also add the following line at the bottom of your `vars.local.sh`.

```bash
alias r='cloudshell launch-tutorial -d TUTORIAL.md'
```

If you, for some reason, clone this repository again through Cloud Shell, you end up in a different working directory. Hence, just move your `vars.local.sh` to your home directory to easily find it again:
```bash
mv vars.local.sh ~/
```

Next, instead of doing `source vars.sh` as requested in the labs, do
```bash
source ~/vars.local.sh
```

## Reloading the tutorial

You can reload the tutorial on-the-fly by typing `r` into the terminal and pressing return. This is the alias we set up in `vars.local.sh`. Let's start by opening the tutorial:
```bash
r
```