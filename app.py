from tkinter import Tk, Label, Button, Entry,Canvas, ttk,END
import mysql.connector
from datetime import datetime,timedelta
import re
import csv
from time import sleep
import os
import sys
import pathlib
from timeit import default_timer as timer
import urllib3
import instaloader
import time

class AppUI():
    def __init__(self,title,size,loader):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.tc = ttk.Notebook(self.root)
        self.t1 = ttk.Frame(self.tc)
        self.t2 = ttk.Frame(self.tc)
        self.loader = loader
        root = self.root
        tc = self.tc
        t1 = self.t1
        t2 = self.t2
        tc.add(t1, text='Account')
        tc.add(t2, text='Scrapper')
        tc.pack()
        tc.place(x=0, y=80)
    
        now = datetime.today().strftime('%Y-%m-%d')
        ttk.Label(text="Instagram Scrapper", width=25,foreground='green').grid(row=3, column=1)
        ttk.Label(text="", width=25).grid(row=3, column=3)
        ttk.Label(text="", width=25).grid(row=4, column=3)
        ttk.Label(text=now, width=25,foreground='green').grid(row=3, column=4)
        ttk.Label(text="Created by kosong", width=25,foreground='green').grid(row=5, column=1)

        ttk.Label(t1, text ="Login", width=25).grid(row =2, column=2)
        ttk.Label(t1, text ="", width=25).grid(row =3, column=2)
        ttk.Label(t1, text ="Username", width=10).grid(row = 4, column=1)
        ttk.Label(t1, text ="Password", width=10).grid(row = 5, column=1)
        ttk.Label(t1, text="", width=30).grid(row=1, column=3)
        ttk.Label(t1, text="", width=15).grid(row=2, column=1)

        self.entry_username = ttk.Entry(t1, width=25)
        self.entry_username.grid(row =4, column=2)
        self.entry_password = ttk.Entry(t1, width=25,show="*")
        self.entry_password.grid(row =5, column=2)

        self.button = ttk.Button(t1, text="Login" ,width=20,command=self.submitLogin).grid(row=6,column=2)


        ttk.Label(t1, text ="", width=25).grid(row =7, column=2)
        self.label_login = ttk.Label(t1, text="", width=25)
        self.label_login.grid(row=8, column=2)

        
        ttk.Label(t2, text="", width=25).grid(row=1, column=1)
        ttk.Label(t2, text="", width=25).grid(row=2, column=1)
        ttk.Label(t2, text="Instagram Account Scrapper", width=25).grid(row=2, column=2)
        ttk.Label(t2, text="", width=25).grid(row=3, column=1)
        
        ttk.Label(t2, text="Username Target", width=30).grid(row=4, column=1)
        self.entry_target = ttk.Entry(t2, width=25)
        self.entry_target.grid(row =4, column=2)

        ttk.Label(t2, text="Minimal Follower", width=30).grid(row=5, column=1)
        self.entry_min = ttk.Entry(t2, width=25)
        self.entry_min.grid(row =5, column=2)

        self.button = ttk.Button(t2, text="Scrap" ,width=20,command=self.submitScrap).grid(row=6,column=2)
        
        ttk.Label(t2, text="", width=25).grid(row=8, column=1)
        ttk.Label(t2, text="Progress", width=25).grid(row=10, column=2)
        ttk.Label(t2, text="Total followers scraped", width=25).grid(row=12, column=1)
        ttk.Label(t2, text="", width=25).grid(row=11, column=1)
        self.total_followers = ttk.Entry(t2, width=25,state='disabled',foreground='green')
        self.total_followers.grid(row =12, column=2)

        ttk.Label(t2, text="Time", width=25).grid(row=13, column=1)
        self.total_time = ttk.Entry(t2, width=25,state='disabled',foreground='green')
        self.total_time.grid(row =13, column=2)
        
        ttk.Label(t2, text="Username", width=25).grid(row=14, column=1)
        self.current_username = ttk.Entry(t2, width=25,state='disabled',foreground='green')
        self.current_username.grid(row =14, column=2)
        
        ttk.Label(t2, text="Account Name", width=25).grid(row=15, column=1)
        self.account_name = ttk.Entry(t2, width=25,state='disabled',foreground='green')
        self.account_name.grid(row =15, column=2)

        ttk.Label(t2, text="", width=25).grid(row=16, column=1)
        ttk.Label(t2, text="", width=25).grid(row=17, column=1)
        ttk.Label(t2, text="", width=25).grid(row=18, column=1)
        ttk.Label(t2, text="", width=25).grid(row=19, column=1)
        self.error_scrap=ttk.Label(t2, text="", width=25)
        self.error_scrap.grid(row=17, column=2)
        root.mainloop()

    def submitLogin(self):
        username=self.entry_username.get()
        password=self.entry_password.get()
        try:
            result=self.loader.login(username,password)
            self.label_login.configure(text="Login Berhasil",foreground='green')
        except Exception as e:
            self.label_login.configure(text="Login Gagal",foreground='red')

    def submitScrap(self):
        pathlib.Path('downloads/').mkdir(parents=True, exist_ok=True)        
        start = timer()   
        PROFILE = self.entry_target.get()
        min_val = self.entry_min.get()
        for ind in range(len(PROFILE)):
            pro = PROFILE
            try:
                filename = 'downloads/'+pro+'.csv'
                with open(filename,'a',newline='',encoding="utf-8") as csvf:
                    csv_writer = csv.writer(csvf)
                    csv_writer.writerow(['username','fullname','is_private','media_count','follower_count','following_count','website','email','hp', 'scraped_at'])
        
                profile = instaloader.Profile.from_username(self.loader.context, pro)
                main_followers = profile.followers
                count = 0
                total = 0
                for person in profile.get_followers():
                    try:
                        username = person.username
                        if(person.followers>int(min_val)):
                            fullname  = person.full_name
                            is_verified = person.is_verified
                            is_private = person.is_private
                            media_count  = person.mediacount
                            follower_count = person.followers
                            following_count = person.followees
                            bio = person.biography
                            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", bio)
                            no_hp= re.findall(r"(\d{4}[-\.\s]??\d{4}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", bio)
                            website = person.external_url
                            curr = str(datetime.datetime.now()) 
                            if(not website):
                                website='Tidak Ada'
                            if(not no_hp):
                                no_hp=['Tidak Ada']
                            if(not emails):
                                emails=['Tidak Ada']
                            with open(filename,'a',newline='') as csvf:
                                csv_writer = csv.writer(csvf)
                                csv_writer.writerow([username,fullname,is_private,media_count,follower_count,following_count,website,emails[0],no_hp[0],curr])
                        total+=1
                        self.current_username['state']='normal'
                        self.current_username.delete(0,END)
                        self.current_username.insert(0,username)
                        self.current_username['state']='disabled'
                        self.total_followers['state']='normal'
                        self.total_followers.delete(0,END)
                        self.total_followers.insert(0,str(total)+' out of '+str(main_followers))
                        self.total_followers['state']='disabled'
                        self.total_time['state']='normal'
                        self.total_time.delete(0,END)
                        self.total_time.insert(0,str(timedelta(seconds=(timer()-start))))
                        self.total_time['state']='disabled'
                        self.account_name['state']='normal'
                        self.account_name.delete(0,END)
                        self.account_name.insert(0,pro)
                        self.account_name['state']='disabled'
                        self.t2.update()
                    except Exception as e:
                        break
            except:
                continue
    

if __name__ == '__main__':
    loader = instaloader.Instaloader()
    gui = AppUI("Instagram Scrapper","550x450",loader)
    