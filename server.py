import http.server
import bcrypt
import random
import sqlite3
import time
import json
import os

PORT = 8045
SESS_COOKIE_NAME = "project-forge-session-id"


class ConnectedClient:
    def __init__(self, username, sessionID):
        self.username = username
        self.sessionID = sessionID
        self.lastActiveTime = time.time()
    
    def __str__(self):
        return f"username: {self.username}, sessionID: {self.sessionID}, lastActiveTime: {self.lastActiveTime}"
    def __repr__(self):
        return self.__str__()

    def update_last_active_time(self):
        self.lastActiveTime = time.time()

sessions = {}
DB_CONN = sqlite3.connect("mydatabase.db")

class customRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.DB_CONN = DB_CONN
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '/home':
            self.path = '/index.html'
        if self.path == '/favicon.ico':
            return super().do_GET()
        self.path = "/dist" + self.path
        print(self.path)
        return super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        cookie_header = self.headers.get('Cookie')

        if cookie_header:
            cookie = cookie_header.split(';')
            for c in cookie:
                if c.strip().startswith(SESS_COOKIE_NAME) and c.strip().split('=')[1] in sessions:
                    session = c.strip().split('=')[1]
                    username = sessions[session].username
                    sessions[session].update_last_active_time()
                    break

        if self.path == '/login':
            data = json.loads(post_data)
            self.login(data['username'], data['password'])
        if self.path == '/addCollab':
            data = json.loads(post_data)
            change=False
            self.addCollab(data['username'], data['RepoID'], data['accessLevel'],change)
        if self.path == '/editCollab':
            data = json.loads(post_data)
            change=True
            self.addCollab(data['username'], data['RepoID'], data['accessLevel'],change)   
            
    def addCollab(self,username,RepoID,accessLevel,change):   
        #accessLevel 0 is viewer and 1 is editor
        query = "SELECT LastLogin FROM securityInfo WHERE UserName=?"
        lastActive=self.send_SQL_query(query,(username,))
        if change:
            query = 'UPDATE INTO Collaborator (UserName, RepoID,LastLogin,accessLevel) VALUES (?, ?, ?, ?)'
        else:
            query = 'INSERT INTO Collaborator (UserName, RepoID,LastLogin,accessLevel) VALUES (?, ?, ?, ?)'
        self.send_SQL_query(query,(username,RepoID,lastActive,accessLevel))
        self.send_json_response(200, {'success': True})
        
    def login(self, username, password):
        username = username.strip()

        # Check if username already exists
        usernamePass = self.send_SQL_query('SELECT * FROM securityInfo WHERE UserName = ? COLLATE NOCASE', (username,), get=True, fetchAll=False)

        print(usernamePass) 
        if usernamePass is not None:
            stored_hashed_password = usernamePass[1]
            # check if password is correct
            if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password): 
                self.send_json_response(400, {'error': 'Incorrect password'})
                return 
            else: # login successful
                sessionID = random.randbytes(32).hex()
                sessions[str(sessionID)] = ConnectedClient(username, sessionID)
                self.send_json_response(200, {'success': True}, {'Set-Cookie': f"{SESS_COOKIE_NAME}={sessionID}; HttpOnly"})
                return 

        else: # new account creation
            print("making new account")
            hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            self.send_SQL_query('INSERT INTO securityInfo (UserName, passw) VALUES (?, ?)', (username, hashedPassword))
            self.DB_CONN.commit()
            # initialize anything needed for a new account

            # create a new session
            sessionID = random.randbytes(32).hex()
            sessions[str(sessionID)] = ConnectedClient(username, sessionID)
            self.send_json_response(200, {'success': True}, {'Set-Cookie': f"{SESS_COOKIE_NAME}={sessionID}; HttpOnly"})

    def send_json_response(self, status_code, data, extra_headers=None):
        self.send_response(status_code)
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def send_SQL_query(self, query, params, get=False, fetchAll=True):
        try:
            cursor = self.DB_CONN.cursor()
            cursor.execute(query, params)
            if get:
                if fetchAll:
                    return cursor.fetchall()
                else:
                    return cursor.fetchone()
        finally:
            if not get:
                self.DB_CONN.commit()
            cursor.close()

with http.server.HTTPServer(("", PORT), customRequestHandler) as httpd:
    print("serving at port", PORT)
    print("http://127.0.0.1:" + str(PORT))
    httpd.serve_forever()