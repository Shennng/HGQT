import wx
import wx.lib.buttons as wxbutton
import _thread as thread
from operator import itemgetter

from analysis import parser_data
from orignal_data import get_code_in_file

class MainFrame(wx.Frame):
    
    def __init__(
            self, parent=None, id=-1, title='HNUST教务网成绩查询小工具  by:王S  微信公众号:Wang的胜宴  来关注 一起学习吧 ~',size=wx.DefaultSize,
            style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.RESIZE_BORDER), UpdateUI=None
    ):
        wx.Frame.__init__(self, parent, id, title=title, size=size, style=style)
        
        self.data = []  #数据初始化
        self.UpdateUI = UpdateUI
        
        '通过 .SetFont(self.font)设置字体'
        # wx.Font(pointSize,family,style,weight,underline,faceName,encoding)
        self.font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'SimHei')
        
        self.InitUI()  #绘制UI界面
        self.Center()
        
    def InitUI(self):
        #绘制面板
        self.panel = wx.Panel(self)
        #软件图标
        self.Software_Icon()
        #文本控件集
        self.Textctrl()
        #成绩列表框
        self.Grades_List()
        #按钮集
        self.Buttons()
        #控件容器
        self.Boxsizer()
        #程序事件处理
        self.Event_deal()
        
    def Software_Icon(self):
        '设置图标'
        icon = wx.Icon('icon/hnust(black).ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)   
        
    def Choice_Listbox(self):
        '选择框控件初始化'
        self.list1 = ['', '2018-2019-1', '2017-2018-2', '2017-2018-1', '2016-2017-2','2016-2017-1', '2016-2015-2', '2016-2015-1', '2015-2014-2', '2015-2014-1']  #可选项
        self.listbox = wx.Choice(self.panel, -1, choices=self.list1)
        self.listbox.SetSelection(0)  #初选项
        self.listbox.SetString(0, '全部成绩')  #给指定项设置标签
    
    def Comment(self):  #注释静态文本
        #self.s_text = wx.StaticText(self.panel, label='*输入学号后按回车也\n 可以获取验证码哦~')
        #self.s_text1 = wx.StaticText(self.panel, label='*教务网密码输入框')
        #self.s_text2 = wx.StaticText(self.panel, label='*选择空白为查询全部成绩', pos=(250,38))
        #self.s_text3 = wx.StaticText(self.panel, label='*刷新验证码の基础招式', pos=(380,43))
        pass
        
    def Textctrl(self):
        '文本控件初始化'
        #学号输入框
        self.text = wx.TextCtrl(self.panel,value='请输入学号...', style=wx.TE_PROCESS_ENTER)
        self.text.SetForegroundColour('#888888')
        #密码输入框
        self.text1 = wx.TextCtrl(self.panel,value='password', style=wx.TE_PASSWORD)
        self.text1.SetForegroundColour('#888888')
        #学段选择框
        self.Choice_Listbox()
        #self.text2 = wx.TextCtrl(self.panel, value='2017-2018-2')
        #self.text2.SetForegroundColour('#888888')
        #注释提示
        self.Comment()
        #验证码输入框
        self.code_text = wx.TextCtrl(self.panel,value='请输入验证码...', style=wx.TE_PROCESS_ENTER)
        self.code_text.SetForegroundColour('#888888')
        
    def Grades_List(self):
        '列表控件初始化'
        self.list = wx.ListCtrl(self.panel, id=-1, pos=(10,75), size=(999,500), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)  # , size=(895,500), 
        self.list.SetFont(self.font)  #设置列表内容的字体为简黑
        self.CreateHeader()  #创建列表标签
        self.list.InsertItem(0, "请填充信息。")  #初始化列表内容为‘请填充信息.’  
        
    def CreateHeader(self):
        '列表标签设定'
        self.list.InsertColumn(0, "学号", format=wx.LIST_FORMAT_LEFT, width=90)
        self.list.InsertColumn(1, "姓名", format=wx.LIST_FORMAT_CENTER, width=60)
        self.list.InsertColumn(2, "开课学期", format=wx.LIST_FORMAT_CENTER, width=100)
        self.list.InsertColumn(3, "课程名称", format=wx.LIST_FORMAT_LEFT, width=230)
        self.list.InsertColumn(4, "总成绩", format=wx.LIST_FORMAT_CENTER, width=50)
        self.list.InsertColumn(5, "课程性质", format=wx.LIST_FORMAT_CENTER, width=100)
        self.list.InsertColumn(6, "课程类别", format=wx.LIST_FORMAT_CENTER, width=75)
        self.list.InsertColumn(7, "学时", format=wx.LIST_FORMAT_CENTER, width=50)
        self.list.InsertColumn(8, "学分", format=wx.LIST_FORMAT_CENTER, width=50)
        self.list.InsertColumn(9, "考试性质", format=wx.LIST_FORMAT_CENTER, width=75)
        self.list.InsertColumn(10, "补重学期", format=wx.LIST_FORMAT_CENTER, width=100)
     
    def Buttons(self):
        '按钮控件初始化'
        self.button = wxbutton.GenButton(self.panel, -1, '查询成绩')
        self.code_button = wxbutton.GenButton(self.panel, -1, '获取/刷新验证码')
        self.help_button = wxbutton.GenButton(self.panel, -1, '帮助')
        
    def Boxsizer(self):
        '容器设定'
        box = wx.BoxSizer(wx.HORIZONTAL) #放置水平的box sizer
        box.Add(self.text, 0, wx.ALL | wx.FIXED_MINSIZE, 10) #水平方向伸展时不改变尺寸
        box.Add(self.text1, 0, wx.ALL | wx.FIXED_MINSIZE, 10)
        #box.Add(self.text2, 0, wx.ALL, 10)
        box.Add(self.code_button, 0, wx.ALL | wx.FIXED_MINSIZE, 10)
        box.Add(self.code_text, 0, wx.ALL | wx.FIXED_MINSIZE, 10)
        box.Add(self.listbox, 0, wx.ALL | wx.FIXED_MINSIZE, 10)
        box.Add(self.button, 0, wx.ALL | wx.FIXED_MINSIZE, 10)
        box.Add(self.help_button, 0, wx.ALL | wx.FIXED_MINSIZE, 10)
        self.panel.SetSizerAndFit(box)
        
    def Event_deal(self):
        '程序事件处理'
        self.Bind(wx.EVT_BUTTON, self.Fresh_Code, self.code_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.Fresh_Code, self.text)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.button)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnRefresh, self.code_text)
        self.Bind(wx.EVT_TEXT, self.modify_colour, self.text)
        self.Bind(wx.EVT_TEXT, self.modify_colour, self.text1)
        #self.Bind(wx.EVT_TEXT, self.modify_colour, self.text2)
        self.Bind(wx.EVT_TEXT, self.modify_colour, self.code_text)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Help, self.help_button)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.sort_by_column, self.list)  #左键单击某列标题，正序重排列表
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.sort_by_column_reversed, self.list)  #右键单击某列标题，逆序重排列表
    
    def modify_colour(self, event):
        '文本框有输入时改变其文本颜色'
        event.GetEventObject().SetForegroundColour('#2F4F4F')
        
    def Fresh_Code(self, event):
        '刷新验证码'
        self.cookies = get_code_in_file()
        self.image_show()
        #self.bmp.SetBitmap(wx.Bitmap(wx.Image('code.jpg', wx.BITMAP_TYPE_JPEG)))

    def image_show(self):
        '验证码显示'
        image = wx.Image('code.jpg', wx.BITMAP_TYPE_JPEG)
        temp = image.ConvertToBitmap()
        #size = temp.GetWidth(), temp.GetHeight()
        self.bmp = wx.StaticBitmap(parent=self.panel, bitmap=temp, pos=(420,40))

    def OnRefresh(self,event):
        '多线程刷新列表'
        try:
            self.get_data()
        except:
            print("用户未登录，成绩无法获取！")
        if self.data:
            thread.start_new_thread(self.SetData,(0, ))
        else:
            self.OnClick()
            
    def get_data(self):
        '获取成绩数据'
        index = self.listbox.GetSelection()
        temp = [self.text.GetValue(), self.text1.GetValue(), self.list1[index]]
        verifycode_ = self.code_text.GetValue()
        self.data = parser_data(verifycode_, self.cookies, temp[0], temp[1], temp[-1])
        if self.data == []:
            self.OnClick()

    def SetData(self, pos):
        '将数据插入到列表，不同成绩段显示不同颜色'
        self.list.ClearAll()
        self.CreateHeader()
        for each in self.data:
            pos = self.list.InsertItem(pos+1,each[0])
            for i in range(1,11):
                self.list.SetItem(pos,i,each[i])
            grade = each[4]
            try:
                if int(grade) < 60:
                    self.list.SetItemBackgroundColour(pos, (255, 0, 0))  #挂科显示为红色
                elif int(grade) <= 61:
                    self.list.SetItemBackgroundColour(pos, (255, 99, 71))  #60到61为浅红
                elif int(grade) <= 74:
                    self.list.SetItemBackgroundColour(pos, (238, 221, 130))  #62到74为黄
                elif int(grade) <= 84:
                    self.list.SetItemBackgroundColour(pos, (152, 251, 152))  #75到84为浅绿
                elif int(grade) <= 100:
                    self.list.SetItemBackgroundColour(pos, (124, 252, 0))  #85到100为绿
            except:
                pass
                
            if grade == '不及格':
                self.list.SetItemBackgroundColour(pos, (255, 0, 0))  #挂科显示为红色
            elif grade == '及格' and each[3] != '军事技能训练':
                self.list.SetItemBackgroundColour(pos, (255, 99, 71))  #及格为浅红
            elif grade == '中':
                self.list.SetItemBackgroundColour(pos, (238, 221, 130))  #中为黄
            elif grade == '良' or each[3] == '军事技能训练':
                self.list.SetItemBackgroundColour(pos, (152, 251, 152))  #良为浅绿，军训特殊，大部分为及格，显示为浅绿
            elif grade == '优':
                self.list.SetItemBackgroundColour(pos, (124, 252, 0))  #优为绿
            
    def sort_by_column(self, listevent):
        '按指定标签正序排序列表'
        num = listevent.GetColumn()
        #with open('data.json', 'w') as f:
        #    f.write(json.dumps(self.data, ensure_ascii=False, indent=4, sort_keys=False))
        self.data = sorted(self.data, key=itemgetter(num))
        self.SetData(pos=0)
        
    def sort_by_column_reversed(self, listevent):
        '按指定标签逆序排序列表'
        num = listevent.GetColumn()
        self.data = sorted(self.data, key=itemgetter(num), reverse=True)
        self.SetData(pos=0)

    def OnClick(self):
        '切换到窗体TipsFrame'
        self.UpdateUI(1)

    def OnClick_Help(self, event):
        '切换到窗体HelpFrame'
        self.UpdateUI(2)
    

