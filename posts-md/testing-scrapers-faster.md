---
author: admin
categories:
- Technical
date: 2021-08-16 19:28:16-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- iteration
- programming
- repl
title: Testing scrapers faster
updated: 2021-08-16 19:28:17-07:00
wordpress_id: 712
wordpress_slug: testing-scrapers-faster
---
Recently I wrote a scraper. First, I downloaded all the HTML files. Next, I wanted to parse the content. However, real world data is pretty messy. I would run the scraper, and it would get partway though the file and fail. Then I would improve it, and it would get further and fail. I’d improve it more, and it would finish the whole file, but fail on the fifth one. Then I’d re-run things, and it would fail on file #52, #1035, and #553,956.

To make testing faster, I added a scaffold. Whenever my parser hit an error, it would print the filename (for me, the tester) and record the filename to an error log. Then, it would immediately exit. When I re-ran the parser, it would test all the files where it had hit a problem **first**. That way, I didn’t have to wait 20 minutes until it got to the failure case.

```
if __name__ == "__main__":
    if os.path.exists("failures.log"):
        # Quicker failures 
        with open("failures.log", "r") as f:
            failures = set([x.strip() for x in f])
        for path in tqdm.tqdm(failures, desc="re-checking known tricky files"):
            try:
                with open(path) as input:
                    parse_file(input)
            except Exception:
                print(path, "failed again (already failed once")
                raise

    paths = []
    for root, dirs, files in os.walk("html"):
        for file in sorted(files):
            path = os.path.join(root, file)
            paths.append(path)
    paths.sort()

    with open("output.json", "w") as out:
        for path in tqdm.tqdm(paths, desc="parse files"): # tqdm is just a progress bar. you can also use 'for path in paths:
            with open(input, "r") as input:
                try:
                    result = parse_file(input)
                except Exception:
                    print(path, "failed, adding to quick-fail test list")
                    with open("failures.log", "a") as fatal:
                        print(path, file=fatal)
                    raise
                json.dump(result, out, sort_keys=True) # my desired output is one JSON dict per line
                out.write("\n")
```
