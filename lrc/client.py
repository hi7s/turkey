import codecs
import os

p_path = 'D:\\a\\'
key = 205000
for i, fa in enumerate(os.listdir(p_path)):
    # read file
    f = codecs.open(p_path + fa, 'r', 'utf-8')
    lns = f.readlines()
    f.close()
    # format
    print('\n')
    # title
    title = '%02d. %s' % (i + 1, lns[2][4:-3])
    # print(title)
    # content
    cont = ''
    for ln in lns[6:]:
        tag_p = '<p>%s</p>' % ln[10:].strip()
        cont += tag_p
        # print(tag_p)
    key += 1
    print('insert into wp_post(id, title, content) value(%d, "%s", "%s");' % (key, title, cont.replace('"', "\\")))
