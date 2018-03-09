#!/bin/bash

# Prints plugins used by jobs
# Assumes $JENKINS_HOME is set or use /var/lib/jenkins as fall back

function check_job_dir() {
    if [ ! -d $1 ]; then
	echo 'Neither $JENKINS_HOME is set nor /var/lib/jenkins exists, or does not contain "jobs" sub dir, existing'
	exit 1
    fi
}

function list_plugins() {
    for cfg in `find $1 -maxdepth 2 -type f -name config.xml`; do
	cat "$cfg" |awk -F '=' '/^.*plugin=.*@/ {print $2}' | awk -F '@' '{gsub("\"",""); print $1}'
    done
}

function list_unique_plugins() {
    echo "Using $job_dir"
    check_job_dir $job_dir
    list_plugins $job_dir | sort -u
}

jenkins_dir="${JENKINS_HOME:-"/var/lib/jenkins"}"
job_dir=$jenkins_dir/jobs

list_unique_plugins $job_dir
