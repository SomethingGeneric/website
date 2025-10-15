#!/usr/bin/env sh

ENV_FILE="$1"
shift

if [ -z "$ENV_FILE" ]; then
	echo "Usage: $0 <env-file> <command> [args...]" >&2
	exit 1
fi

case "$ENV_FILE" in
	*/*) ENV_PATH="$ENV_FILE" ;;
	*) ENV_PATH="./$ENV_FILE" ;;
esac

if [ -f "$ENV_PATH" ]; then
	echo "Loading $ENV_FILE"
	set -a
	# shellcheck disable=SC1090
	. "$ENV_PATH"
	set +a
else
	echo "Warning: $ENV_FILE not found; running command without additional env vars" >&2
fi

exec "$@"
