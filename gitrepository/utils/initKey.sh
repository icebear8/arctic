#!/bin/sh

# Prepare known hosts if not existing
if [ -f ~/.ssh/known_hosts ]; then
  for f in /opt/utils/known_hosts*
  do
    cat $f > ~/.ssh/known_hosts
  done
fi

# Remove keys if they exist
if [ -f ~/.ssh/id_rsa ]; then
  rm ~/.ssh/id_rsa
  rm ~/.ssh/id_rsa.pub
fi

# Generate ad hoc keys for authentication
ssh-keygen -f ~/.ssh/id_rsa -q -P ""
