#!/bin/sh

if ! [[ -z "~/.ssh/id_rsa" ]]; then
  sh ./regenerateKey.sh
fi