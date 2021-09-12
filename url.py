from tkinter import * 
from tkinter import ttk
import pyshorteners
from pytube import YouTube
import os
from PIL import Image,ImageTk
import qrcode


class Url:
    def __init__(self,root):
        self.root=root      
        self.root.title("URL SHORTENER AND YOUTUBE DOWNLOADER AND QR_CODE GENERATOR")
        self.root.geometry("500x420+300+50")
        self.root.resizable(False,False)
        self.root.config(bg='white')

        title=Label(self.root,text='URL SHORTENER AND YOUTUBE DOWNLOADER AND QR_CODE GENERATOR',font=("algerian",10),bg="#262626",fg='white').pack(side=TOP,fill=X)
        
        self.var_url=StringVar()

        lbl_url=Label(self.root,text='URL:',font=("times new roman",15),bg='white').place(x=10,y=50)
        txt_url=Entry(self.root,textvariable=self.var_url,font=("times new roman",13),bg="#d9fcff").place(x=120,y=50,width=340,height=30)

        btn_short=Button(self.root,text='Short',command=self.shorter,font=('times new roman',13),bg='red',fg='white').place(x=30,y=100,width=40,height=40)
        btn_clear=Button(self.root,text='Clear',command=self.clear,font=('times new roman',13),bg='violet',fg='white').place(x=80,y=100,width=40,height=40)
        btn_qr=Button(self.root,text='QR',command=self.qr,font=('times new roman',13),bg='grey',fg='white').place(x=130,y=100,width=40,height=40)
        btn_youtubeaudio=Button(self.root,text='Download Audio',command=self.downloadaudio,font=('times new roman',13),bg='blue',fg='white').place(x=180,y=100,width=150,height=40)
        btn_youtubevideo=Button(self.root,text='Download Video',command=self.download,font=('times new roman',13),bg='green',fg='white').place(x=340,y=100,width=150,height=40)
        frame_=Frame(self.root,bd=2,relief=RIDGE,bg='#d9fcff')
        frame_.place(x=10,y=150,width=470,height=180)



        self.qr_title=Label(frame_,text='QR CODE: ',font=("times new roman",15),bg="white",anchor='w')
        self.qr_title.place(x=0,y=0,relwidth=1)

        self.qr_img=Label(frame_,text='Image',font=("times new roman",15),bg="lightgrey",bd=2,relief=RIDGE)
        self.qr_img.place(x=5,y=32,width=180,height=140)

        lbl_url=Label(frame_,text='Shorted URL : ',font=("times new roman",18),bg="#d9fcff").place(x=190,y=32)
        
        self.video_des=Text(frame_,font=("times new roman",12),bg="#d9fcff")
        self.video_des.place(x=190,y=60,width=270,height=110)

        self.lbl_per=Label(self.root,text='Downloading : 0%',font=("times new roman",13),bg='white')
        self.lbl_per.place(x=0,y=340)
        self.pro=ttk.Progressbar(self.root,orient=HORIZONTAL,length=590,mode='determinate')
        self.pro.place(x=0,y=380,width=485,height=20)
        if os.path.exists('Audios')==False:
            os.mkdir('Audios')
        if os.path.exists('Videos')==False:
            os.mkdir('Videos')
        
    def progress(self,streams,chunk,bytes_remaining):
        percent=(float(abs(bytes_remaining-self.size_byte)/self.size_byte))*float(100)
        self.pro['value']=percent
        self.pro.update()
        self.lbl_per.config(text=f'Downloading : {str(round(percent,2))}%')

        if round(percent,2)==100:
            self.lbl_per.config(text=f'Download Completed')

    def shorter(self):
        if self.var_url.get()=='':
            self.msg.config(text='Please enter url',fg='red')
        else:
            s=pyshorteners.Shortener()
            self.video_des.insert(END,s.tinyurl.short(self.var_url.get()))

    def download(self):
        yt=YouTube(self.var_url.get(),on_progress_callback=self.progress)
        dot=yt.streams.get_highest_resolution()
        self.size_byte=dot.filesize
        maxsize=self.size_byte/1024000
        dot.download('Videos/')
    
    def downloadaudio(self):
        yt=YouTube(self.var_url.get(),on_progress_callback=self.progress)
        dot=yt.streams.filter(only_audio=True).first()
        self.size_byte=dot.filesize
        maxsize=self.size_byte/1024000
        dot.download('Audios/')

    def clear(self):
        self.lbl_per.config(text=f'Downloading : 0%')
        self.var_url.set('')
        self.pro['value']=0

    def qr(self):
        Qr=qrcode.QRCode(version=1,box_size=10,border=5)
        Qr.add_data(self.var_url.get())
        Qr.make(fit=True)
        img=Qr.make_image(fill='black',back_color='white')
        self.image=img
        self.image=self.image.resize((180,140),Image.ANTIALIAS)
        self.image=ImageTk.PhotoImage(self.image)
        self.qr_img.config(image=self.image)



root=Tk()
obj=Url(root)
root.mainloop()
