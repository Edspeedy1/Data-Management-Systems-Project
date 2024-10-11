import http.server

PORT = 8042

class customRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/home':
            self.path = '/index.html'
        self.path = "/dist" + self.path
        print(self.path)
        return super().do_GET()
    
    def do_POST(self):
        pass

with http.server.HTTPServer(("", PORT), customRequestHandler) as httpd:
    print("serving at port", PORT)
    print("http://localhost:" + str(PORT))
    httpd.serve_forever()