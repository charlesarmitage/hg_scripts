# Merging between central repositories in Kiln
# 1. pull and update destination repo
# 3. pull from source repo
# 4. merge
# 5. commit with comment "Merge <source> to <destination>"
# 6. push

#TODO: Use in chainmerge script to run through a set list of branches for merging
#TODO: Use http://docs.python.org/2/library/argparse.html#module-argparse for arguement parsing
#TODO: Offer quick option that does not revert and purge
#TODO: Offer interactive option that runs hg in to check what will be merged and prompts for whether to merge

import subprocess
import string
import sys
import os

def execute_command(cmd, target_repo):
	print 'CWD %s> %s' % (target_repo, ' '.join(cmd))
	p = subprocess.Popen(cmd, cwd=target_repo, shell=True)
	p.wait()

def revert_and_purge(repo):
	execute_command(['hg', 'revert', '--all'], repo)
	execute_command(['hg', 'purge', '--all'], repo)

def pull_update(repo):
	execute_command(['hg', 'pull', '--update'], repo)

def pull_from_source(source_repo, dest_repo):
	execute_command(['hg', 'pull', source_repo], dest_repo)

def merge(dest_repo):
	execute_command(['hg', 'merge'], dest_repo)

def commit(source_repo, dest_repo):
	source_name = source_repo.split('\\')[-1]
	dest_name = dest_repo.split('\\')[-1]
	message = '-m"Merge {0} to {1}"'.format(source_name, dest_name)
	execute_command(['hg', 'commit', message], dest_repo)

def push(repo):
	execute_command(['hg', 'push'], repo)

def mergebranch(source_repo, dest_repo):
	revert_and_purge(dest_repo)
	pull_update(dest_repo)
	pull_from_source(source_repo, dest_repo)
	merge(dest_repo)
	commit(source_repo, dest_repo)
	push(dest_repo)

if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print "Usage: branchmerge source_repo destination_repo"
		sys.exit(-1)

	src = os.path.join(os.getcwd(), sys.argv[1])
	dst = os.path.join(os.getcwd(), sys.argv[2])
	mergebranch(src, dst)

