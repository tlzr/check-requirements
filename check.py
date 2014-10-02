#!/usr/bin/python

import sys
import urllib2

REQUIREMENTS='https://github.com/openstack/nova/blob/master/requirements.txt'

def get_requirements(url):
	"""Gets requirements and imports thems to base
       Raises
	"""
	csvfile = urllib2.urlopen(mosurl)
 
def process_requirements(file):
	    if urlre.match(mosurl) is None:
        print 'The URL is misspelled.'
        sys.exit(3)

if __name__ == "__main__":
	process_requirements(REQUIREMENTS)
	if urlre.match(REQUIREMENTS) is None:
            print 'The URL is misspelled.'
            sys.exit(3)
