#!/bin/bash

JENKINS_DIR=${JENKINS_HOME:-"/var/lib/jenkins"}
JOB_DIR=$JENKINS_DIR/jobs

echo "Counting disk usage in $JOB_DIR"
du  -d 1 $JOB_DIR| sort -t' ' -n -r
