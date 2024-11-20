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
DB_CONN = sqlite3.connect("database.db")

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

        if self.path == '/createRepo':
           if username:  # Ensure the user is authenticated
                print (username)
                data = json.loads(post_data)
                repo_name = data.get('repoID', '').strip()
                # collab_leader = data.get('collabLeader', '').strip()
                collab_leader = username  # Use the authenticated username as CollabLeader

                if not repo_name:
                    self.send_json_response(400, {'error': 'Repository name is required'})
                else:
                    self.repoCreate(collab_leader, repo_name)
           # else:
                self.send_json_response(403, {'error': 'Unauthorized or missing session'})

        if self.path == '/login':
            data = json.loads(post_data)
            self.login(data['username'], data['password'])

        if self.path == '/addCollab':
            # fetch('/addCollab', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ "username":"Ethan27108","RepoID":5,"accessLevel":1}) })
            data = json.loads(post_data)
            change = False
            self.addCollab(data['username'], data['RepoID'], data['accessLevel'], change)

        if self.path == '/editCollab':
            # fetch('/editCollab', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ "username":"Ethan27108","RepoID":5,"accessLevel":0}) })
            data = json.loads(post_data)
            change = True
            self.addCollab(data['username'], data['RepoID'], data['accessLevel'], change)   

        
    def repoCreate(self, collabLeader, RepoID):
        DateCreated = time.time()
        print(f"Collab Leader: {collabLeader}, RepoID: {RepoID}")

        try:
        # Check if the user which collabLeader uses, exists
            user_query = "SELECT UserName FROM User WHERE UserName = ? COLLATE NOCASE"
            userExists = self.send_SQL_query(user_query, (collabLeader,), get=True, fetchAll=False)
            if not userExists:
                print(f"Error: User '{collabLeader}' does not exist.")
                self.send_json_response(205, {"error": "User does not exist"})
                return

        # Check if the RepoID already exists
            repo_query = "SELECT COUNT(*) FROM Repository WHERE RepoID = ?"
            repo_check = self.send_SQL_query(repo_query, (RepoID,), get=True, fetchAll=False)
            if repo_check and repo_check[0] > 0:
                print(f"Error: Repository ID '{RepoID}' already exists.")
                self.send_json_response(409, {'error': 'Repository ID already exists'})
                return

        # If the repo doesn't already exist and has no errors. The repo will be created!
            insert_query = "INSERT INTO Repository (RepoID, collabLeader, DateCreated) VALUES (?, ?, ?)"
            self.send_SQL_query(insert_query, (RepoID, collabLeader, DateCreated))
            print(f"Repository created successfully: RepoID={RepoID}, CollabLeader={collabLeader}")

        # Send a success response (to let me know that im not going crazy)
            self.send_json_response(201, {
                'success': True,
                'repo_id': RepoID,
                'leader': collabLeader,
                'creation_time': DateCreated
            })

        except Exception as e:
        # Log and respond to any unexpected errors
            print(f"Error creating repository: {e}")
            self.send_json_response(500, {'error': 'Internal server error'})
        
    def addCollab(self, username, RepoID, accessLevel, change):   
        # accessLevel 0 is viewer and 1 is editor
        query = "SELECT LastLogin FROM securityInfo WHERE UserName=?"
        lastActive = self.send_SQL_query(query, (username,))
        if change:
            query = "UPDATE Collaborator SET UserName = ?, RepoID = ?, LastLogin = ?, accessLevel = ? WHERE username=?"
            params = (username, RepoID, lastActive, accessLevel, username)
        else:
            check_query = "SELECT COUNT(*) FROM Collaborator WHERE UserName = ? AND RepoID = ?"
            exists = self.send_SQL_query(check_query, (username, RepoID))
            print(exists)
            if (exists[0][0] == 0):
                query = 'INSERT INTO Collaborator (UserName, RepoID, LastLogin, accessLevel) VALUES (?, ?, ?, ?)'
                params = (username, RepoID, lastActive, accessLevel)
            else:
                self.send_json_response(201, {'success': False})
                return
        self.send_SQL_query(query, params)
        self.send_json_response(200, {'success': True})
            

    def login(self, username, password):
        username = username.strip()
        # Check if username already exists
        usernamePass = self.send_SQL_query('SELECT UserName, passw FROM securityInfo WHERE UserName = ? COLLATE NOCASE', (username,))

        if usernamePass != []:
            stored_hashed_password = usernamePass[0][1]
            # check if password is correct
            if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password): 
                self.send_json_response(401, {'error': 'Incorrect password'})
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


    def send_SQL_query(self, query, params=()):
        try:
            cursor = self.DB_CONN.cursor()
            cursor.execute(query, params)
            return (results:=cursor.fetchall())
        except Exception as e:
            print(e)
        finally:
            if not results:
                self.DB_CONN.commit()
            cursor.close()

with http.server.HTTPServer(("", PORT), customRequestHandler) as httpd:
    print("serving at port", PORT)
    print("http://127.0.0.1:" + str(PORT))
    httpd.serve_forever()