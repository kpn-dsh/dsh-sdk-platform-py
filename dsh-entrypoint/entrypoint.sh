#!/usr/bin/env bash
medir=${0%/*}

source ${medir}/setup_ssl_dsh.sh

exec "$@"
