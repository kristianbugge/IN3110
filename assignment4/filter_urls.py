import re
from urllib.parse import urljoin
from requesting_urls import get_html

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)
    regex = r"<a.*href=[\"](.*?)(?:[\"]|[#])"
    urls = set()
    comp = re.compile(regex)

    for url in comp.findall(html):
        if url != "":
            if url[1] == "/":
                url = "https:" + url
                print(url)
            elif url[0] == "/" and base_url:
                url = base_url + url
                print(url)

            urls.add(url)
    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        out = open(output, "w")

        for url in urls:
            out.write(url + '\n')
        out.close()

    return urls


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)

    comp1 = re.compile(r".*wikipedia.org.*")
    comp2 = re.compile(r".*([\/]wiki.*)")

    articles = set()

    for url in urls:
        if len(comp1.findall(url)) != 0:
            articles.add(comp1.findall(url)[0])
        elif len(comp2.findall(url)) != 0:
            articles.add("https://wikipedia.org" + comp2.findall(url)[0])
    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        out = open(output, "w")
        for urls in articles:
            out.write(url + '\n')
        out.close()

    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
if __name__=='__main__':
    article1 = "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup"
    article2 = "https://en.wikipedia.org/wiki/Bundesliga"
    find_urls(article1)
    find_urls(article2)
