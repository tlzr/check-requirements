#!/usr/bin/env python
"""
USAGE:

caheck.py [projects]

This script clones repository which doesn't exist and
pulls requirements.txt
You can also set the checkpoints and retrieve line from
the last initial change.

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
    parser.add_argument('-al',, '--all-logs', action='store_true', help='Get all logs')
    parser.add_argument('-df',, '--diff', action='store_true', help='Get diff')
    parser.add_argument('-l', '--list', metavar=('PROJECT'), nargs=1, help='Get commits list')
    parser.add_argument('projects', nargs='*', help='List of projects, e.g. nova or python-novaclient')
    parser.add_argument('-sl', '--save-last', metavar=('PROJECT'), nargs=1, help='Save the last commit')

    try:
        args = parser.parse_args()
    except Exception as e:
        parser.print_help()

    return args

def get_repodir(name):
    repoloc = os.path.join(repodir, '/', name)

    return repoloc

def check_repo(name):
    repoloc = get_repodir(name)

    if os.path.exists(repoloc):
        repo = git.Git(repoloc)
    else:
        git_clone(name, repoloc)
        repo = git.Git(repoloc)

    return repo

def git_pull(name):
    repo = check_repo(name)
    print 'Pulling %s ...' % (name)
    repo.pull()

def git_clone(name, repoloc):
    print 'Clonning %s into %s ...' % (repoloc + '.git', repodir + '/' + name)
    git.Git().clone(gitloc + name + '.git', repoloc)

def git_log(name):
    repo = check_repo(name)
    repoloc = get_repodir(name)
    fpath = repoloc + '.txt'

    if git_check_checkpoint(fpath) and not args.all-logs and not args.save-last:
        commit_hash, commit_unixtime = git_get_checkpoint()
        logs = StringIO.StringIO(repo.log('--since' + commit_unixtime, '--pretty=' + logformat, reqfile))
    else:
        logs = StringIO.StringIO(repo.log('--pretty=' + logformat, reqfile))

    if args.all-logs:
         for i in logs:
             print i
    
    if args.save-last:
        line = logs.readline()
        git_set_checkpoint(fpath, line)

    if args.diff and git_check_checkpoint(fpath):
        commit_hash, commit_unixtime = git_get_checkpoint(fpath).split(',')
        upstream_commit_hash, upstream_commit_unixtime = logs.readline().split(',')
        commit_diff = repo.diff(commit_hash+'..'+upstream_commit_hash, reqfile)

        if commit_diff:
            print 'Please update spec file'

            if args.diff:
                print commit_diff

def git_check_checkpoint(fpath):
    if os.path.isfile(fpath) and os.access(fpath, os.R_OK) and os.access(fpath, os.W_OK):
        return True
    else:
        return False

def git_set_checkpoint(fpath, line):
    with open(fpath, 'w') as f:
        f.write(line)

def git_get_checkpoint(fpath):
    with open(fpath, 'r') as f:
        buf = f.readline()
        commit_hash, commit_unixtime = buf.split(',')

    return (commit_hash, commit_unixtime)

def pro(name):
    print name

if __name__ == "__main__":
    args = check_args()

    if args.projects:
        print 'arg+proj'
        [pro(i) for i in args.projects]
    if args.list:
        print 'arg+list'
        [git_log(i) for i in args.list]
    if args.save:
        print 'save'
    if args.save_last:
        print 'save_last'
