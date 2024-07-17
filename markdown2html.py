import markdown2
from bs4 import BeautifulSoup

def post_process(soup):
    pass

def markdown2html(html):
    html = markdown2.markdown(html, extras=['tables', 'header-ids', 'fenced-code-blocks'])
    return html
    soup = BeautifulSoup(html, 'html.parser')
    soup = post_process(soup)
    return soup.prettify()
