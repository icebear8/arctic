#!/bin/sh

KEY_DIRECTORY=${GIT_CONFIG_DIR}/.ssh


# Remove keys if they exist
if [ -f ${KEY_DIRECTORY}/id_rsa ]; then
  rm ${KEY_DIRECTORY}/id_rsa
  rm ${KEY_DIRECTORY}/id_rsa.pub
fi

# Generate ad hoc keys for authentication
ssh-keygen -f ${KEY_DIRECTORY}/id_rsa -q -P ""
