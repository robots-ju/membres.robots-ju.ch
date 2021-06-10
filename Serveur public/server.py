from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import ssl
import json
from threading import Thread
from user import *
from dynamic_file_loader import load_file
class MembresRobotsJUHTTPSRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        cookies={}
        for x in self.headers.get("Cookie","").split("; "):
            cookies[x.split("=")[0]]="=".join(x.split("=")[1:])
        if "Cookie" in self.headers:
            del self.headers["Cookie"]
        user=verify_user_cookie(cookies.get("user",""))
        if "user" in cookies:
            del cookies["user"]
        params={}
        if "?" in self.path:
            path=self.path.split("?")[0]
            for x in "?".join(self.path.split("?")[1:]).split("&"):
                params[x.split("=")[0]]="=".join(x.split("=")[1:])
        else:
            path=self.path
        reponse=load_file(path,params,self.headers,cookies,user)
        self.send_response(reponse["http-code"])
        for header in reponse["headers"]:
            self.send_header(header,reponse["headers"][header])
        self.end_headers()
        self.wfile.write(reponse["body"])

    def do_POST(self):
        if self.path=="/login":
            if "Content-Length" in self.headers:
                length=int(self.headers["Content-Length"])
            else:
                self.send_response(411)
                self.end_headers()
                return
            content_json=self.rfile.read(length)
            user_data=json.loads(content_json)
            cookie=create_user_cookie(user_data["username"].encode(),user_data["password"].encode())
            if cookie:
                self.send_response(204)
                self.send_header("Set-Cookie","user="+cookie.decode()+"; SameSite=Strict")
            else:
                self.send_response(401)
            self.end_headers()
            return
        self.send_response(501)
        self.end_headers()

    def redirect(self,location):
        self.send_response(302)
        self.send_header("Location",location)
        self.end_headers()

class RedirectToHTTPSHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header("Location",f"https://membres.robots-ju.ch{self.path}")
        self.end_headers()

class HTTPServerV6(HTTPServer):
    address_family=socket.AF_INET6

class RunHTTPSServer(Thread):
    def __init__(self,HTTPServer):
        self.HTTPServer=HTTPServer
        Thread.__init__(self)
    def run(self):
        server=self.HTTPServer(("",443),MembresRobotsJUHTTPSRequestHandler)
        server.socket=ssl.wrap_socket(server.socket,
                                      keyfile="../../key.pem",
                                      certfile="../../cert.pem",
                                      server_side=True)
        server.serve_forever()

class RunHTTPServer(RunHTTPSServer):
    def run(self):
        server=self.HTTPServer(("",80),RedirectToHTTPSHTTPRequestHandler)
        server.serve_forever()
        
RunHTTPServer(HTTPServer).start()
RunHTTPSServer(HTTPServer).start()
RunHTTPServer(HTTPServerV6).start()
RunHTTPSServer(HTTPServerV6).start()
