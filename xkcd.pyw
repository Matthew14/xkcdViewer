import urllib, re, wx, cStringIO, random, webbrowser
from bs4 import BeautifulSoup

class myFrame(wx.Frame):
   def __init__(self, parent, id):
      self.image = None
      self.noComics = self.currentComic = self.getNocomics()
      wx.Frame.__init__(self, parent, id, 'XKCD', size = (800, 600))
      self.UIinit()
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

   def UIinit(self):
      self.panel = wx.Panel(self)
      self.CreateStatusBar()
      self.MenuInit()
      self.ToolInit()

   def MenuInit(self):
      self.MenuBar = wx.MenuBar()

      viewMenu = wx.Menu()
      viewAltText = viewMenu.Append(wx.NewId(), '&View Alt Text\tCtrl+T', 'View the Hover Text')
      gotoSite = viewMenu.Append(wx.NewId(), '&View on Website\tCtrl+O', 'View the Comic on xkcd.com')

      toolsMenu = wx.Menu()
      randomize = toolsMenu.Append(wx.NewId(), '&Random Comic\tCtrl+R', 'View a Random Comic')
      previous = toolsMenu.Append(wx.NewId(), '&Previous Comic\tCtrl+P', 'Go to Previous Comic')
      next = toolsMenu.Append(wx.NewId(), '&Next Comic\tCtrl+N', 'Go to Next Comic')

      self.MenuBar.Append(viewMenu, '&View')
      self.MenuBar.Append(toolsMenu, '&Tools')

      self.Bind(wx.EVT_MENU, self.showAltText, viewAltText)
      self.Bind(wx.EVT_MENU, self.gotoSite, gotoSite)
      self.Bind(wx.EVT_MENU, self.randomize, randomize)
      self.Bind(wx.EVT_MENU, self.prev, previous)
      self.Bind(wx.EVT_MENU, self.next, next)

      self.SetMenuBar(self.MenuBar)

   def ToolInit(self):
      self.tool = self.CreateToolBar()

      self.numberCtrl = wx.TextCtrl(self.tool, -1, "")
      self.tool.AddControl(self.numberCtrl)
      self.numberCtrl.SetValue(str(self.currentComic))

      self.numberCtrlButton = wx.Button(self.tool, label = 'Go!', pos=(740, 22), size=(60, 22))
      self.tool.AddControl(self.numberCtrlButton)
      self.Bind(wx.EVT_BUTTON, self.GoToComicButton, self.numberCtrlButton)
      self.Bind(wx.EVT_TEXT_ENTER, self.GoToComicButton, self.numberCtrl)

      self.tool.Realize()

   def showAltText(self, event):
      wx.MessageBox(self.hoverText, self.title, wx.OK | wx.ICON_INFORMATION)

   def gotoSite(self, event):
      webbrowser.open(self.url + str(self.currentComic))

   def GoToComicButton(self, event):
      self.GoToComic(int(self.numberCtrl.GetValue()))

   def randomize(self, event):
      self.GoToComic(random.randint(1, self.noComics))

   def prev(self, event):
      if self.currentComic != 1:
         self.GoToComic(self.currentComic - 1)

   def next(self, event):
      if self.currentComic != self.noComics:
         self.GoToComic(self.currentComic + 1)

   def GoToComic(self, number):
      url = "http://www.xkcd.com/" + str(number)
      self.numberCtrl.SetValue(str(number))
      try:
         content = urllib.urlopen(url).read()

      except Exception:
         print ("Cannot retrieve data. Internet working?")
         exit(1)

      soup = BeautifulSoup(content)
      img = soup.find('img', src=re.compile("\/comics\/")) #only the comics are stored in the comics directory

      self.hoverText = str(img['title'])

      self.title = str(soup.find('div', id='ctitle').string) #.string is the text in the tags
      self.SetTitle(self.title)

      print (img['src'])
      imgHandle = urllib.urlopen(img['src'])

      self.currentComic = int(str(soup.find('a', rel="prev")['href']).strip('/')) + 1
      self.DisplayImage(imgHandle)

   def DisplayImage(self, imgHandle):
      if self.image != None:
      	self.image.Destroy()
      with open("tmpImage.png", "wb") as img:
         img.write(imgHandle.read())
      comic = 'tmpImage.png'
      comic  = wx.Image(str(comic), wx.BITMAP_TYPE_ANY )
      comic = comic.ConvertToBitmap()
      self.image = wx.StaticBitmap(self, -1, comic, (0, 40), (comic.GetWidth(), comic.GetHeight()))

if __name__ == '__main__':
   app = wx.PySimpleApp()
   frame = myFrame(parent = None, id = -1)
   frame.Show()
   app.MainLoop()