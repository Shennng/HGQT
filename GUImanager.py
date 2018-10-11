import frame

class Manager():
    
    def __init__(self,UpdateUI):
        self.UpdateUI = UpdateUI
        self.frameDict = {} # 用来装载已经创建的Frame对象
        
    def GetFrame(self,number):
        frame = self.frameDict.get(number)
        
        if frame:
            pass
        else:
            frame = self.CreateFrame(number)
            self.frameDict[number] = frame
            
        return frame
        
    def CreateFrame(self,number):
        if number == 0:
            return frame.MainFrame(id=number, size=(1035, 620), UpdateUI=self.UpdateUI)
        elif number == 1:
            return frame.TipsFrame(id=number, size=(750, 400), UpdateUI=self.UpdateUI)
            #* pos=(wx.DisplaySize()[0]/2, wx.DisplaySize()[1]/2
        elif number == 2:
            return frame.HelpFrame(id=number, size=(750, 400), UpdateUI=self.UpdateUI)
