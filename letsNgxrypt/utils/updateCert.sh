#!/bin/sh

lego --"${LETSENCRYPT_CHALLANGE}" --tls.port ":${LETSENCRYPT_PORT}" --http.port ":${LETSENCRYPT_PORT}" --path "${CERTIFICATE_DIR}" \
     --email "${LETSENCRYPT_MAIL}" --domains "${LETSENCRYPT_DOMAINS}" --server="${LETSENCRYPT_SERVER}" --http.webroot "${NGX_CONTENT_DIR}" --accept-tos \
     ${LETSENCRYPT_GLOBAL_OPTIONS} \
     run
