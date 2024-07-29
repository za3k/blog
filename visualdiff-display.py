"""
Display top problems
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


def sort_order(x):
    return [
        x["pixel-perfect?"] == "False",
        int(x["height-difference"]),
        int(x["pixels-different"]),
        x["post-id"],
    ]

def open_webpage(url):
    subprocess.run(["chromium", url])

if __name__ == "__main__":
    with open("visual-diff.csv", "r") as _csv:
        csvfile = csv.DictReader(_csv, dialect="excel")
        #csvfile.writerow(["post-id", "url", "local-url", "pixel-perfect?", "html-screenshot", "markdown-screenshot", "diff-screenshot", "height-difference", "pixels-different"])
        rows = list(csvfile)

    ordered = sorted(rows, key=sort_order, reverse=True)
    ordered = [x for x in ordered if x["pixel-perfect?"] == "False"]
    #for x in ordered[:10]:
    #    print(x["post-id"], x["height-difference"], x["pixels-different"], x["pixel-perfect?"])
    for x in ordered:#[:30]:
        print(x["local-url"])
        open_webpage(x["local-url"])
