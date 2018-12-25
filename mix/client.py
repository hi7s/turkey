import codecs
import itertools
import os


def get_lines(_n):
    _f = codecs.open('%s/src/%s' % (os.getcwd(), _n), 'r', 'utf-8')
    _result = [_ln.strip() for _ln in _f.readlines()]
    _f.close()
    return _result


if __name__ == '__main__':
    items = itertools.product(
        get_lines('a'),
        get_lines('b'),
        get_lines('c'),
    )
    f = codecs.open('client.py.out', 'w', 'utf-8')
    for item in items:
        ln = '\t'.join(item)
        print(ln)
        f.write(ln + '\n')
    f.close()
