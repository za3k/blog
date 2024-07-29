import markdown2
from bs4 import BeautifulSoup


def post_process(soup):
    for img in soup.find_all("img"):
        figure = soup.new_tag("figure")
        figure['class'] = "wp-block-image"
        img.wrap(figure)

    for pre in soup.find_all("pre"):
        pre['class'] = "wp-block-code"

    for hr in soup.find_all("hr"):
        hr['class'] = "wp-block-separator"

    for table in soup.find_all("table"):
        figure = soup.new_tag("figure")
        figure['class'] = "wp-block-table"
        table.wrap(figure)

    for video in soup.find_all("video"):
        figure = soup.new_tag("figure")
        figure['class'] = "wp-block-video"
        video.wrap(figure)

    # YT embeds
    for iframe in soup.find_all("iframe"):
        if 'youtube.com' in iframe['src']:
            figure = soup.new_tag("figure")
            figure['class'] = "wp-block-embed"
            iframe.wrap(figure)
            
    # <figure> inside <p> is illegal
    for figure in soup.find_all("figure"):
        parent = figure.parent
        while parent.name in ["a"]:
            parent = parent.parent
        if parent.name == "p" and len(list(parent.children)) == 1:
            parent.unwrap()

    #for p in soup.select("blockquote > p"):
    #    if len(p.find_previous_siblings("p")) > 0: continue
    #    p['style'] = "color:#222222;"
    #for p in soup.select("li > p"):
    #    p.unwrap()
    return soup

def markdown2html(html):
    html = markdown2.markdown(html, extras=['tables', 'header-ids', 'fenced-code-blocks'])
    soup = BeautifulSoup(html, 'html.parser')
    soup = post_process(soup)
    return str(soup) #.prettify()
