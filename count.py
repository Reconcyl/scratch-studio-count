import sys, re, functools
import requests

PARSE_RE = re.compile(r"^(?:https?://)?scratch\.mit\.edu/studios/(\d+)/?$|^(\d+)$")
LI_RE = re.compile("<li")

EXIT_NOARGS = 1
EXIT_INVALID_STUDIO_ID = 2
EXIT_FIRST_PAGE_404 = 3

if len(sys.argv) == 1:
    print("Usage:")
    print("  {0} <url or studio ID>:    counts the projects in that studio".format(sys.argv[0]))
    print("  {0} -v <url or studio ID>: verbose mode (logs all queries)".format(sys.argv[0]))
    sys.exit(EXIT_NOARGS)

verbose = ("-v" in sys.argv)
studio_match = PARSE_RE.match(sys.argv[-1])
if not studio_match:
    print("Error: Invalid studio ID")
    print("Must be a URL (scratch.mit.edu/studios/12345678) or a number (12345678)")
    sys.exit(EXIT_INVALID_STUDIO_ID)
studio_id = studio_match.group(1)

@functools.lru_cache(maxsize=16)
def query_page(studio_id, page):
    if verbose:
        print(end="Querying page {0}... ".format(page))
    url = "https://scratch.mit.edu/site-api/projects/in/{0}/{1}/".format(studio_id, page)
    if verbose:
        print("done")
    return requests.get(url).text

def is_404(page_html):
    # The 404 page is a full webpage with a <!DOCTYPE>
    return ("<!D" in page_html)

def count_li(page_html):
    # Counts the number of instances of the string "<li" in the argument
    return len(LI_RE.findall(page_html))

page_maximum = 1
while True:
    page_html = query_page(studio_id, page_maximum)
    if is_404(page_html):
        if page_maximum == 1:
            print("Error: couldn't get the first page of studio results.")
            print("{0} might be an invalid studio ID.".format("scratch.mit.edu/studios/{0}".format(studio_id)))
            sys.exit(EXIT_FIRST_PAGE_404)
        page_minimum = page_maximum // 2
        break
    page_maximum *= 2

# preform a binary search to find the first 404 studio
while page_maximum - page_minimum > 1:
    page_num = (page_minimum + page_maximum) // 2
    page_html = query_page(studio_id, page_num)
    if is_404(page_html):
        page_maximum = page_num
    else:
        page_minimum = page_num

page_count = page_minimum
highest_page_html = query_page(studio_id, page_count)
highest_page_project_count = count_li(highest_page_html)
total = (page_count - 1) * 60 + highest_page_project_count
print(total)
