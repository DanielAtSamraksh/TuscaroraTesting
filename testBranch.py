#!/usr/bin/env python
# (Use /usr/bin/env for portabiity, see http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script)

import argparse
import os
import subprocess

############# Methods ################

def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError(
            "readable_dir:{0} is not a valid path".format(prospective_dir))
    if not os.access(prospective_dir, os.R_OK):
        raise argparse.ArgumentTypeError(
            "readable_dir:{0} is not a readable dir".format(prospective_dir))
    return prospective_dir

def cmd(cmd): # run a command
    return subprocess.check_output( cmd, cwd=repo ) # repo is global

########## Main Starts Here #############

# from http://stackoverflow.com/a/1265445/268040, ensure only one instance is running.
from tendo import singleton # install with "sudo pip install tendo"
me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

### Parsing Arguments
parser = argparse.ArgumentParser(description='Test a branch.')

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
# print args.accumulate(args.integers)

parser.add_argument( '--args', metavar='args', help="Arguments to pass to the test script.",
                     default="--report-dir /var/www/RegressionTest/NightlyTest/Reports/ --output-dir /var/www/RegressionTest/NightlyTest/TestOutput/ --html" )

parser.add_argument(
    'test', metavar='test', type=file,
    help="Path to the test program in the repo. "
    "The test program is run from its parent directory.");

parser.add_argument( 'branches', metavar='branches', nargs='+', 
                     help='Branches to test.')

args = parser.parse_args()
print (args);

if not args.test.closed: args.test.close()
test = "./%s"%os.path.basename(args.test.name)
repo = os.path.dirname(args.test.name) # global
print "test: %s, repo: %s"%(test, repo)

### run tests for each branch specified    
for branch in args.branches:
    try:
        print "branch = %s"%branch
        original_branch = cmd( ["git", "rev-parse", "--abbrev-ref", "HEAD"] )
        original_branch = original_branch.strip()
        print "original_branch = %s"%original_branch

        if original_branch != branch: 
            cmd( ["git", "checkout", branch] )

        cmd( ["git", "pull"] ) # bring branch up-to-date.
        
        # current_commit = subprocess.check_output( ["git", "rev-parse", "HEAD"], cwd=repo )
        # current_commit = current_commit.strip();
        # print "current_commit = %s"%current_commit

        try:
            # run the test with the arguments. The arguments need to
            # be parsed according to the shell.
            import shlex # see http://stackoverflow.com/a/899314/268040
            print cmd ( [test] + shlex.split(args.args or '') )
        except subprocess.CalledProcessError as e:
            print e.output
            
        if original_branch != branch: 
            cmd( ["git", "checkout", original_branch] )
    
    except subprocess.CalledProcessError as e:
        print "%s Error: command %s gave error: %s"%(__file__, e.cmd, e)
        print e.output
        continue
