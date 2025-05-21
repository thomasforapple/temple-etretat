#!/bin/bash

# Fetch latest changes from the remote
git fetch

# Pull latest changes into the current branch
git pull

supervisorctl restart temple-etretat