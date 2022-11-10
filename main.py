import html.parser
import os
from urllib.request import urlopen

import easygui

if __name__ == '__main__':
    dir = easygui.diropenbox('请选择下载目录')
    while True:
        id = easygui.enterbox('请输入乐乐课堂CID')
        pages = int(easygui.enterbox('请输入总页数'))
        filename = easygui.enterbox('请输入文件名')
        result = []
        for i in range(1, pages+1):
            url = f'http://www.leleketang.com/let3/knowledge_list.php?cid={id}&p={i}'

            class parser(html.parser.HTMLParser):
                tmp = ''
                getting = False
                result = []

                def handle_starttag(self, tag, attrs):
                    a = dict(attrs)
                    if 'class' in a:
                        if a['class'] == 'public-background-image knowledge_play_btn':
                            self.tmp = a['data-video']
                        elif a['class'] == 'knowledge_name ellipsis':
                            self.getting = True

                def handle_data(self, data) -> None:
                    if self.getting:
                        self.result.append((self.tmp, data))
                        self.getting = False
            p = parser()
            p.result = []
            u = urlopen(url).read().decode()
            p.feed(u)
            result += p.result
        with open(os.path.join(dir, filename+'.txt'), 'w', encoding='utf-8') as f:
            no = 1
            for i, j in result:
                print(i, file=f)
                print(f' out={no}.{j}.mp4', file=f)
                no += 1
