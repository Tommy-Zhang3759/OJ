from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.parse
import OJ
import os
from pathlib import Path
import threading
import json

# Initialize the OJ service
oj = OJ.OJService(ojID="oj_demo", databaseRoot="./ojDatabase")
oj.addTask("z123456789", "print(\"Hello OJ!!!\")")
oj.statrOJServer() # start OJ service

# HTTP APIs class
class HTTPApis:
    @classmethod
    def judgeReq(cls, zID, codeFile):
        try:
            task = oj.addTask(zID=zID, codeFile=codeFile) # True or false
        except:
            return {
                "Success": False,
                "Error": task
            }
        return {
            "Success": True,
            "rID": task.rID
        }
    
    @classmethod
    def taskInfo(cls, rID):
        try:
            res = oj.__taskList__[int(rID)].checkTaskInfo() # now, rIDs are continous numbers. update in FUTURE.
            res.testPoints = []
            return {
                "codeFile": res.codeFile,
                "rID": res.rID,
                "problemId": res.problemId,
                "status": OJ.OJService.__task_status_int2str__(res.status),
                "testPoints": res.testPoints,
                "zID": res.zID,
                "time": res.time
            }
        except IndexError: # out of range
            return {
                "Success": False,
                "Error": OJ.SYS_ERR_101
            }



BASE_DIRECTORY = "./webRoot"

# HTTP request handler class
class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.response()
        
    def do_POST(self):
        self.response()


    def response(self):
        parsedURL = urllib.parse.urlparse(self.path)

        queryDict = urllib.parse.parse_qs(parsedURL.query) # Query dictionary


        if parsedURL.path.startswith('/api/'): # is calling an API
            self.handle_api(parsedURL)
            return
        
        if self.serve_static_file(parsedURL.path): # requesting a static file
            return
        
        self.send_response(404) # cannot find the file, neigher API
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"404 Not Found")
    
    def readJsonBody(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            return json.loads(post_data)
        
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return False



    def handle_api(self, parsedURL): # define all the APIs

        match parsedURL.path:
            case "/api/judgeReq": # /api/judgeReq

                data = self.readJsonBody()
                if data == False: return


                zID = data.get("zID")
                codeFile = data.get("codeFile")

                response = HTTPApis.judgeReq(zID, codeFile)
                
                self.send_response(200) # deal with error in FUTRUE
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # print(response)

                self.wfile.write(json.dumps(response).encode())

                return True
            
            case "/api/taskInfo":
                queryDict = urllib.parse.parse_qs(parsedURL.query)
                rID = queryDict['q'][0] # one task once CUTTENTLY

                response = HTTPApis.taskInfo(rID=rID)

                print(response)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                self.wfile.write(json.dumps(response).encode())

                return True            

            case _:
                self.send_response(404) # API cannot be found
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "API Not Found"}).encode())





    def get_content_type(self, file_path):
        ext = os.path.splitext(file_path)[1]
        return {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif'
        }.get(ext, 'application/octet-stream')

    def serve_static_file(self, url_path):
        possible_paths = [
            BASE_DIRECTORY + url_path,
            BASE_DIRECTORY + url_path + "/index.html"
        ]

        for file_path in possible_paths:
            if os.path.isfile(file_path):
                contentType = self.get_content_type(file_path)
                self.send_response(200)
                self.send_header('Content-type', contentType)
                self.end_headers()

                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())

                return True
        return False


# Create and start the multi-threaded HTTP server
httpd = ThreadingHTTPServer(('127.0.0.1', 8080), HttpHandler) 
httpd.serve_forever() # Start HTTP service


"""
Host: localhost:8080
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: "Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
DNT: 1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
"""

"""
from urllib.parse import urlparse

url = 'http://www.example.com/path/to/page?query=123#fragment'
parsed_url = urlparse(url)

print(parsed_url)
# 输出: ParseResult(scheme='http', netloc='www.example.com', path='/path/to/page', params='', query='query=123', fragment='fragment')

print(parsed_url.scheme)   # 输出: 'http'
print(parsed_url.netloc)   # 输出: 'www.example.com'
print(parsed_url.path)     # 输出: '/path/to/page'
print(parsed_url.query)    # 输出: 'query=123'
print(parsed_url.fragment) # 输出: 'fragment'
"""