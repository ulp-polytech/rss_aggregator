import feedparser
from lxml import etree

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

            yield entry
            item_count += 1

def write_feed(generator, output_file):
    with open(output_file, "wb") as f, etree.xmlfile(f) as xf:
        with xf.element("rss", version="2.0"):
            with xf.element("channel"):
                for entry in generator:
                    with xf.element("item"):
                        xf.write(etree.Element("title",
                            text=entry.title))
                        xf.write(etree.Element("link",
                            text=entry.link))
                        xf.write(etree.Element("description",
                            text=entry.description))

urls = generate_urls("sources.txt")
feed = generate_feed(urls)
write_feed(feed, "rss.xml")

