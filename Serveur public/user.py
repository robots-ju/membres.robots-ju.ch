import pickle
import hmac
import hashlib
import time
import base64
import random

with open("secret_key.txt","rb") as f:
    secret_key=f.read()

###################################
#                                 #
#         database entry:         #
#                                 #
#    username, password, rfid,    #
#  presences, present_mnt, admin  #
#                                 #
###################################

def _make_password_hash(password):
    salt=b""
    for i in range(20):
        salt+=bytes([random.randrange(256)])
    return salt+hashlib.sha512(password+salt).digest()

def _verify_password_hash(password,pw_hash):
    salt=pw_hash[:20]
    return hmac.compare_digest(hashlib.sha512(password+salt).digest(),pw_hash[20:])

def _verify_password(username,password):
    with open("database.db","rb") as f:
        unpickler=pickle.Unpickler(f)
        user_found=False
        while not user_found:
            try:
                user=unpickler.load()
            except EOFError:
                return False
            if user[0]==username:
                user_found=True
    return _verify_password_hash(password,user[1])

def create_user_cookie(username,password): # /!\ risque de poser des problèmes à partir de 2106
    if not _verify_password(username,password):
        return b""
    delay=int(time.time())+5400
    username_and_delay=username+delay.to_bytes(4,"big")
    cookie_bin=username_and_delay+hmac.digest(secret_key,username_and_delay,"sha512")
    return base64.b64encode(cookie_bin)
    
def verify_user_cookie(cookie): # /!\ risque de poser des problèmes à partir de 2106
    cookie_bin=base64.b64decode(cookie)
    username_and_delay=cookie_bin[:-64]
    delay=int.from_bytes(username_and_delay[-4:],"big")
    if delay<time.time():
        return b""
    uad_digest=hmac.digest(secret_key,username_and_delay,"sha512")
    if hmac.compare_digest(uad_digest,cookie_bin[-64:]):
        return username_and_delay[:-4]
    else:
        return b""

def change_password(username,old,new):
    if not _verify_password(username,old):
        return False
    database=[]
    with open("database.db","rb")as f:
        unpickler=pickle.Unpickler(f)
        fini=False
        while not fini:
            try:
                database.append(unpickler.load())
            except EOFError:
                fini=True
    for user in database:
        if user[0]==username:
            user[1]=_make_password_hash(new)
            break
    with open("database.db","wb")as f:
        pickler=pickle.Pickler(f)
        for user in database:
            pickler.dump(user)
    return True

__all__=("create_user_cookie","verify_user_cookie","change_password")
