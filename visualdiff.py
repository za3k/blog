"""
Compare markdown and HTML versions of posts.
Assumes they are already generated
"""

import csv
import json
import multiprocessing
import os
import pathlib
import subprocess
import sys
import time

tqdm = lambda x, **kw: x
if sys.stdout.isatty():
    try:
        from tqdm import tqdm
    except ImportError:
        pass

def unsorted_parallel_map(f, lst, n=10):
    with multiprocessing.Pool(n) as p:
        yield from tqdm(p.imap_unordered(f, lst), total=len(lst))

def pixel_compare(*args):
    result = subprocess.run(["node", "pixel-compare.js"] + list(args), capture_output=True)
    identical = result.returncode == 0
    output = result.stdout.decode('utf8')
    try:
        result = json.loads(output)
    except:
        print(args, output, file=sys.stderr)
        raise

    return identical, result

def blog_articles():
    return sorted(x.stem for x in pathlib.Path("posts-html").iterdir())

def compare(post_id, save=False):
    url = "https://blog2.za3k.com/posts/{}.html".format(post_id)
    local_url = "file:///home/zachary/blog/public/posts/{}.html".format(post_id)
    html_path = "public/posts/{}.orig.html".format(post_id)
    markdown_path = "public/posts/{}.md.html".format(post_id)
    html_screenshot_path = "screenshots/{}.html.png".format(post_id)
    markdown_screenshot_path = "screenshots/{}.md.png".format(post_id)
    visual_diff_path = "screenshots/{}.diff.png".format(post_id)
    pixel_identical, ret = pixel_compare(html_path, markdown_path, html_screenshot_path, markdown_screenshot_path, visual_diff_path)
    return [post_id, url, local_url, pixel_identical, html_screenshot_path, markdown_screenshot_path, visual_diff_path, ret["heightDifference"], ret["pixelsDifferent"]]

if __name__ == "__main__":

    start_time = time.time()
    with open("visual-diff.csv", "w") as _csv:
        csvfile = csv.writer(_csv, dialect="excel")
        csvfile.writerow(["post-id", "url", "local-url", "pixel-perfect?", "html-screenshot", "markdown-screenshot", "diff-screenshot", "height-difference", "pixels-different"])
        rows = sorted(unsorted_parallel_map(compare, blog_articles()))
        csvfile.writerows(rows)
    time_elapsed = time.time() - start_time

    total = len(rows)
    pixel_identical = len([x for x in rows if x[3]])
    not_identical = total - pixel_identical
    example_failure = sorted([x[0] for x in rows if not x[3]])[0]

    print("        Progress Tracker\n")
    print("            DIFFERENT      SAME    ")
    print("          |-----------|-----------|")
    print("          |    {: >3.0f}%   |    {: >3.0f}%   | 100%".format(not_identical/total*100, pixel_identical/total*100))
    print("          |-----------|-----------|")
    print("          |    {: >3d}    |    {: >3d}    | {: >3d}".format(not_identical, pixel_identical, total))
    print("          |-----------|-----------|")
    print()
    print("Time: {:.0f}s".format(time_elapsed))
    print("Time per file: {:.2f}s".format(time_elapsed/total))
    print("Next failure: {}".format(example_failure))

    os.system("rm -r /tmp/puppeteer_dev_chrome_profile-X*")