class TipsFrame(wx.Frame):
    
    def __init__(
        self, parent=None, id=0, title='来自王Sの温馨提示~', pos=wx.DefaultPosition,size=wx.DefaultSize, 
        style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER), UpdateUI=None
    ):
        wx.Frame.__init__(self, parent, id,title=title, size=size, pos=pos, style=style)
        
        self.UpdateUI = UpdateUI
        
        '通过 .SetFont(self.font)设置字体'
        # wx.Font(pointSize,family,style,weight,underline,faceName,encoding)
        self.font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'SimHei')
        
        self.InitUI() # 绘制UI界面
        self.Center()
        
    def InitUI(self):
        #绘制面板
        panel = wx.Panel(self)
        #图标设定
        self.Software_Icon()
        #图片插入
        image = wx.Image('hnust(black).ico', wx.BITMAP_TYPE_ICO)
        temp = image.ConvertToBitmap()
        #size = temp.GetWidth(), temp.GetHeight()
        self.bmp = wx.StaticBitmap(parent=panel, bitmap=temp)
        #静态文本
        self.text = wx.StaticText(panel, label='--请检查你输入的学号、密码或验证码是否正确\n--学号输入完成记得按回车键\n--请核对你所查询的学段\n--或者刷新验证码试试吧~', pos=(10,10))
        self.text.SetForegroundColour('#FF4500')
        self.text.SetFont(self.font)
        #确定按钮
        button = wxbutton.GenButton(panel, 0, '好的~')
        #控件排版
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.bmp, 1, wx.CENTER, 50)
        box.Add(self.text, 0, wx.CENTER, 50)
        box.Add(button, 0, wx.CENTER, 50)
        panel.SetSizerAndFit(box)
        #事件处理
        self.Bind(wx.EVT_BUTTON, self.OnClick, button)
        
    def Software_Icon(self):
        icon = wx.Icon('hnust(black).ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

    def OnClick(self,event):
        '关闭该窗口'
        self.Close()

        
class HelpFrame(wx.Frame):
    def __init__(
        self, parent=None, id=1, title='帮助信息', pos=wx.DefaultPosition,size=wx.DefaultSize,
        style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER), UpdateUI=None
    ):
        wx.Frame.__init__(self,parent, id, title, size=size, pos=pos, style=style)
        
        self.UpdateUI = UpdateUI
                
        '通过 .SetFont(self.font)设置字体'
        # wx.Font(pointSize,family,style,weight,underline,faceName,encoding)
        self.font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'SimHei')
        
        self.InitUI()
        self.Center()
        
    def InitUI(self):
        panel = wx.Panel(self)

        self.Software_Icon()
        
        image = wx.Image('hnust(black).ico', wx.BITMAP_TYPE_ICO)
        temp = image.ConvertToBitmap()
        #size = temp.GetWidth(), temp.GetHeight()
        self.bmp = wx.StaticBitmap(parent=panel, bitmap=temp)
        
        self.text = wx.StaticText(panel, label='    ------------四步走------------\n  ①输入学号按回车获取验证码\n  ②第二框输入教务网密码\n  ⑤输入验证码按回车或点击"查询成绩"即可\n', pos=(10,10))
        self.text.SetForegroundColour('#FF4500')
        self.text.SetFont(self.font)
        button = wxbutton.GenButton(panel, 1, 'Get！')
        
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.bmp, 1, wx.CENTER, 50)
        box.Add(self.text, 0, wx.CENTER, 50)
        box.Add(button, 0, wx.CENTER, 50)
        panel.SetSizerAndFit(box)
        
        self.Bind(wx.EVT_BUTTON, self.OnClick, button)

    def Software_Icon(self):
        icon = wx.Icon('hnust(black).ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
    def OnClick(self, event):
        '关闭该窗口'
        self.Close()
        
