#!/bin/bash
set -u

mkdir -p /logs/verifier
log_path=/logs/verifier/evaluator.log

set +e
timeout --signal=TERM --kill-after=10s 3500s \
    bash -c 'cd /home/workspace/openttd_ai && OPENTTD_N_SEEDS=5 python3 /tmp/eval_openttd.py' \
    2>&1 | tee "$log_path"
eval_status=${PIPESTATUS[0]}
set -e

python3 /tests/write_reward.py \
    --kind log-max \
    --baseline 100000 \
    --expert 1000000000 \
    --eval-status "$eval_status" \
    "$log_path"
