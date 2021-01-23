import socket
import pickle
cnx_p=socket.socket()
cnx_p.bind(("",63714))
cnx_p.listen(1)
while 1:
    cnx,infos=cnx_p.accept()
    cmd=cnx.recv(1024)
    if cmd[:3]==b"GET":
        id=cmd[3:]
        with open("database.db","rb")as f:
            db=pickle.Unpickler(f).load()
        cnx.send(db.get(id,b"invalid ID"))
        if id in db:
            if db[id][-1]:
                db[id]=db[id][:-1]+b"\0"
            else:
                db[id]=db[id][:-1]+b"\1"
            with open("database.db","wb")as f:
                pickle.Pickler(f).dump(db)
    elif cmd[:3]==b"ADD":
        id_len=cmd[3]
        id=cmd[4:4+id_len]
        with open("database.db","rb")as f:
            db=pickle.Unpickler(f).load()
        if id in db:
            cnx.send(b"ID already in use.")
        else:
            db[id]=cmd[4+id_len:]
            if len(db[id])<3:
                del db[id]
                cnx.send(b"invalid name")
            else:
                cnx.send(b"Added")
            with open("database.db","wb")as f:
                pickle.Pickler(f).dump(db)
    elif cmd[:3]==b"DEL":
        id=cmd[3:]
        with open("database.db","rb")as f:
            db=pickle.Unpickler(f).load()
        if id in db:
            del db[id]
            cnx.send(b"Deleted")
            with open("database.db","wb")as f:
                pickle.Pickler(f).dump(db)
        else:
            cnx.send(b"invalid ID")
    cnx.close()
