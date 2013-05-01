import urllib
import re
from bs4 import BeautifulSoup
class ComicViewer(object):
    def __init__(self):
        self.url = "http://www.xkcd.com/"
        self.comicName = 'xkcd'
        self.image = None
        self.noComics = self.currentComic = self.getNocomics()
        self.currentComicUrl = self.url + str(self.currentComic)
        self.GoToComic(self.currentComic)

    def getNocomics(self):
      self.url = "http://www.xkcd.com/"
      try:
         content = urllib.urlopen(self.url).read()
      except Exception:
         print ("Cannot retrieve data. Internet working?")
         exit(1)
      soup = BeautifulSoup(content)
      return int(str(soup.find('a', rel="prev")['href']).strip('/')) + 1 #link to prev comic + 1

    def GoToComic(self, number):
      url = self.url + str(number)
      try:
         content = urllib.urlopen(url).read()
      except Exception:
         print ("Cannot retrieve data. Internet working?")
         exit(1)

      soup = BeautifulSoup(content)
      img = soup.find('img', src=re.compile("\/comics\/")) #only the comics are stored in the comics directory

      self.hoverText = str(img['title'])

      self.title = str(soup.find('div', id='ctitle').string) #.string is the text in the tags

      self.currentComic = int(str(soup.find('a', rel="prev")['href']).strip('/')) + 1
      self.currentComicUrl = self.url + str(self.currentComic)
      self.image = img['src']