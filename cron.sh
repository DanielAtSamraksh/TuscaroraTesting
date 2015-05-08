#!/bin/bash
set -x
# cron will not source .bashrc, so we need to do it in a script.
HOME=/home/dan
source ${HOME}/.bashrc
${HOME}/Tuscarora/Testing/testBranch.py ~/Tuscarora/TuscaroraFW/validate.sh dev master
