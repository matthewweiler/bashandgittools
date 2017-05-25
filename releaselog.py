import subprocess
import sys
	
args = sys.argv;
if len(args) < 2 or len(args) > 3  or ( len(args) == 3 and not args[1] == "--simple" and not args[1] == "--abbrev" ):
	print("Usage: git releaselog [--simple|--abbrev] release_branch_name")
	quit()
	
def listOfMergedBranches(baseBranch):
	return [branch.strip() for branch in subprocess.check_output(["git","branch", "-r", "--merged", baseBranch]).split("\n")]
	
def compareReleaseVersion(r1, r2):
	r1Parts = r1.split(".")
	r2Parts = r2.split(".")
	index = 0
	while True:
		if len(r1Parts) > index and len(r2Parts) <= index: return -1
		elif len(r1Parts) <= index and len(r2Parts) > index: return 1
		elif len(r1Parts) <= index and len(r2Parts) <= index: return 0
			
		ve1 = False
		ve2 = False
		try:
			int(r1Parts[index])
		except ValueError:
			ve1 = True
		try:
			int(r2Parts[index])
		except ValueError:
			ve2 = True
		if ve1 and ve2: return 0
		if ve1 and not ve2: return 1
		if not ve1 and ve2: return -1
		cmpPart =  int(r2Parts[index]) - int(r1Parts[index])
		if cmpPart == 0:
			index += 1
		else:
			return cmpPart
	
releaseBranch = args[1] if len(args) == 2 else args[2]

allReleaseBranches = listOfMergedBranches(releaseBranch)

lastRelease = ""
lastReleaseBranch = ""

for branch in allReleaseBranches:
	releaseIndex = branch.find("release/")
	if releaseIndex < 0:
		continue
	if branch.find(releaseBranch) >= 0:
		continue
	thisRelease = branch[releaseIndex + 8:]
	if compareReleaseVersion(lastRelease,thisRelease) > 0:
		lastRelease = thisRelease
		lastReleaseBranch = branch
lastReleaseBranches = listOfMergedBranches(lastReleaseBranch)

result = set(allReleaseBranches) - set(lastReleaseBranches)
result = list(result)
result.sort()
if len(args) == 3:
	if args[1] == "--abbrev":
		result = [r[r.rfind("/") + 1:] if r.rfind("/") >= 0 else r for r in result]
	elif args[1] == "--simple":
		result = [r[r.rfind("origin/") + 7:] if r.rfind("origin/") >= 0 else r for r in result]
		result = [r[r.rfind("deleted/") + 8:] if r.rfind("deleted/") >= 0 else r for r in result]
		result = [ r[1:] if r.find("/") == 0 else r for r in result]
print("Previous Release: " + lastRelease)
for r in result:
	print(r)
	
