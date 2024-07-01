import frontmatter
import yaml
import chevron as mustache
from pathlib import Path
from collections import ChainMap
import os.path

class PseudoMap():
    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError()
    def __setitem__(self, key, value):
        setattr(self, key, value)

# I have verified wordpress slugs match this format too
allowable="abcdefghijklmnopqrstuvwxyz0123456789-" 
def url_slug(title):
    title = title.lower().replace(" ", "-")
    title = "".join(x for x in title if x in allowable)
    return title

class Templatable(PseudoMap):
    def __init__(self, blog):
        self.blog = blog
    
    @property
    def type(self):
        return str(self.__class__.__name__).lower()

    @property
    def output_path(self):
        output_path_template = self.blog["{}_destination".format(self.type)]
        return Path(mustache.render(output_path_template, self.context))

    @property
    def template_path(self):
        return self.blog["{}_template".format(self.type)]

    def content(self):
        with open(self.template_path, "r") as f:
            template = f.read()
        return mustache.render(template, self.context).encode("utf8")

    def output(self):
        output = self.content()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "wb") as f:
            f.write(output)

    @property
    def context(self):
        return ChainMap(self, self.blog)

class Static(Templatable):
    def __init__(self, path, blog):
        super().__init__(blog)
        self.path = path
    def content(self):
        with open(self.path, "rb") as f:
            return f.read()
    @property
    def relative_path(self):
        return self.path.relative_to(self.blog.static_dir)

class Post(Templatable):
    def __init__(self, parsed, blog):
        super().__init__(blog)
        self.post, self.comments = parsed.pop("content").split("<!-- comments -->\n")
        for k, v in parsed.items():
            self[k] = v
    @property
    def id(self):
        if hasattr(self, "wordpress_slug"): return self.wordpress_slug
        if hasattr(self, "slug"): return self.slug
        return utrl_slug(self.title)

class Tag(Templatable):
    def __init__(self, tag, blog):
        super().__init__(blog)
        self.tag = tag
    def __hash__(self):
        return hash(self.tag)
class Category(Tag):
    pass
class Page(Templatable):
    pass
class Image(Templatable):
    pass

class Blog(PseudoMap):
    def __init__(self, config="config.yaml"):
        self.tags = set()
        self.categories = set()
        self.posts = []

        self.load_config(config)
        self.load_posts()

    def load_config(self, path):
        with open(path) as f:
            config = yaml.safe_load(f)

        for k in {"source", "destination"}:
            self[k] = os.path.expanduser(config.pop(k))
        for k, v in config.items():
            if k.endswith("_dir") or k.endswith("_template"):
                v = os.path.join(self.source, os.path.expanduser(v))
            self[k] = v

    def load_posts(self):
        for post_input_path in Path(self.post_dir).iterdir():
            self.add_post(Post(frontmatter.load(post_input_path), self))

    def add_post(self, post):
        self.posts.append(post)
        for tag in post.tags:
            self.tags.add(Tag(tag, self))
        for category in post.categories:
            self.categories.add(Category(category, self))

    @property
    def images(self):
        return [] # TODO
    @property
    def static(self):
        for dirpath, dirnames, filenames in Path(self.static_dir).walk():
            for name in filenames:
                path = dirpath / name
                yield Static(path, self)
    @property
    def pages(self):
        return [] # TODO

if __name__ == "__main__":
    blog = Blog()
    for image in blog.images:
        image.output()
    for static in blog.static:
        static.output()
    for post in blog.posts:
        post.output()
    for tag in blog.tags:
        tag.output()
    for category in blog.categories:
        category.output()
    for page in blog.pages:
        page.output()
