#!bin/bash

# how to remove the git cache
git rm --cached {filename}

# how to reset the commit which will be rejected to push because of too large file
git rm --cached {filename}
echo {filename} > .gitignore
git commit --amend -CHEAD