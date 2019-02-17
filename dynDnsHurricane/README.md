# Dynamic DNS Update for Hurricane Electrics
Simple script to periodically check and update the local IP to on [Hurricane Electric](https://dns.he.net) DNS.
This container **supports only Hurricane Electrics DNS servers**.

##  Changelog
* ddnshurricane:0.1-r1; Initial version

# Usage
`docker run -e "LOC_EXECUTION_PERIOD=1h" -e "LOC_INTERFACE=eth0" -e "LOC_IPV=ipv6" -e "DNS_HOSTNAME=my.domain.org" -e "DNS_TOKEN=mySecretHurricaneToken" icebear8/ddnshurricane:latest`

## Hints
- The script caches the IP and only updates if the IP has been changed
- `LOC_EXECUTION_PERIOD` supports `sleep` syntax (minutes `2m`, hours `2h`...)
- Cron has not been used for this implementation since the container since cron requires to be started as root
