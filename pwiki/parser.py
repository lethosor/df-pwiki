import HTMLParser
import re

class ParserError(Exception): pass

class Parser(object):
    tag_blacklist = ('script', 'html', 'head', 'title', 'body', 'style')
    link_pattern = re.compile(r'\[\[([^|\]])+(\|([^\]]))?\]\]')
    def __init__(self):
        self.htmlparser = HTMLParser.HTMLParser()

    @staticmethod
    def replace_links(*args):
        for a in args:
            print(a.groups())

    def parse_links(self, wikitext):
        return self.link_pattern.sub(self.replace_links, wikitext)

    def render_html(self, wikitext):
        html = self.htmlparser.unescape(wikitext)
        for tag in self.tag_blacklist:
            if '<' + tag in html or '</' + tag in html:
                raise ParserError('Unsafe tag: %s' % tag)
        lines = html.split('\n')
        for line in lines:
            line = self.parse_links(line)
        html = '\n'.join(lines)
        return html
