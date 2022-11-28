# -*- coding: utf-8 -*-
# @Date    : 2015-07-28 20:38:38
# @Author  : Weizhong Tu (mail@tuweizhong.com)
# @Link    : http://www.tuweizhong.com

'''
create some records for demo database
'''

from app.models import Case,CaseType, Customer,CustomerType


def main():
    columns_urls = [
      ('体育新闻', 'sports'),
      ('社会新闻', 'society'),
      ('科技新闻', 'tech'),
    ]

    for column_name, url in columns_urls:
        c = CaseType.objects.get_or_create(name=column_name, slug=url)[0]
        # 创建 10 篇新闻
        for i in range(1, 11):
            article = Case.objects.get_or_create(
                title='{}_{}'.format(column_name, i),
                slug='case_{}'.format(i),
                content='新闻详细内容： {} {}'.format(column_name, i),
            )[0]
            article.column.add(c)


if __name__ == '__main__':
    main()
    print("Done!")