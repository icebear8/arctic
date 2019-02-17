#!/bin/sh

DETECTED_IP=""

if [ "${LOC_IPV}" == "ipv6" ]
then
  # Get IPv6 IP, ignore private IPv6 IPs starting with f (e.g. ffdd:::::), only use the fist detected IP
  DETECTED_IP=$(ip addr show dev ${LOC_INTERFACE} | grep -oE "inet6 [0-9A-Da-d][0-9A-Fa-f:]*" | awk 'NR==1{print $2}')
else
  # Get IPv4, only use the first detected IP
  DETECTED_IP=$(ip addr show dev ${LOC_INTERFACE} | grep -oE "inet [0-9.]*" | awk '{print $2}')
fi

CACHED_IP=$(cat ${IP_CACHE_PATH})

# Check whether an IP has been detected
if [ "${DETECTED_IP}" == "" ]
then
  if [ ${CACHED_IP} != "INVALID_IP" ]
  then
    echo "INVALID_IP" > ${IP_CACHE_PATH}
    echo "ERROR: No IP detected, abort"
  fi
  exit 1
fi

# Check whether the IP has been changed
if [ "${DETECTED_IP}" == "${CACHED_IP}" ]
then
  exit 0
fi

if [ "${CACHED_IP}" == "INVALID_IP" ]
then
  echo "INFO: Recovered, IP detected again, update"
fi

# Cache IP and update
echo ${DETECTED_IP} > ${IP_CACHE_PATH}
curl "https://dyn.dns.he.net/nic/update?hostname=${DNS_HOSTNAME}&password=${DNS_TOKEN}&myip=${DETECTED_IP}"
