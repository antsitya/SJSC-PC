#coding=gbk
from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
port=9999

httpd=HTTPServer(('',port),CGIHTTPRequestHandler)
print("Starting simple_http on port:"+str(httpd.server_port))
httpd.serve_forever()