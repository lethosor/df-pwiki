""" Dwarf Fortress portable wiki """
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pwiki.util as util
util.add_path('depends/bottle')

import pwiki.database as database
import pwiki.parser as parser
import pwiki.server as server

def main():
    util.printf('Loading database... ')
    db = database.Database(util.find_dump())
    util.printf('Done (%i pages)\n', len(db.pages))
    server.main('localhost', 8025, db, parser.Parser())

if __name__ == '__main__':
    main()
