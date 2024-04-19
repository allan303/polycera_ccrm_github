from bs4 import BeautifulSoup
from app.models.post.models import PostOrm
from mongoengine import connect, disconnect
disconnect()
connect('polycera_ccrm')
qs = PostOrm.objects.order_by('-create_time').first()
s = qs.soup


def deal_bs4_li(soup: BeautifulSoup, ls: list):
    if not hasattr(soup, 'contents'):
        ls.append(soup)
    else:
        contents = list(soup.contents)
        if contents:
            for c in contents:
                deal_bs4_li(soup=c, ls=ls)


ls = []
deal_bs4_li(soup=s, ls=ls)
ls
