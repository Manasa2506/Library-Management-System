import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Label
from kivy.uix.button import Button
from kivy.base import stopTouchApp
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition,FadeTransition
from kivy.core.window import Window
from kivy.clock import Clock
import mysql.connector
import random
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
Window.size=(1366,768)
Window.fullscreen=True
mydb=mysql.connector.connect(host="localhost",user="root",passwd="adnan",database="LMS")
crsr=mydb.cursor()
crsr.execute("""create table if not exists student (
                        id int(3) primary key,
                        name varchar(30),
                        grade int(3),
                        sec char(2),
                        bk_brwed varchar(50),
                        date_brwed date,
                        expctd_ret varchar(12),
                        bk_condtn varchar(80),
                        Fine int)""")
crsr.execute("""create table if not exists library (
                        id int(3) primary key,
                        bK_name varchar(30),
                        genre varchar(10),
                        author varchar(30),
                        publsher varchar(30),
                        avbl varchar(15))""")

#-----------------------------------------------------------------------------------------------------------------------------------
class splash_screen(Screen):
    def __init__(self,**kwargs):
        super(splash_screen,self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.layout=BoxLayout()
        self.pic=Image(source='Hm_scr.jpg')
        self.layout.add_widget(self.pic)
        self.add_widget(self.layout)
        Clock.schedule_once(self.scrn_change,7)
    def scrn_change(self,*args):
        self.layout.remove_widget(self.pic)
        self.manager.transition=FadeTransition()
        self.manager.current='main'
        Window.clearcolor = (0.1, 0.1, 0, 1)
#-----------------------------------------------------------------------------------------------------------------------------------
class main_screen(Screen):
    def __init__(self,**kwargs):
        super(main_screen,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical",spacing=100)
        exop=BoxLayout(size_hint=(None, None), height=30, pos_hint={'right': 1})
        name=Label(text="Babajividhyashram",font_size=50,size_hint_y=.2)
        hd=Label(text="Library Managenent System",font_size=60)
        navig = BoxLayout(size_hint_y=0.5,padding=10,spacing=10)
        std=Button(text="Student",font_size=40)
        lib=Button(text="Library",font_size=40)
        ext=Button(size_hint=(None,None),width=30 ,height=30,background_down="close_pressed.png",background_normal="close.png")
        ext.bind(on_release=self.close)
        minimz=Button(size_hint=(None,None),width=30 ,height=30,background_down="min_pressed.png",background_normal="min.png")
        minimz.bind(on_release=self.minimize)
        exop.add_widget(minimz)
        exop.add_widget(ext)
        layout.add_widget(exop)
        layout.add_widget(name)
        layout.add_widget(hd)
        navig.add_widget(std)
        navig.add_widget(lib)
        std.bind(on_release=self.student)
        lib.bind(on_release=self.library)
        layout.add_widget(navig)
        self.add_widget(layout)
    def student(self,*args):
        self.manager.transition=SlideTransition(direction="right")
        Window.clearcolor = (0, 0.1, 0, 1)
        self.manager.current='student'
    def library(self,*args):
        self.manager.transition=SlideTransition(direction="left")
        self.manager.current='library'
        Window.clearcolor = (0, 0, 0.1, 1)
    def close(self,*args):
        stopTouchApp()
        Window.close()
    def minimize(self,*args):
        App.get_running_app().root_window.minimize()
#___________________________________________________________________________________________________________________________________
class Student(Screen):
    def __init__(self,**kwargs):
        super(Student,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical")
        astd=Button(text="Add Student",font_size=35)
        astd.bind(on_release=self.adstd)
        rstd=Button(text="Remove Student",font_size=35)
        rstd.bind(on_release=self.rmstd)
        sstd=Button(text="Show Students",font_size=35)
        sstd.bind(on_release=self.std_db)
        bstd=Button(text="Book Lending",font_size=35)
        bstd.bind(on_release=self.brw_bks)
        back=Button(text="Back",size_hint=(.2,.1),pos_hint={"x":.4,"y":.1})
        back.bind(on_release=self.bck)
        navig1=BoxLayout(orientation="vertical",padding=30,spacing=30)
        navig2=BoxLayout(orientation="vertical",padding=30,spacing=30)
        navig3=BoxLayout()
        lbl=Label(text="Student Manager",font_size=60)
        layout.add_widget(lbl)
        navig1.add_widget(astd)
        navig1.add_widget(rstd)
        navig2.add_widget(sstd)
        navig2.add_widget(bstd)
        navig3.add_widget(navig1)
        navig3.add_widget(navig2)
        layout.add_widget(navig3)
        layout.add_widget(back)
        self.add_widget(layout)
    def adstd(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current="add_std"            
    def rmstd(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current="rem_std"
    def std_db(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current="std_db"
    def brw_bks(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current='book_lending'
    def bck(self,arg):
        self.manager.transition=SlideTransition(direction="left")
        self.manager.current='main'
        Window.clearcolor = (0.1, 0.1, 0, 1)
#___________________________________________________________________________________________________________________________________
class Library(Screen):
    def __init__(self,**kwargs):
        super(Library,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical")
        lbl=Label(text="Library Manager",font_size=60)
        back=Button(text="Back",size_hint=(.2,.1),pos_hint={"x":.4,"y":.1})
        back.bind(on_release=self.bck)
        abk=Button(text="Add Books",font_size=35)
        abk.bind(on_release=self.adbk)
        rbk=Button(text="Remove Books",font_size=35)
        rbk.bind(on_release=self.rmbk)
        sbk=Button(text="Show Books",font_size=35)
        sbk.bind(on_release=self.shbk)
        vbk=Button(text="View Books Available",font_size=35)
        vbk.bind(on_release=self.vwbk)
        navig1=BoxLayout(orientation="vertical",padding=30,spacing=30)
        navig2=BoxLayout(orientation="vertical",padding=30,spacing=30)
        navig3=BoxLayout()
        layout.add_widget(lbl)
        navig1.add_widget(abk)
        navig1.add_widget(rbk)
        navig2.add_widget(sbk)
        navig2.add_widget(vbk)
        navig3.add_widget(navig1)
        navig3.add_widget(navig2)
        layout.add_widget(navig3)
        layout.add_widget(back)
        self.add_widget(layout)
    def adbk(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current='add_book'            
    def rmbk(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current='remove_book'
    def shbk(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current='show_book'
    def vwbk(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current='view_book'
    def bck(self,arg):
        self.manager.transition=SlideTransition(direction="right")
        self.manager.current='main'
        Window.clearcolor = (0.1, 0.1, 0, 1)
#___________________________________________________________________________________________________________________________________
class add_student(Screen):
    
    def __init__(self,**kwargs):
        super(add_student,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical",padding=10,spacing=10)
        self.lbl=Label(text="Enter student details",font_size=50)
        tf1=BoxLayout(padding=10)
        tf2=BoxLayout(padding=10)
        tf3=BoxLayout(padding=10)
        tf4=BoxLayout(padding=10)
        btns=BoxLayout(spacing=900,padding=10)
        stdnm=Label(text="Student Name:",font_size=30,size_hint_x=0.3)
        grd=Label(text="Grade:",font_size=30,size_hint_x=0.3)
        sec=Label(text="Sec:",font_size=30,size_hint_x=0.3)
        sid=Label(text="ID:",font_size=30,size_hint_x=0.33)
        self.sidt=TextInput(font_size=40,multiline=False,input_filter="float")
        self.stdnmt=TextInput(font_size=40,multiline=False)
        self.grdt=TextInput(font_size=40,multiline=False,input_filter="float")
        self.sect=TextInput(font_size=40,multiline=False)
        self.sect.bind(on_text_validate=self.sbmt)
        rand=Button(text="Press here to\ngenerate Id",size_hint=(.1,1),font_size=14)
        rand.bind(on_release=self.randomize)
        submit=Button(text="Submit",size_hint=(.1,.7),font_size=30)
        submit.bind(on_release=self.sbmt)
        back=Button(text="Back",size_hint=(.1,.7),font_size=30)
        back.bind(on_release=self.bck)
        tf1.add_widget(stdnm)
        tf1.add_widget(self.stdnmt)
        tf2.add_widget(grd)
        tf2.add_widget(self.grdt)
        tf3.add_widget(sec)
        tf3.add_widget(self.sect)
        tf4.add_widget(sid)
        tf4.add_widget(rand)
        tf4.add_widget(self.sidt)
        btns.add_widget(back)
        btns.add_widget(submit)
        layout.add_widget(self.lbl)
        layout.add_widget(tf4)
        layout.add_widget(tf1)
        layout.add_widget(tf2)
        layout.add_widget(tf3)
        layout.add_widget(btns)
        self.add_widget(layout)
    def bck(self,*args):
        self.manager.transition=FadeTransition()
        self.manager.current='student'
    def sbmt(self,*args):
        if self.sidt.text!="" and self.stdnmt.text!="" and self.grdt.text!="" and self.sect.text!="":
            sid=int(self.sidt.text)
            sname=str(self.stdnmt.text)
            grd=int(self.grdt.text)
            sec=str(self.sect.text)
            try:
                sql="INSERT INTO student(id,name,grade,sec) VALUES(%s,%s,%s,%s)"
                val=(sid,sname,grd,sec)
                crsr.execute(sql,val)
                popup = Popup(title='Success',title_size=22,title_color=[0,1,0,1],content=Label(text=sname+' has been successfully added',font_size=26),
                              size_hint=(None, None), size=(500,150))
                popup.open()
                mydb.commit()
                self.sidt.text=""
                self.stdnmt.text=""
                self.grdt.text=""
                self.sect.text=""
            except:
                popup = Popup(title='Error',content=Label(text='Error adding student',font_size=25),
                              size_hint=(None, None), size=(450,150))
                popup.open()
        else:
            popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please enter all details",font_size=30),size_hint=(None,None),size=(450,150))
            popup.open()
            
    def randomize(self,*args):
        sql="SELECT id from student"
        crsr.execute(sql)
        myresult=crsr.fetchall()
        l=[]
        for i in myresult:
           l.append(i[0])
        while True:
           x=random.randint(100,999)
           if x not in l:
               self.sidt.text=str(x)
               break
           else:
               pass
#___________________________________________________________________________________________________________________________________
class remove_student(Screen):
    def __init__(self,**kwargs):
        super(remove_student,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical",padding=10,spacing=10)
        tf=BoxLayout(padding=70)
        btns=BoxLayout(spacing=900,padding=10)
        self.lbl=Label(text='Enter Student ID',font_size=50)
        sid=Label(text="Student ID",font_size=30,size_hint_x=0.3)
        self.sidt=TextInput(multiline=False,font_size=40,input_filter="float")
        self.sidt.bind(on_text_validate=self.sbmt)
        submit=Button(text="Submit",size_hint=(.1,.3),font_size=30)
        submit.bind(on_release=self.sbmt)
        back=Button(text="Back",size_hint=(.1,.3),font_size=30)
        back.bind(on_release=self.bck)
        tf.add_widget(sid)
        tf.add_widget(self.sidt)
        btns.add_widget(back)
        btns.add_widget(submit)
        layout.add_widget(self.lbl)
        layout.add_widget(tf)
        layout.add_widget(btns)
        self.add_widget(layout)
    def sbmt(self,*args):
        if self.sidt.text!="":
            sql="SELECT id from student"
            crsr.execute(sql)
            myresult=crsr.fetchall()
            l=[]
            for i in myresult:
               l.append(i[0])
            sql="delete from student where id=%s"
            val=int(self.sidt.text)
            if val in l:
                crsr.execute(sql,(val,))
                popup=Popup(title="Success",title_color=[0,1,0,1],title_size=22,content=Label(text="Student successfully removed",font_size=25),
                            size_hint=(None,None),size=(450,150))
                popup.open()
                mydb.commit()
                self.sidt.text=""
            else:
                popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Error removing student",font_size=25),
                            size_hint=(None,None),size=(450,150))
                popup.open()
        else:
            popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please enter all details",font_size=30),size_hint=(None,None),size=(450,150))
            popup.open()

    def bck(self,*args):
        self.manager.transition=FadeTransition()
        self.manager.current='student'
#___________________________________________________________________________________________________________________________________
class student_db(Screen):
    def __init__(self,**kwargs):
        super(student_db,self).__init__(**kwargs)
        blayout=BoxLayout(orientation="vertical")
        hdlayout=BoxLayout()
        glayout=GridLayout(cols=9,padding=50, spacing=50,size_hint=(None, None), width=1366)
        glayout.bind(minimum_height=glayout.setter('height'))
        
        scroll = ScrollView(size_hint=(None, None), size=(1366,640),pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        lbl=Label(text="All Student Details",font_size=40)
        back=Button(text="Back",size_hint=(.09,.6))
        back.bind(on_release=self.bck)
        crsr.execute("select* from student")
        std=crsr.fetchall()
        hd=["ID","Name","Grade","Sec","Borrowed","Date Borrowed","Return By","Book Condition","Fine"]
        for i in hd:
            head=Label(text=i,font_size=24)
            glayout.add_widget(head)
        crsr.execute("SELECT * FROM student")
        std=crsr.fetchall()
        for i in std:
            for j in i:
                det=Label(text=str(j),font_size=22)
                glayout.add_widget(det)
        hdlayout.add_widget(back)
        hdlayout.add_widget(lbl)
        scroll.add_widget(glayout)
        blayout.add_widget(hdlayout)
        blayout.add_widget(scroll)
        self.add_widget(blayout)
    def bck(self,*args):
        self.manager.transition=FadeTransition()
        self.manager.current='student'
#___________________________________________________________________________________________________________________________________
class book_lnd(Screen):
    def __init__(self,**kwargs):
        super(book_lnd,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical")
        hd=Label(text="Book Lending",font_size=60)
        navig = BoxLayout(size_hint_y=0.5,padding=15,spacing=12)
        lb=Button(text="Lend Books",font_size=40,size_hint_y=0.6)
        rb=Button(text="Return Books",font_size=40,size_hint_y=0.6)
        back=Button(text="Back",size_hint=(.2,.1),pos_hint={"x":.4,"y":.1})
        back.bind(on_release=self.bck)
        layout.add_widget(hd)
        navig.add_widget(lb)
        navig.add_widget(rb)
        lb.bind(on_release=self.lnd)
        rb.bind(on_release=self.ret)
        layout.add_widget(navig)
        layout.add_widget(back)
        self.add_widget(layout)
    def lnd(self,*args):
        self.manager.transition=SlideTransition(direction="right")
        self.manager.current='lend_book'
    def ret(self,*args):
        self.manager.transition=SlideTransition(direction="left")
        self.manager.current='return_book'
    def bck(self,arg):
        self.manager.transition=FadeTransition()
        self.manager.current='student'
#___________________________________________________________________________________________________________________________________
class brrw_bks(Screen):
    def __init__(self,**kwargs):
        super(brrw_bks,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical")
        std=BoxLayout(padding=50)
        bk=BoxLayout(padding=50)
        btns=BoxLayout(spacing=900,padding=10)
        lbl=Label(text="Lend Books",font_size=55)
        self.sidt=TextInput(font_size=40,multiline=False,input_filter="float")
        self.bidt=TextInput(font_size=40,multiline=False,input_filter="float")
        self.bidt.bind(on_text_validate=self.sbmt)
        sid=Label(text="Student ID: ",font_size=35,size_hint_x=.3)
        bid=Label(text="Book ID: ",font_size=35,size_hint_x=.3)
        submit=Button(text="Submit",size_hint=(.2,.4),font_size=30)
        submit.bind(on_release=self.sbmt)
        back=Button(text="Back",size_hint=(.2,.4),font_size=30)
        back.bind(on_release=self.bck)
        std.add_widget(sid)
        std.add_widget(self.sidt)
        bk.add_widget(bid)
        bk.add_widget(self.bidt)
        btns.add_widget(back)
        btns.add_widget(submit)
        layout.add_widget(lbl)
        layout.add_widget(std)
        layout.add_widget(bk)
        layout.add_widget(btns)
        self.add_widget(layout)
    def bck(self,*args):
        self.bidt.text=""
        self.sidt.text=""
        self.manager.transition=FadeTransition()
        self.manager.current='student'

    def sbmt(self,*args):
        if self.sidt.text!="" and self.bidt.text!="":
            sid=int(self.sidt.text)
            bid=int(self.bidt.text)
            crsr.execute("SELECT * FROM library")
            bkd = crsr.fetchall()
            bk_det_id=[]
            for i in bkd:
                bk_det_id.append(i[0])
            bnm=""
            sql="SELECT * from student"
            crsr.execute(sql)
            myresult=crsr.fetchall()
            std_det=[]
            sid_det=[]
            for i in range(len(myresult)):
                b=(myresult[i][4],myresult[i][-1])
                std_det.append(b)
                sid_det.append(myresult[i][0])
                
            for i in std_det:
                if sid in sid_det:
                    if i[0] == None:
                        if i[1] == None:
                            if bid in bk_det_id:
                                for i in bkd:
                                    if bid==i[0]:
                                        if i[-1]=="Available":
                                            bnm=i[1]
                                            sql="UPDATE student SET bk_brwed=%s,date_brwed=curdate(),expctd_ret=curdate()+10 WHERE id=%s"
                                            val=(bnm,sid)
                                            crsr.execute(sql,val)
                                            crsr.execute('UPDATE library SET avbl="Unavailable" where id=%s',(bid,))
                                            mydb.commit()
                                            popup = Popup(title='Success',title_size=22,title_color=[0,1,0,1],content=Label(text='Book successfully borrowed',font_size=25),size_hint=(None, None), size=(450,150))
                                            popup.open()
                                        else:
                                            popup=Popup(title='Error',content=Label(text='This book has already been borrowed',font_size=25),size_hint=(None, None), size=(550,150))
                                            popup.open()
                                            break
                                    else:
                                        pass
                            else:
                                popup = Popup(title='Error',content=Label(text='Please enter valid Book ID',font_size=25),size_hint=(None, None), size=(450,150))
                                popup.open()        
                        else:
                            popup = Popup(title='Error',content=Label(text='Student already has pending fine',font_size=25),size_hint=(None, None), size=(550,150))
                            popup.open()

                    else:
                        popup = Popup(title='Error',content=Label(text='Student has already borrowed a book',font_size=25),size_hint=(None, None), size=(550,150))
                        popup.open()
                else:
                    popup = Popup(title='Error',content=Label(text='Please enter valid Student ID',font_size=25),size_hint=(None, None), size=(450,150))
                    popup.open()
        else:
            popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please fill in all details",font_size=30),size_hint=(None,None),size=(450,150))
            popup.open()
                
#___________________________________________________________________________________________________________________________________
class retn_bk(Screen):
    def __init__(self,**kwargs):
        super(retn_bk,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical",padding=20,spacing=10)
        lsid=BoxLayout(spacing=15)
        lbid=BoxLayout(spacing=15)
        lbc=BoxLayout(spacing=15)
        lfn=BoxLayout(spacing=15)
        btns=BoxLayout(spacing=900,padding=10)
        tab=TabbedPanel(background_color = (0, 1, 1, .7))
        tabitem=TabbedPanelItem()
        tab.add_widget(tabitem)
        tabitem.text = 'Return Book'
        tab.do_default_tab=False
        tabitem.add_widget(layout)
        lbl=Label(text="Return Books",font_size=50)
        sid=Label(text="Student ID: ",font_size=35)
        bc=Label(text="Book conditon: ",font_size=35)
        fn=Label(text="Fine: ",font_size=35)
        bid=Label(text="Book ID: ",font_size=35)
        self.sidt=TextInput(multiline=False,font_size=40)
        self.bidt=TextInput(multiline=False,font_size=40)
        self.bct=TextInput(multiline=False,font_size=40)
        self.fnt=TextInput(multiline=False,font_size=40,input_filter="float")
        self.fnt.bind(on_text_validate=self.sbmt)
        self.bidt.bind(on_text_validate=self.sbmt)
        submit=Button(text="Submit",size_hint=(.1,.7),font_size=30)
        submit.bind(on_release=self.sbmt)
        back=Button(text="Back",size_hint=(.1,.7),font_size=30)
        back.bind(on_release=self.bck)
        btns.add_widget(back)
        btns.add_widget(submit)
        lsid.add_widget(sid)
        lsid.add_widget(self.sidt)
        lbid.add_widget(bid)
        lbid.add_widget(self.bidt)
        lbc.add_widget(bc)
        lbc.add_widget(self.bct)
        lfn.add_widget(fn)
        lfn.add_widget(self.fnt)
        layout.add_widget(lbl)
        layout.add_widget(lsid)
        layout.add_widget(lbid)
        layout.add_widget(lbc)
        layout.add_widget(lfn)
        layout.add_widget(btns)
#___________________________________________________________________________________________________________________________________
        #PAY FINE TAB
        tab2=TabbedPanelItem()
        tab2.text="Pay Fine"
        layout=BoxLayout(orientation="vertical",padding=10,spacing=10)
        tf=BoxLayout(padding=70)
        btns=BoxLayout(spacing=900,padding=10)
        self.lbl=Label(text='Enter Student ID',font_size=50)
        sid=Label(text="Student ID",font_size=30,size_hint_x=0.3)
        self.fsidt=TextInput(multiline=False,font_size=40,input_filter="float")
        self.fsidt.bind(on_text_validate=self.pay)
        submit=Button(text="Submit",size_hint=(.1,.3),font_size=30)
        submit.bind(on_release=self.pay)
        back=Button(text="Back",size_hint=(.1,.3),font_size=30)
        back.bind(on_release=self.bck)
        tf.add_widget(sid)
        tf.add_widget(self.fsidt)
        btns.add_widget(back)
        btns.add_widget(submit)
        layout.add_widget(self.lbl)
        layout.add_widget(tf)
        layout.add_widget(btns)
        tab2.add_widget(layout)
        tab.add_widget(tab2)
        self.add_widget(tab)
    def bck(self,*args):
        self.bidt.text=""
        self.sidt.text=""
        self.bct.text=""
        self.fnt.text=""
        self.manager.transition=FadeTransition()
        self.manager.current='book_lending'
    def sbmt(self,*args):
        if self.sidt.text!="":
            sql="SELECT id from student"
            crsr.execute(sql)
            myresult=crsr.fetchall()
            l=[]
            for i in myresult:
               l.append(i[0])
            print(l)
            if self.bct.text !="" and int(self.sidt.text) in l:
                try:
                    crsr.execute('UPDATE library SET avbl="Available" WHERE id=%s',(int(self.bidt.text),))
                    crsr.execute('UPDATE student SET bk_brwed=NULL,date_brwed=NULL,expctd_ret=NULL,bk_condtn=%s,Fine=%s WHERE id=%s',(self.bct.text,int(self.fnt.text),int(self.sidt.text)))
                    popup=Popup(title="Success",title_color=[0,1,0,1],title_size=22,content=Label(text="Book has been returned\nstudent has been fined successfully",font_size=30),size_hint=(None,None),size=(550,250))
                    popup.open()
                except:
                    popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please enter valid details",font_size=30),size_hint=(None,None),size=(450,150))
                    popup.open()
            else:
                try:
                    crsr.execute('UPDATE library SET avbl="Available" WHERE id=%s',(int(self.bidt.text),))
                    crsr.execute('UPDATE student SET bk_brwed=NULL,date_brwed=NULL,expctd_ret=NULL WHERE id=%s',(int(self.sidt.text),))
                    popup=Popup(title="Success",title_color=[0,1,0,1],title_size=22,content=Label(text="Book returned successfully",font_size=30),size_hint=(None,None),size=(450,150))
                    popup.open()
                except:
                    popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please enter valid details",font_size=30),size_hint=(None,None),size=(450,150))
                    popup.open()
        else:
            popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please fill in all details",font_size=30),size_hint=(None,None),size=(450,150))
            popup.open()

        mydb.commit()

    def pay(self,*arg):
        if self.fsidt.text!="":
            stdi=int(self.fsidt.text)
            sql="SELECT id from student"
            crsr.execute(sql)
            myresult=crsr.fetchall()
            l=[]
            fine=[]
            for i in myresult:
               l.append(i[0])
            crsr.execute("SELECT Fine FROM student")
            myresult=crsr.fetchall()
            for i in myresult:
               fine.append(i[0])
            print(len(l),len(fine))
            if stdi in l:
                for i in l:
                    if i==stdi:
                        b=l.index(i)
                        if fine[b]!=None:
                            crsr.execute('UPDATE student SET bk_brwed=NULL,date_brwed=NULL,expctd_ret=NULL,bk_condtn=NULL,Fine=NULL WHERE id=%s',(stdi,))
                            popup=Popup(title="Success",title_color=[0,1,0,1],title_size=22,content=Label(text="Student fine cleared successfully",font_size=30),size_hint=(None,None),size=(490,150))
                            popup.open()
                        else:
                            popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Student has no pending fine",font_size=30),size_hint=(None,None),size=(450,150))
                            popup.open()
                    else:
                        pass
            else:
                popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please enter valid details",font_size=30),size_hint=(None,None),size=(450,150))
                popup.open()
        else:
            popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please fill in all details",font_size=30),size_hint=(None,None),size=(450,150))
            popup.open()

        mydb.commit()


#-----------------------------------------------------------------------------------------------------------------------------------
class add_bk(Screen):
    def __init__(self,**kwargs):
        super(add_bk,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical",padding=10,spacing=10)
        self.lbl=Label(text="Enter Book details",font_size=50)
        tf1=BoxLayout(padding=10)
        tf2=BoxLayout(padding=10)
        tf3=BoxLayout(padding=10)
        tf4=BoxLayout(padding=10)
        tf5=BoxLayout(padding=10)
        btns=BoxLayout(spacing=900,padding=10)
        bknm=Label(text="Book Name:",font_size=30,size_hint_x=0.3)
        gen=Label(text="Genre:",font_size=30,size_hint_x=0.3)
        aut=Label(text="Author:",font_size=30,size_hint_x=0.3)
        pub=Label(text="Publisher:",font_size=30,size_hint_x=0.3)        
        bid=Label(text="ID:",font_size=30,size_hint_x=0.3)
        self.bidt=TextInput(font_size=40,multiline=False,input_filter="float")
        self.bknmt=TextInput(font_size=40,multiline=False)
        self.gent=TextInput(font_size=40,multiline=False)
        self.pubt=TextInput(font_size=40,multiline=False)
        self.autt=TextInput(font_size=40,multiline=False)
        self.pubt.bind(on_text_validate=self.sbmt)
        submit=Button(text="Submit",size_hint=(.1,.7),font_size=30)
        submit.bind(on_release=self.sbmt)
        back=Button(text="Back",size_hint=(.1,.7),font_size=30)
        back.bind(on_release=self.bck)
        tf1.add_widget(bknm)
        tf1.add_widget(self.bknmt)
        tf2.add_widget(gen)
        tf2.add_widget(self.gent)
        tf3.add_widget(aut)
        tf3.add_widget(self.autt)
        tf4.add_widget(bid)
        tf4.add_widget(self.bidt)
        tf5.add_widget(pub)
        tf5.add_widget(self.pubt)        
        btns.add_widget(back)
        btns.add_widget(submit)
        layout.add_widget(self.lbl)
        layout.add_widget(tf4)
        layout.add_widget(tf1)
        layout.add_widget(tf2)
        layout.add_widget(tf3)
        layout.add_widget(tf5)
        layout.add_widget(btns)
        self.add_widget(layout)
    def bck(self,*args):
        self.bidt.text=""
        self.bknmt.text=""
        self.gent.text=""
        self.autt.text=""
        self.pubt.text=""
        self.manager.transition=FadeTransition()
        self.manager.current='library'
        
    def sbmt(self,*args):
        if self.bidt.text!="" and self.bknmt.text!="" and self.gent.text!="" and self.autt.text!="" and self.pubt.text!="":
            bid=int(self.bidt.text)
            bname=self.bknmt.text
            gen=self.gent.text
            aut=self.autt.text
            pub=self.pubt.text
            try:
                sql="INSERT INTO library VALUES(%s,%s,%s,%s,%s,%s)"
                val=(bid,bname,gen,aut,pub,"Available")
                crsr.execute(sql,val)
                popup = Popup(title='Success',title_size=22,title_color=[0,1,0,1],content=Label(text=bname+' has been successfully added',font_size=26),
                              size_hint=(None, None), size=(500,150))
                popup.open()
                mydb.commit()
                self.bidt.text=""
                self.bknmt.text=""
                self.gent.text=""
                self.autt.text=""
                self.pubt.text=""
            except:
                popup = Popup(title='Error',content=Label(text='Error adding book',font_size=35),
                              size_hint=(None, None), size=(450,150))
                popup.open()
        else:
            popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please fill in all details",font_size=30),size_hint=(None,None),size=(450,150))
            popup.open()

#-----------------------------------------------------------------------------------------------------------------------------------
class remove_bk(Screen):
    def __init__(self,**kwargs):
        super(remove_bk,self).__init__(**kwargs)
        layout=BoxLayout(orientation="vertical",padding=10,spacing=10)
        tf=BoxLayout(padding=70)
        btns=BoxLayout(spacing=900,padding=10)
        self.lbl=Label(text='Enter Book ID',font_size=50)
        bid=Label(text="Book ID",font_size=30,size_hint_x=0.3)
        self.bidt=TextInput(multiline=False,font_size=40,input_filter="float")
        self.bidt.bind(on_text_validate=self.sbmt)
        submit=Button(text="Submit",size_hint=(.1,.3),font_size=30)
        submit.bind(on_release=self.sbmt)
        back=Button(text="Back",size_hint=(.1,.3),font_size=30)
        back.bind(on_release=self.bck)
        tf.add_widget(bid)
        tf.add_widget(self.bidt)
        btns.add_widget(back)
        btns.add_widget(submit)
        layout.add_widget(self.lbl)
        layout.add_widget(tf)
        layout.add_widget(btns)
        self.add_widget(layout)
    def sbmt(self,*args):
        if self.bidt.text!="":
            sql="SELECT id from library"
            crsr.execute(sql)
            myresult=crsr.fetchall()
            l=[]
            for i in myresult:
               l.append(i[0])
            sql="delete from library where id=%s"
            val=int(self.bidt.text)
            if val in l:
                crsr.execute(sql,(val,))
                popup=Popup(title="Success",title_color=[0,1,0,1],title_size=22,content=Label(text="Book successfully removed",font_size=36),
                            size_hint=(None,None),size=(450,150))
                popup.open()
                mydb.commit()
                self.bidt.text=""
            else:
                popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Error removing Book",font_size=36),
                            size_hint=(None,None),size=(450,150))
                popup.open()
        else:
            popup=Popup(title="Error",title_color=[1,0,0,1],title_size=22,content=Label(text="Please fill in all details",font_size=30),size_hint=(None,None),size=(450,150))
            popup.open()

    def bck(self,*args):
        self.manager.transition=FadeTransition()
        self.manager.current='library'

class avbl_bk(Screen):
    def __init__(self,**kwargs):
        super(avbl_bk,self).__init__(**kwargs)
        blayout=BoxLayout(orientation="vertical")
        hdlayout=BoxLayout()
        glayout=GridLayout(cols=5,padding=50, spacing=50,size_hint=(None, None), width=1366)
        glayout.bind(minimum_height=glayout.setter('height'))
        scroll = ScrollView(size_hint=(None, None), size=(1366,640),pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        lbl=Label(text="Available Book ",font_size=40)
        back=Button(text="Back",size_hint=(.09,.6))
        back.bind(on_release=self.bck)
        crsr.execute("select* from library")
        std=crsr.fetchall()
        hd=["ID","Book","Genre","Author","Publisher"]
        for i in hd:
            head=Label(text=i,font_size=24)
            glayout.add_widget(head)
        crsr.execute('SELECT * FROM library WHERE avbl="Available"')
        std=crsr.fetchall()
        for i in std:
            for j in range(0,5):
                det=Label(text=str(i[j]),font_size=22)
                glayout.add_widget(det)
        hdlayout.add_widget(back)
        hdlayout.add_widget(lbl)
        scroll.add_widget(glayout)
        blayout.add_widget(hdlayout)
        blayout.add_widget(scroll)
        self.add_widget(blayout)
    def bck(self,*args):
        self.manager.transition=FadeTransition()
        self.manager.current='library'
#-----------------------------------------------------------------------------------------------------------------------------------
class bk_db(Screen):
    def __init__(self,**kwargs):
        super(bk_db,self).__init__(**kwargs)
        blayout=BoxLayout(orientation="vertical")
        hdlayout=BoxLayout()
        glayout=GridLayout(cols=6,padding=50, spacing=50,size_hint=(None, None), width=1366)
        glayout.bind(minimum_height=glayout.setter('height'))
        scroll = ScrollView(size_hint=(None, None), size=(1366,640),pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        lbl=Label(text="All Book Details",font_size=40)
        back=Button(text="Back",size_hint=(.09,.6))
        back.bind(on_release=self.bck)
        crsr.execute("select* from library")
        std=crsr.fetchall()
        hd=["ID","Book","Genre","Author","Publisher","Availability"]
        for i in hd:
            head=Label(text=i,font_size=24)
            glayout.add_widget(head)
        crsr.execute("SELECT * FROM library")
        std=crsr.fetchall()
        for i in std:
            for j in i:
                det=Label(text=str(j),font_size=22)
                glayout.add_widget(det)
        hdlayout.add_widget(back)
        hdlayout.add_widget(lbl)
        scroll.add_widget(glayout)
        blayout.add_widget(hdlayout)
        blayout.add_widget(scroll)
        self.add_widget(blayout)
    def bck(self,*args):
        self.manager.transition=FadeTransition()
        self.manager.current='library'
#-----------------------------------------------------------------------------------------------------------------------------------
class manager(App):
    def build(self):
        root=ScreenManager()
        root.add_widget(splash_screen(name='spl_screen'))
        root.add_widget(main_screen(name='main'))
        root.add_widget(Student(name="student"))
        root.add_widget(Library(name="library"))
        root.add_widget(add_student(name="add_std"))
        root.add_widget(remove_student(name="rem_std"))
        root.add_widget(student_db(name="std_db"))
        root.add_widget(brrw_bks(name="lend_book"))
        root.add_widget(retn_bk(name="return_book"))
        root.add_widget(add_bk(name="add_book"))
        root.add_widget(remove_bk(name="remove_book"))
        root.add_widget(avbl_bk(name="view_book"))
        root.add_widget(bk_db(name="show_book"))
        root.add_widget(book_lnd(name="book_lending"))
        print(root.screen_names)
        return root
m=manager()
m.run()
#-----------------------------------------------------------------------------------------------------------------------------------
