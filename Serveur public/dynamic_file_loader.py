from mimetypes import guess_type

def load_file(filepath,params,headers,cookies,user):
    if filepath.endswith("/"):
        suffixe="index.html"
    else:
        suffixe=""
    try:
        with open("WEB"+filepath+suffixe,"rb")as f:
            ctn=f.read()
    except FileNotFoundError:
        with open("WEB/404.html","rb")as f:
            ctn=f.read()
        return {"http-code":404,"headers":{"Content-Type":"text/html","Content-Length":str(len(ctn))},"body":ctn}
    if ctn.startswith(b"####dynamic_file%%"):
        code=ctn.split(b"####fin%%")[0]
        pages=ctn.split(b"####fin%%")[1].split(b"####page_suivante%%")
        results={}
        exec(code,{"params":params,"headers":headers,"cookies":cookies,"user":user,"pages":pages,"results":results})
    else:
        results={"body":ctn}
    #si le fichier ne précise pas un code http, on met 200 (OK) par défaut
    if not "http-code" in results:
            results["http-code"]=200
    #mise en place des headers par défaut
    if not "headers" in results:
        results["headers"]={}
    if not "Connection" in results["headers"]:
        results["headers"]["Connection"]="Close"
    if "body" in results:
        if not "Content-Type" in results["headers"]:
            file_type=guess_type(filepath)
            if file_type:
                results["headers"]["Content-Type"]=file_type
        if not "Content-Length" in results["headers"]:
            results["headers"]["Content-Length"]=str(len(results["body"]))
    else:
        results["body"]=b""
    return results
