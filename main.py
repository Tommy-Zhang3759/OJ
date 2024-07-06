from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.parse
import OJ
import os
from pathlib import Path

# Initialize the OJ service
oj = OJ.OJService()
oj.addTask("z123456789", "Code is here")
oj.statrOJServer() # start OJ service
print(oj.__taskList__[0].time)

# HTTP APIs class
class HTTPApis:
    @classmethod
    def judgeReq(cls, zid, code):
        try:
            oj.addTask(zid=zid, code=code)
        except:
            raise "Fail to add an OJ Task"
        return 

BASE_DIRECTORY = "./webRoot"

# HTTP request handler class
class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.response()
        
    def do_POST(self):
        self.response()

    def response(self):
        parsedURL = urllib.parse.urlparse(self.path)
        path = Path(parsedURL.path)
        pathLev = path.parts # Path levels
        queryDict = urllib.parse.parse_qs(parsedURL.query) # Query dictionary
        
        if os.path.isfile(BASE_DIRECTORY + parsedURL.path):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(BASE_DIRECTORY + parsedURL.path, 'rb') as file:
                self.wfile.write(file.read())

        elif os.path.isfile(BASE_DIRECTORY + parsedURL.path + ".html"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(BASE_DIRECTORY + parsedURL.path + ".html", 'rb') as file:
                self.wfile.write(file.read())

        elif os.path.isfile(BASE_DIRECTORY + parsedURL.path + "/index.html"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(BASE_DIRECTORY + parsedURL.path + "/index.html", 'rb') as file:
                self.wfile.write(file.read())

        elif self.logic(pathLev):
            return
        
        else:

            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def logic(self, path):
        match path:
            case ('\\', 'api', 'judgeReq'):
                print(self.request)
                HTTPApis.judgeReq("z1234567", "print(\"Hello\")")
                return True
            case _:
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