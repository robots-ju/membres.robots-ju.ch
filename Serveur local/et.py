import socket
import time
#import pickle
cnx_p=socket.socket()
cnx_p.bind(("",63714))
cnx_p.listen(1)

cnx,infos=cnx_p.accept()
while 1:
    
    cmd=cnx.recv(1024)
    print(cmd)
    if cmd[:3]==b"GET":
        id=cmd[3:]
        print(id)
        if id==b"411C98AD":
            cnx.send(b"Gael Fleury")
        else:
            cnx.send(b"invalid ID")

        #with open("database.db","rb")as f:
        #    db=pickle.Unpickler(f).load()
        #cnx.send(db.get(id,b"invalid ID"))
    time.sleep(0.01)
    print('-')
cnx.close()