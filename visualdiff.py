"""
Compare markdown and HTML versions of posts.
Assumes they are already generated
"""

import csv
import pathlib
import subprocess
import time
import multiprocessing
import os
import sys

tqdm = lambda x, **kw: x
if sys.stdout.isatty():
    try:
        from tqdm import tqdm
    except ImportError:
        pass

def unsorted_parallel_map(f, lst, n=10):
    with multiprocessing.Pool(n) as p:
        yield from tqdm(p.imap_unordered(f, lst), total=len(lst))

def pixel_compare(path1, path2):
    return subprocess.run(["node", "pixel-compare.js", path1, path2], stderr=subprocess.DEVNULL).returncode == 0

def html_compare(path1, path2):
    return False

def blog_articles():
    return sorted(x.stem for x in pathlib.Path("posts-html").iterdir())

def compare(post_id):
    url = "https://blog2.za3k.com/posts/{}.html".format(post_id)
    html_path = "public/posts/{}.orig.html".format(post_id)
    markdown_path = "public/posts/{}.md.html".format(post_id)
    pixel_identical = pixel_compare(html_path, markdown_path)
    html_identical = html_compare(html_path, markdown_path)
    return [post_id, url, pixel_identical, html_identical]

if __name__ == "__main__":

    start_time = time.time()
    with open("visual-diff.csv", "w") as _csv:
        csvfile = csv.writer(_csv, dialect="excel")
        csvfile.writerow(["post-id", "url", "pixel-perfect?", "html-identical?"])
        rows = sorted(unsorted_parallel_map(compare, blog_articles()))
        csvfile.writerows(rows)
    time_elapsed = time.time() - start_time

    both_identical = len([x for x in rows if x[2] and x[3]])
    pixel_identical = len([x for x in rows if x[2]]) - both_identical
    html_identical = len([x for x in rows if x[3]]) - both_identical
    total = len(rows)
    neither_identical = total - pixel_identical - html_identical - both_identical

    print("        Progress Tracker\n")
    print("           pixel:NO   pixel: YES ")
    print("          |-----------|-----------|")
    print(" html:NO  |    {: >2.0f}%    |    {: >2.0f}%    |    {: >2.0f}%".format(neither_identical/total*100, pixel_identical/total*100, (neither_identical + pixel_identical)/total*100))
    print("          |-----------|-----------|")
    print(" html:YES |    {: >2.0f}%    |    {: >2.0f}%    |    {: >2.0f}%".format(html_identical/total*100, both_identical/total*100, (html_identical + both_identical)/total*100))
    print("          |-----------|-----------|")
    print("               {: >2.0f}%    {: >2.0f}%".format((neither_identical + html_identical)/total*100, (pixel_identical+both_identical)/total*100))
    print()
    print("Posts: {}".format(total))
    print("Time: {:.0f}s".format(time_elapsed))
    print("Time per file: {:.2f}s".format(time_elapsed/total))

    os.system("rm -r /tmp/puppeteer_dev_chrome_profile-X*")
