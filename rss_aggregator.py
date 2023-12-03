import feedparser
from lxml import etree

keywords = ["power", "energy", "havesting", "supply", "converter"]

def generate_urls(input_file):
    with open(input_file, 'r') as file:
        for url in file:
            yield url.strip()

def generate_feed(urls, max_items=1000):
    item_count = 0
    for url in urls:
        if item_count >= max_items:
            break

        feed = feedparser.parse(url)
        for entry in feed.entries:
            if item_count >= max_items:
                return

            if any(x in entry.description for x in keywords):
                yield entry
                item_count += 1

def write_feed(generator, output_file):
    with open(output_file, "wb") as f, etree.xmlfile(f) as xf:
        with xf.element("rss", version="2.0"):
            with xf.element("channel"):
                for entry in generator:
                    with xf.element("item"):
                        title = etree.Element("title")
                        title.text = entry.title
                        xf.write(title)

                        link = etree.Element("link")
                        link.text = entry.link
                        xf.write(link)

                        description = etree.Element("description")
                        description.text = entry.description
                        xf.write(description)

urls = generate_urls("sources.txt")
feed = generate_feed(urls)
write_feed(feed, "rss.xml")

