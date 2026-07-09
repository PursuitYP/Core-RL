#!/usr/bin/env bash
# Submit a CPU-only Core-RL experiment to the cluster rjob CPU task queues.
#
# Examples:
#   PARTITION=safethm_cpu_task bash experiments/alberta_core_rl/scripts/run_cpu_task.sh \
#     core-rl-output-main "python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_main.json"
#
#   PARTITION=safer2ai_cpu_task CPU=32 MEM=128000 bash experiments/alberta_core_rl/scripts/run_cpu_task.sh \
#     core-rl-all-main "python experiments/alberta_core_rl/scripts/run_all.py --suite main --seeds 0 1 2 3 4"
set -eo pipefail

export PATH="$PATH:$HOME/.local/bin"
export PYTHONUNBUFFERED="${PYTHONUNBUFFERED:-1}"
export PYTHONNOUSERSITE="${PYTHONNOUSERSITE:-1}"

NAME="${1:?usage: run_cpu_task.sh <job-name> <command> [extra rjob args...]}"
CMD="${2:?usage: run_cpu_task.sh <job-name> <command> [extra rjob args...]}"
shift 2 || true

PARTITION="${PARTITION:-safethm_cpu_task}"
CPU="${CPU:-16}"
MEM="${MEM:-64000}"
IMG="${IMG:-registry.h.pjlab.org.cn/ailab/pytorch2.7.0-cuda12.8-cudnn9:v5}"

case "$PARTITION" in
  safethm_cpu_task) NS=ailab-safethm; CG=safethm_cpu_task ;;
  safer2ai_cpu_task) NS=ailab-safer2ai; CG=safer2ai_cpu_task ;;
  *) echo "unknown PARTITION=$PARTITION"; exit 2 ;;
esac

echo "[submit-cpu] partition=$PARTITION ns=$NS charged=$CG cpu=$CPU mem=$MEM name=$NAME"
rjob submit --name="$NAME" \
  --gpu=0 --cpu="$CPU" --memory="$MEM" \
  --charged-group="$CG" --namespace="$NS" --private-machine=group \
  --image="$IMG" --image-pull-policy=IfNotPresent --priority=9 \
  --mount=gpfs://gpfs1/yupeng:/mnt/shared-storage-user/yupeng \
  --custom-resources brainpp.cn/fuse=1 \
  "$@" \
  -- bash -exc "cd /mnt/shared-storage-user/yupeng/Core-RL && export MPLCONFIGDIR=/tmp/core-rl-mplconfig && mkdir -p \$MPLCONFIGDIR && $CMD"
