#!/usr/bin/env python
"""
USAGE:

caheck.py ssh://path/to/the/repo

This script clones repository which is not exists and
after that it checks requirements.txt for any changes.
"""

import git
import os
import subprocess
import sys

def check_args():
    if not len(sys.argv) > 1:
        print __doc__
        sys.exit(1)

if __name__ == "__main__":
    check_args()

    if os.path.exists(sys.argv[1]):
        subprocess.call('ls -l', shell=True)
    else:
        print "No luck"

#    repo = git.Repo("/home/ai/Scripts/check-requirements/cache/")
#    assert repo.bare == False
#    git.Git().clone("ssh://gerrit.mirantis.com/openstack-ci/openstack/nova-build")    
