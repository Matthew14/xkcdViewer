import wx
import urllib
import random
import webbrowser
import os
from comicViewer import ComicViewer

class viewerFrame(wx.Frame):
   def __init__(self, parent, id):
      self.image = None
      self.comicViewer = ComicViewer()
      wx.Frame.__init__(self, parent, id, self.comicViewer.comicName, size = (800, 600))
      self.UIinit()
      self.numberCtrl.SetValue(str(self.comicViewer.currentComic))
      self.SetTitle(self.comicViewer.title)
      self.DisplayImage()
      self.Bind(wx.EVT_CHAR_HOOK, self.onKey)

   def onKey(self, event):
      key = event.GetKeyCode()
      if key == wx.WXK_LEFT:
         self.prev(event)
      elif key == wx.WXK_RIGHT:
         self.next(event)

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
      self.numberCtrl.SetValue(str(self.comicViewer.currentComic))

      self.numberCtrlButton = wx.Button(self.tool, label = 'Go!', pos=(740, 22), size=(60, 22))
      self.tool.AddControl(self.numberCtrlButton)
      self.Bind(wx.EVT_BUTTON, self.GoToComicButton, self.numberCtrlButton)
      self.Bind(wx.EVT_TEXT_ENTER, self.GoToComicButton, self.numberCtrl)

      self.tool.Realize()

   def showAltText(self, event):
      wx.MessageBox(self.comicViewer.hoverText, self.comicViewer.title, wx.OK | wx.ICON_INFORMATION)

   def gotoSite(self, event):
      webbrowser.open(self.comicViewer.currentComicUrl)

   def randomize(self, event):
      self.comicViewer.GoToComic(random.randint(1, self.comicViewer.noComics))
      self.DisplayImage()

   def prev(self, event):
      if self.comicViewer.currentComic != 1:
         self.comicViewer.GoToComic(self.comicViewer.currentComic - 1)
         self.DisplayImage()

   def next(self, event):
      if self.comicViewer.currentComic != self.comicViewer.noComics:
         self.comicViewer.GoToComic(self.comicViewer.currentComic + 1)
         self.DisplayImage()

   def GoToComicButton(self, event):
      try:
         comicNo  = int(self.numberCtrl.GetValue())
         self.GoToComic(comicNo)
         self.numberCtrl.SetValue(str(self.comicViewer.currentComic))
         self.SetTitle(self.comicViewer.title)
         self.DisplayImage(self.comicViewer.image)
      except ValueError as e:
         pass

   def DisplayImage(self):
      imgHandle = urllib.urlopen(self.comicViewer.image)
      if self.image != None:
         self.image.Destroy()
      with open("tmpImage.png", "wb") as img:
         img.write(imgHandle.read())
      comic = 'tmpImage.png'
      comic  = wx.Image(str(comic), wx.BITMAP_TYPE_ANY )
      comic = comic.ConvertToBitmap()
      self.image = wx.StaticBitmap(self.panel, -1, comic, (0, 40), (comic.GetWidth(), comic.GetHeight()))
      self.numberCtrl.SetValue(str(self.comicViewer.currentComic))
      self.SetTitle(self.comicViewer.title)
      os.remove('tmpImage.png')

if __name__ == '__main__':
   app = wx.PySimpleApp()
   frame = viewerFrame(parent = None, id = -1)
   frame.Show()
   app.MainLoop()