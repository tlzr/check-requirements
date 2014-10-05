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
import sys

#knownBuilds = ('python-novaclient', 'nova')
gitloc = 'https://github.com/openstack/'
repodir = 'cache'

def check_args():
    if not len(sys.argv) > 1:
        print __doc__
        sys.exit(0)

def check_path(name):
    repoloc = repodir + '/' + name

    if os.path.exists(repoloc):
        repo = git.Git(repoloc)
        repo.pull()
        repo.log('--since=1410993264', '--pretty=format:%H,%at')
        repo.config('remote.origin.url')
    else:
        git_clone(name, repoloc)

def git_clone(name, repoloc):
    print 'Clonning %s into %s ...' repoloc + '.git', repodir + name
    git.Git().clone(gitloc + name + '.git', repoloc)

if __name__ == "__main__":
    check_args()
    knownBuilds = sys.argv[1:]
    [check_path(i) for i in knownBuilds]

