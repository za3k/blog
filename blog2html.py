import bs4
from datetime import datetime
import yaml

from pathlib import Path

INPUT_DIR = Path("/home/zachary/blog.za3k.com")
OUTPUT_DIR = Path("/home/zachary/blog_converter/posts")
IMAGES = OUTPUT_DIR / 'images'

BLACKLIST={"wp-json", "feed"}
def posts():
    for possible_post in INPUT_DIR.iterdir():
        if possible_post.is_dir() and possible_post.name not in BLACKLIST:
            possible_post /= "index.html"
            if possible_post.is_file():
                yield possible_post

def parse_date(s):
    # 2023-07-17T13:58:49-07:00
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")
        
def scrape_post(post):
    html = bs4.BeautifulSoup(post, 'html.parser')
    article = html.find('article')
    comments = html.find('ol', id="commentlist")

    result = {}
    result["html_content"] = str(article)
    result["html_comments"] = (str(comments) if comments else "")
    result["title"] = article.find('h1', class_="entry-title").get_text()
    assert result["title"] == html.find('title').get_text()
    result["date"] = parse_date(html.find('time', class_="published")['datetime'])
    if updated := html.find('time', class_="updated"):
        result["updated"] = parse_date(updated['datetime'])
    result["wordpress_id"] = int(article['id'].removeprefix("post-"))
    result["categories"] = [link.get_text() for link in article.select(".bl_categ a[rel=tag]")]
    result["tags"] = [link.get_text() for link in article.select(".bl_posted a[rel=tag]")]
    result["source"] = "wordpress"
    result["author"] = article.find(rel="author").get_text()
    result["markup"] = "html"

    return result

def output_post(post):
    content = "<!-- blogpost -->\n" + post.pop("html_content") + "\n\n<!-- comments -->\n" + post.pop("html_comments")
    front_matter = yaml.dump(post)
    return "---\n{front_matter}---\n{content}".format(content=content, front_matter=front_matter)

import sys
if __name__ == "__main__":
    for post_path in posts():
        slug = post_path.parts[-2] 
        output_path = OUTPUT_DIR / (slug + ".html")
        with open(post_path, "r") as f:
            post = f.read()
        parse = scrape_post(post)
        parse["wordpress_slug"] = slug
        output = output_post(parse)
        with open(output_path, "w") as f:
            f.write(output)

