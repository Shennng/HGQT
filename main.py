import wx

from GUImanager import Manager

class MainApp(wx.App):
    
    def OnInit(self):
        self.guimanager = Manager(self.UpdateUI)
        self.frame = self.guimanager.GetFrame(number=0)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def UpdateUI(self,number):
        self.frame = self.guimanager.GetFrame(number)
        self.frame.Show(True)
        
def main():
    app = MainApp()
    app.MainLoop()
        
if __name__ == '__main__':
    main()
