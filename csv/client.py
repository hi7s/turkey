import codecs


def get_comps():
    f = codecs.open('client.py.in', 'r', 'utf-8')
    result = [ln.strip() for ln in f.readlines()]
    f.close()
    return result


def convert(src):
    f = codecs.open('client.py.out', 'w', 'utf-8')
    for i in range(0, len(src)):
        s = '{},1581108{}00'.format(src[i], i + 10)
        f.write(s + '\n')
        print(s)
    f.close()


if __name__ == '__main__':
    comps = get_comps()
    convert(comps)
