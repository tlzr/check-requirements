#!/usr/bin/env python
"""
USAGE:

caheck.py ssh://path/to/the/repo

This script clones repository which is not exists and
after that it checks requirements.txt for any changes.

Please ensure that GitPython is installed:
pip install GitPython
"""

import git
import os
#import subprocess
import sys

knownBuilds = ('nova', 'python-novaclient')

def check_args():
    if not len(sys.argv) > 1:
        print __doc__
        sys.exit(0)

def check_path(path):
    if os.path.exists(path):
        git_clone(path)
    else:
        print "Path: %s - doesn't exist." % path

def git_clone(path):
    

if __name__ == "__main__":
    check_args()
    [check_path(i) for i in knownBuilds]


#    if os.path.exists(sys.argv[1]):
#        subprocess.call('ls -l', shell=True)
#    else:
#        print "No luck"

#    repo = git.Repo("/home/ai/Scripts/check-requirements/cache/")
#    assert repo.bare == False
#    git.Git().clone("ssh://gerrit.mirantis.com/openstack-ci/openstack/nova-build")    

