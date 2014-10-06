#!/usr/bin/env python
"""
USAGE:

caheck.py [projects]

This script clones repository which is not exists and
after that it checks requirements.txt for any changes.

Please ensure that GitPython is installed:
pip install GitPython
"""

import argparse
import git
import os
import StringIO
import sys

gitloc = 'https://github.com/openstack/'
repodir = 'cache'
reqfile = 'requirements.txt'
logformat = 'format:%H,%at'

def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', metavar=('PROJECT', 'HASH'), nargs=2, help='Save the commit')
    parser.add_argument('-sl', '--save-last', metavar=('PROJECT'), nargs=1, help='Save the last commit')
    parser.add_argument('projects', nargs='+', help='List of projects, e.g. nova or python-novaclient')

    try:
        args = parser.parse_args()
    except Exception as e:
        parser.print_help()

    return args

def process(name):
    repoloc = repodir + '/' + name

    if os.path.exists(repoloc):
        repo = git.Git(repoloc)

        logs = StringIO.StringIO(repo.log('--since=1410993264', '--pretty=' + logformat, reqfile))
        for i in logs:
            commit_hash, commit_unixtime = i.split(',')
            print commit_hash
            print commit_unixtime
                       
        #piz2 = repo.config('remote.origin.url')
        #print piz2
    else:
        git_clone(name, repoloc)

def git_pull(name, repoloc):
    repo = git.Git(repoloc)
    print 'Pulling %s ...' % (name)
    repo.pull()

def git_clone(name, repoloc):
    print 'Clonning %s into %s ...' % (repoloc + '.git', repodir + '/' + name)
    git.Git().clone(gitloc + name + '.git', repoloc)

def pro(name):
    print name

if __name__ == "__main__":
    args = check_args()
    print args
    sys.exit(0)
    #[pro(i) for i in parser.projects]
    #main()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', dest='save', metavar=('PROJECT', 'HASH'), nargs=2, help='Save the commit')
    parser.add_argument('-sl', '--save-last', dest='save_last', metavar=('PROJECT'), nargs=1, help='Save the last commit')
    parser.add_argument('projects', nargs='+', help='List of projects, e.g. nova or python-novaclient')

    try:
        args = parser.parse_args()
    except Exception as e:
        parser.print_help()

    print args
 
    if args.projects:
        print args.projects
        [pro(i) for i in args.projects]
    elif args.save:
        print 'save'
    elif args.save_last:
        print 'save_last'


