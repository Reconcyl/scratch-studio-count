# `scratch-studio-count`

If a Scratch studio has more than 100 projects, it just says 100+ on the studio
webpage. This means that it is not convenient to get the number of projects...
until now! `scratch-studio-count` is a simple script written in Python3 that will
tell you EXACTLY how many projects are in a studio, using the site API.

Notes:
* Input can be via the command line or, if no arguments are provided, from input.
* This script can take a while to execute, depending on your internet connection.
* You must have the requests module installed to use this script. You can download
  it by typing `pip install requests` in the command line. (If this doesn't work,
  you might have to install pip)
