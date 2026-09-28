#!/usr/bin/env bash
# Start n8n for NewsHub. NO_PROXY must list 127.0.0.1 explicitly:
# n8n's HTTP client ignores CIDR ranges like 127.0.0.0/8, so local calls would go through the proxy.
export NO_PROXY=localhost,127.0.0.1,::1
export no_proxy=$NO_PROXY
export N8N_HOST=127.0.0.1
export N8N_LISTEN_ADDRESS=127.0.0.1
export N8N_SECURE_COOKIE=false
export N8N_DIAGNOSTICS_ENABLED=false
export N8N_VERSION_NOTIFICATIONS_ENABLED=false
exec n8n "${@:-start}"
