#!/bin/sh

# Remove keys if they exist
if [ -f ~/.ssh/id_rsa ]; then
  rm ~/.ssh/id_rsa
  rm ~/.ssh/id_rsa.pub
fi

# Generate ad hoc keys for authentication
ssh-keygen -f ~/.ssh/id_rsa -q -P ""
