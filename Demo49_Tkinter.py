#Tkinter(Toolkit工具包 interface图形界面工具包)
from tkinter import *
import tkinter.messagebox as messagebox

class Application(Frame):   #Frame框架类，是所有widget的父容器
    def __init__(self, master= None):   #Application 类的实例已经隐式地创建了一个主窗口
        Frame.__init__(self, master)    #初始化并关联到父窗口
        self.pack() #自动调用pack()方法，将自己放置到父窗口中
        self.createWidgets()
    def createWidgets(self):
        self.helloLabel = Label(self, text= 'Hello, world!')
        self.helloLabel.pack()
        self.quitButtion = Button(self, text= 'Quit', command= self.quit)
        self.quitButtion.pack()
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text= 'OK', command= self.hello)
        self.alertButton.pack()
    def hello(self):
        messagebox.showinfo('Hello', 'Hello, %s!' % self.nameInput.get())

app = Application()
app.master.title('Hello, world2!')  #设置窗口标题GUI(Graphical User Interface)
app.master.geometry('192x108+100+100')  #设置窗口大小和位置
#app.master.iconbitmap("icon.ico")    #设置窗口图标
#app.master.resizable(False, False)     #设置窗口大小不可变
app.mainloop()
