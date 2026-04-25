#!/usr/bin/env bash
set -euo pipefail

API_HOST="${API_HOST:-127.0.0.1}"
API_PORT="${PORT:-8000}"
HURL_BASE_URL="${HURL_BASE_URL:-http://${API_HOST}:${API_PORT}}"
DATABASE_URL="${DATABASE_URL:-postgresql://taskflow:password@localhost:5432/taskflow}"
SECRET_KEY="${SECRET_KEY:-test-secret-key}"
HURL_PASSWORD="${HURL_PASSWORD:-password123}"
HURL_EMAIL_PREFIX="${HURL_EMAIL_PREFIX:-ci}"
HURL_EMAIL_DOMAIN="${HURL_EMAIL_DOMAIN:-example.com}"
HURL_AUTH_EMAIL="${HURL_AUTH_EMAIL:-${HURL_EMAIL_PREFIX}-auth-$(date +%s)@${HURL_EMAIL_DOMAIN}}"
HURL_TODOS_EMAIL="${HURL_TODOS_EMAIL:-${HURL_EMAIL_PREFIX}-todos-$(date +%s)@${HURL_EMAIL_DOMAIN}}"
API_PID=""

cleanup() {
  if [[ -n "${API_PID}" ]] && kill -0 "${API_PID}" 2>/dev/null; then
    kill "${API_PID}"
    wait "${API_PID}" 2>/dev/null || true
  fi
}

trap cleanup EXIT

command -v docker >/dev/null 2>&1 || {
  echo "docker is required for the hurl integration test database."
  exit 1
}

command -v hurl >/dev/null 2>&1 || {
  echo "hurl is required. Install hurl before running API endpoint tests."
  exit 1
}

echo "Running pytest..."
DATABASE_URL="sqlite:///./test_taskflow.db" SECRET_KEY="${SECRET_KEY}" python -m pytest

echo "Starting PostgreSQL..."
docker compose up -d db

echo "Waiting for PostgreSQL..."
until docker compose exec -T db pg_isready -U taskflow -d taskflow >/dev/null 2>&1; do
  sleep 1
done

echo "Starting API at ${HURL_BASE_URL}..."
DATABASE_URL="${DATABASE_URL}" SECRET_KEY="${SECRET_KEY}" python -m uvicorn main:app --host "${API_HOST}" --port "${API_PORT}" &
API_PID="$!"

echo "Waiting for API readiness..."
until curl -fsS "${HURL_BASE_URL}/readyz" >/dev/null 2>&1; do
  sleep 1
done

echo "Running hurl API tests..."
hurl --test --variable "base_url=${HURL_BASE_URL}" hurl/health.hurl
hurl --test --variable "base_url=${HURL_BASE_URL}" --variable "email=${HURL_AUTH_EMAIL}" --variable "password=${HURL_PASSWORD}" hurl/auth.hurl
hurl --test --variable "base_url=${HURL_BASE_URL}" --variable "email=${HURL_TODOS_EMAIL}" --variable "password=${HURL_PASSWORD}" hurl/todos.hurl

echo "All tests passed."
