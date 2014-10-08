#!/usr/bin/env python
"""
USAGE:

check.py -h

The main purpose of this script is to check
if some changes are taking place and to notifie
user about it.

Please ensure that GitPython is installed:
pip install GitPython
"""

import argparse
import git
import os
import re
import smtplib
import StringIO
import sys

gitloc = 'https://github.com/openstack/'
logformat = 'format:%H,%at'
repodir = 'cache'
reqfile = 'requirements.txt'
sender ='root@cz5577.host-telecom.com'
recipients = ['iudovichenko@mirantis.com', 'ii@mymailbox.pp.ua']

hashre = re.compile('^[a-z0-9]+$')
unixtimere = re.compile('^[0-9]+$')


def check_args():
    '''Checks arguments
       Returns object with all of it'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-al', '--all-logs', metavar=('PROJECT'), nargs='+', help='Get all logs')
    parser.add_argument('-df', '--diff', metavar=('PROJECT'), nargs='+', help='Get diff')
    parser.add_argument('-se', '--send-email', action='store_true', help='Send email')
    parser.add_argument('-sl', '--save-last', metavar=('PROJECT'), nargs=1, help='Save the last commit')
    parser.add_argument('-u', '--update', metavar=('PROJECT'), nargs='+', help='Update project list')

    if not len(sys.argv) > 1:
        parser.print_help()

    try:
        args = parser.parse_args()
    except Exception as e:
        parser.print_help()

    return args

def get_repodir(name):
    '''Returns the directory with cloned repository'''
    repoloc = os.path.join(repodir, name)

    return repoloc

def check_repo(name):
    '''Checks if the directory with cloned repository exista.
       If not, then clones it.
       Returns the repository object.'''
    repoloc = get_repodir(name)

    if os.path.exists(repoloc):
        repo = git.Git(repoloc)
    else:
        git_clone(name, repoloc)
        repo = git.Git(repoloc)

    return repo

def git_pull(name):
    '''Pulls changes for specified projects'''
    repo = check_repo(name)
    print 'Pulling %s ...' % (name)
    repo.pull()

def git_clone(name, repoloc):
    '''Clones repositories to specified location'''
    print 'Clonning %s into %s ...' % (repoloc + '.git', repodir + '/' + name)
    git.Git().clone(gitloc + name + '.git', repoloc)

def git_log(name):
    '''Checks logs of specified projects. If checkpoint
       (saved hash and unixtime) exists then it returns logs
       starting from this checkpoint, otherwise returns
       full log.
       Arguments: all-logs, diff, send-email, save-last,
       are processed here'''
    repo = check_repo(name)
    repoloc = get_repodir(name)
    fpath = repoloc + '.txt'

    if git_check_checkpoint(fpath) and not args.all_logs:
        commit_hash, commit_unixtime = git_get_checkpoint(fpath)
        logs = StringIO.StringIO(repo.log('--since=' + commit_unixtime, '--pretty=' + logformat, reqfile))
    else:
        logs = StringIO.StringIO(repo.log('--pretty=' + logformat, reqfile))

    if args.all_logs:
         print '\n----------------------\nShowing logs for %s:\
                \n----------------------' % (name)
         for i in logs:
             print i

    if args.save_last:
        line = logs.readline()
        print '\n----------------------\n Saving:\n         %s\
               \n----------------------' % (line)
        git_set_checkpoint(fpath, line)

    if args.diff and git_check_checkpoint(fpath):
        commit_hash, commit_unixtime = git_get_checkpoint(fpath)
        upstream_commit_hash, upstream_commit_unixtime = logs.readline().split(',')
        commit_diff = repo.diff(commit_hash+'..'+upstream_commit_hash, reqfile)
        if commit_diff:
            print commit_diff

            if args.send_email:
                send_mail(commit_diff)

def git_check_checkpoint(fpath):
    '''Checks if checkpoint exists and if "yes" then validates it
       Returns "True" if file exists and fits the format requirements
       otherwise "False"'''
    if os.path.isfile(fpath) and os.access(fpath, os.R_OK) and os.access(fpath, os.W_OK):
        with open(fpath, 'r') as f:
            buf = f.readline()
            if buf:
                buf = buf.split(',')
                if len(buf) == 2:
                    hash, unixtime = buf
                    if hashre.match(hash) and unixtimere.match(unixtime) is not None:
                        return True
                    else:
                        print 'Checkpoint has a malformed format. Please update/removes\
                               %s which contains it' % (fpath)
                        return False
    else:
        return False

def git_set_checkpoint(fpath, line):
    '''Creates/updates checkpoint'''
    with open(fpath, 'w') as f:
        f.write(line)

def git_get_checkpoint(fpath):
    '''Gets checkpoint
       Returns a tuple with hash and unixtime'''
    with open(fpath, 'r') as f:
        buf = f.readline()
        commit_hash, commit_unixtime = buf.split(',')

    return (commit_hash, commit_unixtime)

def send_mail(body):
    '''Formats message and sends it'''
    mail_server = 'localhost'
    mail_server_port = 25
    subject_header = 'Diff log'
    message = """\
From: %s
To: %s
Subject: %s

%s
""" % (sender, ", ".join(recipients), subject_header, body)
    s = smtplib.SMTP(mail_server, mail_server_port)
    s.sendmail(sender, recipients, message)
    s.quit()

if __name__ == "__main__":
    args = check_args()

    if args.update:
        [git_pull(i) for i in args.update]
    if args.all_logs:
        [git_log(i) for i in args.all_logs]
    if args.diff:
        [git_log(i) for i in args.diff]
    if args.save_last:
        [git_log(i) for i in args.save_last]
