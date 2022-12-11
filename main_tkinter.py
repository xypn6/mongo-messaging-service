import tkinter
import pymongo
import certifi
from cryptography.fernet import Fernet
import datetime
import platform
import socket
import requests
import time
from github import Github
from pprint import pprint
import random
import sys
from colorama import Fore, Back, Style


git_pass = "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"

github = Github(git_pass)
user = github.get_user()
repository = user.get_repo(f'k-hold')
file_content = repository.get_contents('held_k.txt')
key = file_content.decoded_content.decode()
en_key = Fernet(key)

software_version = {"type": en_key.encrypt(b"GUI"), 
                    "version": en_key.encrypt(b"2.0")}

def messageWin():
    global col
    mw = tkinter.Tk()
    mw.title("Login")
    mw.geometry("665x400")
    
    message_e = tkinter.Entry(mw, bg="light blue")
    msg_box = tkinter.Text(mw, height=23,bg="grey")
    scrollbar1 = tkinter.Scrollbar(mw, orient="vertical", command=msg_box.yview)
    
    
    client = pymongo.MongoClient(f"mongodb+srv://{usr}:{psw}@messagehost.r9loud3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = client["msgs"]
    col = db[channel]
    
    def refresh():
        file_content = repository.get_contents('held_k.txt')
        key = file_content.decoded_content.decode()
        en_key = Fernet(key)
        msgs = []
        line = 0.0
        line2 = 0
        msg_box.delete(0.0,"end")
        for i in col.find({}, {"_id": 0, "message": 1, "username": 1, "time": 1}):
            u_name = en_key.decrypt(i["username"])
            m_recv = en_key.decrypt(i["message"])
            dt_recv = en_key.decrypt(i["time"])
                
            u_name = str(u_name)[2:]
            u_name = u_name[:-1]
            m_recv = str(m_recv)[2:]
            m_recv = m_recv[:-1]
            dt_recv = str(dt_recv)[13:]
            dt_recv = dt_recv[:-8]

            msgs.append(f"{u_name}({dt_recv}): {m_recv} \n")
            msg_box.insert(line, msgs[line2])
            line+=1
            line2+=1
            msg_box['yscrollcommand'] = scrollbar1.set  
        mw.after(991,refresh)
    
    def send():
        col = db[channel]
        message = message_e.get()
        
        if message == "":
            print("Please enter a message")
        else:   
            message_e.delete(0, int(len(message))+1)
            sent = datetime.datetime.now()
            try:
                m_send = {"username": en_key.encrypt(bytes(usr, encoding="utf-8")), 
                        "message": en_key.encrypt(bytes(message, encoding="utf-8")),
                        "time": en_key.encrypt(bytes(str(sent), encoding="utf-8"))
                }
            except TypeError:
                print("Please enter a message")
            col = col.insert_one(m_send)
        
    message_b = tkinter.Button(mw, text="send", command=send)
    channel_l = tkinter.Label(mw, text=f"connected to {channel}")
    
    message_e.place(x=1,y=372, width=628, height=28)
    message_b.place(x=625,y=371,height=30,width=40)
    msg_box.place(x=0,y=0)
    scrollbar1.place(x=645,y=0, height=300)
    
    refresh()
    
    mw.mainloop()


def login():
    lw = tkinter.Tk()
    lw.title("Login")
    lw.geometry("300x300")
    key_status = tkinter.IntVar()
    # 0 = unchecked
    # 1 = checked
    
    u_ent = tkinter.Entry(lw)
    u_lab = tkinter.Label(lw, text="username:")
    p_ent = tkinter.Entry(lw)
    p_lab = tkinter.Label(lw, text="password:")
    p_ent.config(show="*")
    
    def p_hide():
        if key_status.get() == 0:
            p_ent.config(show="*")
        else:
            p_ent.config(show="")
    
    key_visable = tkinter.Checkbutton(lw, text="show", variable=key_status, onvalue=1, offvalue=0, command=p_hide)
    
    def check_credentials():
        global usr
        global psw
        global channel
        
        usr = u_ent.get()
        psw = p_ent.get()
        channel = channel_e.get()
        
        try:
            client = pymongo.MongoClient(f"mongodb+srv://{usr}:{psw}@messagehost.r9loud3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
            db = client["msgs"]
            col = db["login-log"]
                
            current_time = datetime.datetime.now()
            user_details = {
                "DateTime": current_time,
                "username": usr,
                "software info": software_version
            }
            
            x = col.insert_one(user_details)
            
            messageWin()
            
        except pymongo.errors.OperationFailure:
            print("Bad auth")
        except pymongo.errors.InvalidURI:
            print("Please enter login details")
        except pymongo.errors.ConfigurationError:
            print("Missing username or password. fix this")
            
    def login_help():
        lh = tkinter.Tk()
        lh.title("Login help")
        lh.geometry("300x300")
        
        help_lab = tkinter.Label(lw, text='''Bad auth: either details incorrect or you dont have an account. contact xypn6#6438 to be added or change password''')
        help_lab.place(x=0,y=0)
        
        lh.mainloop()
    
    channel_e = tkinter.Entry(lw)
    channel_l = tkinter.Label(lw, text="channel:")
    
    c_check = tkinter.Button(lw, text="login", command=check_credentials)
    help_b = tkinter.Button(lw, text="help", command=login_help)
    
    u_lab.place(x=0,y=0)
    u_ent.place(x=62,y=2)
    p_lab.place(x=0,y=20)
    p_ent.place(x=62,y=22)
    channel_l.place(x=0,y=40)
    channel_e.place(x=62,y=42)
    
    key_visable.place(x=190,y=20)
    
    c_check.place(x=0,y=62)
    help_b.place(x=38,y=62)
    
    lw.mainloop()
    
login()