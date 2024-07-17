"""
A python wrapper around html2markdown.js, which converts posts-html/ to posts-md/
"""
import frontmatter
import subprocess
from pathlib import Path

CMD=["node", "html2markdown.js"]

class Post():
    def __init__(self, path):
        self.stem = path.stem
        self.data = frontmatter.load(path)

    @staticmethod
    def html2markdown(html):
        result = subprocess.run(CMD, input=html.encode("utf8"), capture_output=True)
        try:
            result.check_returncode()
        except subprocess.CalledProcessError:
            print(result.stdout.decode('utf8'))
            print(result.stderr.decode('utf8'))
            raise
        return result.stdout.decode("utf8")

    def convert(self):
        self.data["content"] = self.html2markdown(self.data["content"].split("<!-- comments -->")[0])

    def save(self, target_dir):
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / (self.stem + ".md")
        frontmatter.save(target_path, self.data)

class Converter():
    def __init__(self, from_, to):
        self.from_ = from_
        self.to = to

    def posts(self):
        for post in Path(self.from_).iterdir():
            yield Post(post)

    def convert_all(self):
        for post in self.posts():
            post.convert()
            post.save(Path(self.to))

if __name__ == "__main__":
    converter = Converter("posts-html", "posts-md")
    converter.convert_all()
