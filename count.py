# If a Scratch studio has more than 100 projects, it just says 100+ on the studio webpage.
# This means that it is not convenient to get the number of projects... until now!
# This is a simple script that will tell you EXACTLY how many projects are in a studio,
# using the site-api.
#
# The way the site-api works is it looks at https://scratch.mit.edu/site-api/projects/in/xxx/y/
# where xxx is the studio ID and y is the page. Each page has 60 projects, except for the last page.
# For example, say a studio has 133 projects. Then it would have 3 pages of projects. The first
# two pages have 60 projects each, and the third page has 13 projects. Any page after that is
# the Scratch default 404 page.
#
# This program looks through the content of these webages until it finds a 404 page, at which point
# it calculates how many projects are in the studio.

from requests import get
import sys

# take and validate input

args = sys.argv[1:]
if args == []:
  studioLink = input("Link to the studio: ")
elif len(args) == 1:
  studioLink = args[0]
else:
  raise RuntimeError("Invalid input: script must be activated with 0 or 1 command line arguments")
  
studioLink = studioLink.rstrip("/") # eliminate trailing slash in URL
  
if studioLink[:-7] != "https://scratch.mit.edu/studios/":
  raise RuntimeError('Invalid input: input must be URL of the form "https://scratch.mit.edu/studios/#"')

studioID = studioLink[-7:]

try:
  int(studioID)
except ValueError:
  raise RuntimeError("Invalid input: studio ID must be a number")
  
# Get the number of projects in the studio

def matches(text, match): # returns the number of instances of match in text
  length = len(match)
  matchNum = 0
  while match in text:
    matchNum += 1
    index = text.index(match)
    text = text[index + length:]
  return matchNum
  
invalid = lambda x: "404" in x # if the page contains the string 404, then it was not found.
getStudio = lambda x: get("https://scratch.mit.edu/site-api/projects/in/{0}/{1}/".format(studioID, x)).text # gets page x from the Scratch website

pageCount = 1

while True: # this will break after it finds an invalid page
  page = getStudio(pageCount)
  if invalid(page):
    if pageCount == 1:
      raise RuntimeError("Unable to get the projects webpage for an unknown reason")
    else:
      break
  save = page # this will end up being the last webpage before the 404 error
  pageCount += 1
  
# each webpage has 60 projects, except for the last one, which we don't know, so we get that manually

projectCount = matches(save, "<li class") # looks for how many elements are in the final webpage
total = (pageCount-2) * 60 + projectCount

print("Total projects: {0}".format(total))
