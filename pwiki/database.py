import bz2
import sys

try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

def get_tag_contents(xml, tag):
    start = xml.find('<%s' % tag)
    if start < 0:
        raise ValueError('Tag %s not found' % tag)
    start = xml.find('>', start) + 1
    if xml[start - 2:start] == '/>':
        return ''
    end = xml.find('</%s>' % tag, start)
    if end < 0:
        raise ValueError('Unclosed tag: %s' % tag)
    return xml[start:end]

class Page(object):
    def __init__(self, xml):
        self.title = get_tag_contents(xml, 'title')
        self.contents = get_tag_contents(xml, 'text')
        self.rendered = None

    def render(self, parser):
        if self.rendered is None:
            self.rendered = parser.render_html(self.contents)
        return self.rendered

    def purge(self):
        self.rendered = None

class Database(object):
    def __init__(self, path):
        self.pages = {}
        self.namespaces = {}
        buffer = StringIO()
        compressed = False
        with open(path, 'rb') as f:
            if f.read(2) == b'BZ':
                compressed = True
        if compressed:
            f = bz2.BZ2File(path, 'r')
        else:
            f = open(path, 'rb')
        while True:
            chunk = f.read(4096)
            buffer.write(chunk)
            if len(chunk) < 4096:
                break
        contents = buffer.getvalue()
        start = 0
        while contents.find('<page>', start) != -1:
            start = contents.find('<page>', start)
            end = contents.find('</page>', start) + len('</page>')
            if end == -1:
                raise ValueError('Unclosed <page> tag in %s' % path)
            page = Page(contents[start:end])
            self.pages[page.title] = page
            start = end
