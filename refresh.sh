#!/bin/sh

gitRemote="base"
gitUrl="https://gitlab.cs.man.ac.uk/a21674fl/comp24011.git"
gitBranch="lab4"

set -e
git remote remove "$gitRemote" || true
git remote add "$gitRemote" "$gitUrl"
git fetch "$gitRemote"
git merge "$gitRemote/$gitBranch"

# vim:set et sw=2 ts=2:
