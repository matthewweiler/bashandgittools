import subprocess
import sys

def trimline(line):
	return line.replace("*","").strip()

subprocess.check_output(["git","fetch", "-p"])
remoteBranches = subprocess.check_output(["git","branch", "-r"]).split("\n")
localBranches = subprocess.check_output(["git","branch"]).split("\n")

remoteDeletedBranches = [trimline(branch) for branch in remoteBranches if "origin/deleted" in branch]
nonDeletedLocalBranches = [trimline(branch) f:or branch in localBranches if "deleted/" not in branch]

for local in nonDeletedLocalBranches:
	for remoteDeleted in remoteDeletedBranches:
		if "origin/deleted/" + local == remoteDeleted:
			print(subprocess.check_output(["git","branch", "-D", local]).strip())
			break