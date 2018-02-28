#!/bin/bash

JENKINS_DIR=/var/lib/jenkins
GIT_DIR=/jenkins_backup

cd $GIT_DIR
git pull --rebase origin master
rsync -aR $JENKINS_DIR/./jobs/*/config.xml $GIT_DIR
#ensure deleted projects are removed,
#previous line uses * which lists all exiting dirs, but not deleted ones
#and thus using --delete on previous line has no effect
rsync -dR --delete $JENKINS_DIR/./jobs/ $GIT_DIR
rsync -a --delete $JENKINS_DIR/*.xml $GIT_DIR
git add --all $GIT_DIR
git commit -m "Backup on `date +%Y-%m-%d-%H-%M`"
git push origin master


