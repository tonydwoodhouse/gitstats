#!/usr/bin/python

import re
import datetime
import os

from os import walk
from sys import stdout as sys_stdout
from subprocess import Popen, PIPE


# Set the current date and log file variables.
now = datetime.datetime.now()
fDir = "logs/{}{:0>2}{:0>2}".format(now.year, now.month, now.day)
fLog = "{}/gitlog.txt".format(fDir)


def main():
    # Delete the log file if it exists.
    if os.path.exists(fLog):
        os.remove(fLog)

    # Create the folder if it's not there.
    if not os.path.exists(fDir):
        os.mkdir(fDir)
    
    # Add the headers to the log file.
    writelogfile("Repository|WeekNum|Month|Date|Author|CommitHash|CommitDesc\n", fLog)
    
    # Collect the stats data from each repository.
    for root, dirs, _ in walk("."):
        if ".git" in dirs:
            print("%s" % (root[2:]))
            dirs.remove('.git')

            getstats(root, root[2:])
            print


def getstats(root, repo):
    """
    Gets all the stats of the Git repositories.
    """

    # Fetch all the meta data from Origin.
    process = Popen("git fetch", cwd=root, shell=True, stdout=PIPE, stderr=PIPE)
    _, stderr = process.communicate()
    success = not process.returncode

    if success:
        print("Fetched latest data from repo.")
    else:
        print(stderr)
        return

    # Push the log data into file.
    process = Popen("git log --remotes --format=\"{}|||%cd|%an|%h|%s\" --date=short".format(repo), cwd=root, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    success = not process.returncode

    if success:
        writelogfile(stdout.decode("utf-8"), fLog,)
        print("Branch commit history exported to {}".format(fLog))
    else:
        print(stderr)
    
    # Push the summary info into file.
    fSummary = "{}/gitsummary_{}.txt".format(fDir, repo)

    if os.path.exists(fSummary):
        os.remove(fSummary)

    process = Popen("git branch -r", cwd=root, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    success = not process.returncode

    if success:
        writelogfile(stdout.decode("utf-8"), fSummary)
        print("Branch summary info exported to {}".format(fSummary))
    else:
        print(stderr)

    print("")


def writelogfile(data, filename):
    file = open(filename, "a")
    file.write(data)
    file.close()


if __name__ == "__main__":
    main()
