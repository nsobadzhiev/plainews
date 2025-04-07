from xml.etree import ElementTree
from xml.dom.minidom import parseString

from model.feed import Feed


def parse_opml(file_path: str):
    tree = ElementTree.parse(file_path)
    root = tree.getroot()

    if root.tag != 'opml':
        raise ValueError("This is not a valid OPML file.")

    rss_feeds = []
    for outline in root.findall(".//outline"):
        # Check if the 'outline' element has an 'xmlUrl' attribute (this holds the RSS feed URL)
        rss_url = outline.attrib.get('xmlUrl')
        if rss_url:
            rss_feeds.append(rss_url)
    return rss_feeds

def generate_opml(feeds: list[Feed]) -> str:
    opml = ElementTree.Element("opml", version="2.0")
    head = ElementTree.SubElement(opml, "head")
    title = ElementTree.SubElement(head, "title")
    title.text = "My RSS Feeds"
    body = ElementTree.SubElement(opml, "body")
    [ElementTree.SubElement(body, "outline", text=feed.title, xmlUrl=feed.url) for feed in feeds]
    xml_bytes = ElementTree.tostring(opml, encoding="utf-8", xml_declaration=True)
    xml_string = xml_bytes.decode("utf-8")
    # pretty print before returning
    return parseString(xml_string).toprettyxml()
