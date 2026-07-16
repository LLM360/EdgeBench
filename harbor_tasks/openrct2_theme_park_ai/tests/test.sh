#!/bin/bash
set -u

mkdir -p /logs/verifier
log_path=/logs/verifier/evaluator.log

set +e
timeout --signal=TERM --kill-after=10s 2300s \
    bash -c 'cd /home/workspace/openrct2 && OPENRCT2_TIMEOUT=120 python3 /tmp/eval_openrct2.py' \
    2>&1 | tee "$log_path"
eval_status=${PIPESTATUS[0]}
set -e

python3 /tests/write_reward.py \
    --eval-status "$eval_status" \
    "$log_path"
