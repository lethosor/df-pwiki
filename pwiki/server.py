import bottle
from bottle import route

import pwiki.parser

db = None
parser = None

@route('/page/<page>')
def callback(page):
    if page not in db.pages:
        bottle.abort(404, 'Page not found')
    page = db.pages[page]
    yield '<html><head><title>%s</title></head><body>' % page.title
    try:
        yield page.render(parser).encode('utf-8')
    except pwiki.parser.ParserError as e:
        yield '<h2 class="error">Parser error: %s</h2>' % e
    yield '</body></html>'

def main(host, port, database, _parser):
    global db, parser
    db = database
    parser = _parser
    app = bottle.app()
    app.run(host=host, port=port, debug=True)
