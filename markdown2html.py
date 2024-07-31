import markdown2
from bs4 import BeautifulSoup, NavigableString, Tag


def post_process(soup):
    for img in soup.find_all("img"):
        figure = soup.new_tag("figure")
        figure['class'] = "wp-block-image"

        caption = None
        if img['alt'] == "": # No alt-text or caption
            del img['alt']
        elif img['alt'] and img['alt'].startswith('alt:'): # Alt-text
            img['alt'] = img['alt'].removeprefix('alt:')
        else: # Caption
            if img['alt'] and img['alt'].startswith('caption:'):
                img['alt'] = img['alt'].removeprefix('caption:')
            caption = img['alt']

        if img.parent.name == "a":
            img = img.parent
        img.wrap(figure)
        if caption is not None:
            captionE = soup.new_tag("figcaption")
            captionE.string = caption
            figure.append(captionE)


    for pre in soup.find_all("pre"):
        pre['class'] = "wp-block-code"

    for hr in soup.find_all("hr"):
        hr['class'] = "wp-block-separator"

    for table in soup.find_all("table"):
        figure = soup.new_tag("figure")
        figure['class'] = "wp-block-table"
        figure = table.wrap(figure)

        # Look for a figcaption
        n = figure.next_sibling
        while isinstance(n, NavigableString):
            n = n.next_sibling
        if isinstance(n, Tag) and n.name == "figcaption":
            n.extract()
            figure.append(n)

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

    return soup

def markdown2html(html):
    html = markdown2.markdown(html, extras=['tables', 'header-ids', 'fenced-code-blocks', 'markdown-in-html'])
    soup = BeautifulSoup(html, 'html.parser')
    soup = post_process(soup)
    return str(soup) #.prettify()
