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

# if anyone gains access to this pass, it means literally nothing. 
# its a burner acc and has all fake details including spoofed IPs. 
# you gain nothing except the encryption key (reset ever hour lmao) to a service only used for casual banter
# lmao get fucked

git_pass = "[redacted]"

github = Github(git_pass)
user = github.get_user()
repository = user.get_repo(f'k-hold')
file_content = repository.get_contents('held_k.txt')
key = file_content.decoded_content.decode()
print(key)
en_key = Fernet(key)


software_version = {"type": en_key.encrypt(b"CLI"), 
                    "version": en_key.encrypt(b"1.0")}
intro = '''
xypn6 presents...
====================================
     _____  ______ _____  _____
    |  __ \|  ____/ ____|/ ____|
    | |__) | |__ | |    | (___      Private
    |  ___/|  __|| |     \___ \     Encrypted
    | |    | |___| |____ ____) |    Communications
    |_|    |______\_____|_____/     Service

====================================
'''

def message():
    for c in intro:
        print(c, end=''),
        sys.stdout.flush()
        time.sleep(0.005)
    
    print('''
Welcome to <name>
(NOTE: due to current limitations, the program can't automatically update messages. you need to type "r")
use "help" when selecing channel to get a guide to selecing channels
use "help" when making a request to get help with currently available commands
          ''')
    print("====================================")
    channel = input("channel:")
    if channel == "help":
        print('''
              To select a channel, type the name of the channel you want to access.
              use "list" to see a list of currently available channels
              (auto-selecing 'public-channel')
              ''')
        channel = "public"
    elif channel == "login-log":
        print("You do not have access to this channel")
        channel = "public"
    else:
        pass
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@[redacted]/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = client["msgs"]
    col = db[channel]
    print(f"Connected to channel: {channel}")
    print("================================")
    
    while True:
        def refresh():
            file_content = repository.get_contents('held_k.txt')
            key = file_content.decoded_content.decode()
            en_key = Fernet(key)
            
            print(f"Reading messages from: {channel}")
            for i in col.find({}, {"_id": 0, "message": 1, "username": 1}):
                u_name = en_key.decrypt(i["username"])
                m_recv = en_key.decrypt(i["message"])
                
                u_name = str(u_name)[2:]
                u_name = u_name[:-1]
                m_recv = str(m_recv)[2:]
                m_recv = m_recv[:-1]  
                
                print(Fore.BLUE + f"{u_name}:")
                print(Fore.WHITE + f"{m_recv}")
                print("-----------")
                
        def send():
            msg = input("message:")
            m_send = {"username": en_key.encrypt(bytes(username, encoding="utf-8")), 
                      "message": en_key.encrypt(bytes(msg, encoding="utf-8"))}
            x = col.insert_one(m_send)
            
        req = input("request:")
        if req == "r":
            refresh()
        elif req == "s":
            send()
        elif req == "help":
            print('''
                 use "r" to update messages (outputs all messages from channel) 
                 use "s" to send a message
                 use "help" to display this message
                  ''')
        else:
            print("Enter correct request")
        
def login():
    global username
    global password
    
    username = input("username:")
    password = input("password:")
    try:
        client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@[redacted]/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
        db = client["msgs"]
        col = db["login-log"]
            
        current_time = datetime.datetime.now()
        endpoint = 'https://ipinfo.io/json'
        response = requests.get(endpoint, verify=True)

        if response.status_code != 200:
            print('Status:', response.status_code, 'Problem with the request. Exiting.')
            exit()

        data = response.json()
        public_ip = data['ip']
        private_ip = socket.gethostbyname(socket.gethostname())
        hardware_info = {
            "PubIP": en_key.encrypt(bytes(public_ip, encoding="utf-8")),
            "PrivIP": en_key.encrypt(bytes(private_ip, encoding="utf-8")),
            "platform": en_key.encrypt(bytes(platform.platform(), encoding="utf-8")),
            "machine": en_key.encrypt(bytes(platform.machine(), encoding="utf-8")),
            "processor": en_key.encrypt(bytes(platform.processor(), encoding="utf-8")),
            "node": en_key.encrypt(bytes(platform.node(), encoding="utf-8")),
            "release": en_key.encrypt(bytes(platform.release(), encoding="utf-8")),
            "system": en_key.encrypt(bytes(platform.system(), encoding="utf-8")),
            "sys version": en_key.encrypt(bytes(platform.version(), encoding="utf-8"))
            }
             
        user_details = {
            "DateTime": en_key.encrypt(bytes(str(current_time), encoding="utf-8")),
            "username": en_key.encrypt(bytes(username, encoding="utf-8")),
            "software info": software_version,
            "hardware info": hardware_info,
            }
        
        x = col.insert_one(user_details)
        
        message()
    except pymongo.errors.OperationFailure:
        print("Bad auth")
    except pymongo.errors.InvalidURI:
        print("Please enter login details")
    except pymongo.errors.ConfigurationError:
        print("Missing username or password. fix this")
        
login()
