# `scratch-studio-count`

Script to count pages in a Scratch studio.

Invoke as:

    python3 count.py [-v] studio

If `-v` is enabled, all queries to the site API will be logged. The studio can be given as
a URL or as a number.

It can also be used from other code as `count.count_pages(studio_id)` or `count.count_pages(studio_id, verbose=True)`,
where `studio_id` is a number or numeric string.
