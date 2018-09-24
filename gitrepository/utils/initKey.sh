#!/bin/sh

if [ -f ~/.ssh/id_rsa ]; then
  rm ~/.ssh/id_rsa
  rm ~/.ssh/id_rsa.pub
fi

ssh-keygen -f ~/.ssh/id_rsa -q -P ""
