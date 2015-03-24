import os
import sys
import pwiki.err as err

def add_path(path, check_existence=True):
    if check_existence and not os.path.isdir(os.path.abspath(path)):
        raise err.FileError('Not a directory: %s' % path)
    sys.path.append(os.path.abspath(path))

def find_dump():
    for path in ('dump.xml.bz2', 'dump.xml'):
        if os.path.exists(path):
            return path
    for path in os.listdir():
        if path.lower().startswith('dump') and path.lower().split('.bz2')[0].endswith('.xml'):
            return path
    raise err.FileError('Could not find dump')

def printf(s, *args):
    sys.stdout.write(s % args)
    sys.stdout.flush()
