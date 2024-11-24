import http.server
import bcrypt
import random
import sqlite3
import time
import json
import os
from multipart import MultipartParser
from io import BytesIO

PORT = 8045
SESS_COOKIE_NAME = "project-forge-session-id"
UPLOAD_FOLDER = "uploads"

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
        if self.path in ['/', '/index.html', '/login', '/home', '/repo', '/uploadFiles', '/accountInfo', '/createRepo', '/search'] or '/repo/' in self.path or '/search'in self.path:
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

        if self.path == '/api/createRepo':
            content_type = self.headers.get('Content-Type')

            # Ensure the content type is multipart/form-data
            if 'multipart/form-data' in content_type:
                boundary = content_type.split('boundary=')[1]
                parser = MultipartParser(BytesIO(post_data), boundary=boundary)
        
                description = None
                repoName = None
                # Loop through the parts parsed by MultipartParser
                for part in parser.parts():
                    if part.name == 'repoID':  # This should match the form field name in your HTML form
                        repo_id = part.value
                    elif part.name == 'description':  # This should match the form field name for description
                        description = part.value
                    elif part.name == "repoName":
                        repoName = part.value
                        
                     # Call repoCreate with the collected data
                    # Ensure repo_id and description are not None
                    if repo_id and description: 
                        self.repoCreate(username, repo_id, description, repoName)
                    else:
            # Return an error response if repo_id or description is missing
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(b"Error: Missing required fields 'repo_id' or 'description'.")


        if self.path == '/api/login':
            data = json.loads(post_data)
            self.login(data['username'], data['password'])

        if self.path == '/api/changeUI':
            data = json.loads(post_data)
            self.changeUI(
                data['UserName'],                      
                data.get('PrimaryColor'),              
                data.get('SecondaryColor'),            
                data.get('TertiaryColor'),             
                data.get('FontType'),                  
                data.get('Theme'),                     
                data.get('RepoID')                     
            )

        if self.path == '/api/addCollab':
            # fetch('/api/addCollab', { method: 'POST', body: JSON.stringify({ "username":"Ethan27108","RepoID":5,"accessLevel":1}) })
            data = json.loads(post_data)
            change = False
            self.addCollab(data['username'], data['RepoID'], data['accessLevel'], change)

        if self.path == '/api/editCollab':
            # fetch('/api/editCollab', { method: 'POST', body: JSON.stringify({ "username":"Ethan27108","RepoID":5,"accessLevel":0}) })
            data = json.loads(post_data)
            change=True
            self.addCollab(data['username'], data['RepoID'], data['accessLevel'],change)   
            
        if self.path == '/api/getUsersRepos':
            data = json.loads(post_data)
            self.getUsersRepos(username, data['username'] if data['username'] else None)   
        
        if self.path == '/api/searchBar':
            data = json.loads(post_data)
            self.searchBar(data['word']) 
        
        if self.path == '/api/getCollab':
            data = json.loads(post_data)
            self.getCollab(data['RepoID']) 
            
        if self.path == '/api/logout':
            self.logout(session)
             
        # Assuming this is part of your `do_POST` method that handles requests
    
    def repoCreate(self, collabLeader, repoID, description, repoName):
        DateCreated = time.time()
        repoName = repoID
        print(f"Collab Leader: {collabLeader}, RepoID: {repoID}")
        try:
            # Check if the user which collabLeader uses, exists
            user_query = "SELECT UserName FROM User WHERE UserName = ? COLLATE NOCASE"
            userExists = self.send_SQL_query(user_query, (collabLeader,))
            if not userExists:
                print(f"Error: User '{collabLeader}' does not exist.")
                self.send_json_response(205, {"error": "User does not exist"})
                return

            # Check if the RepoID already exists
            repo_query = "SELECT COUNT(*) FROM Repository WHERE RepoID = ?"
            repo_check = self.send_SQL_query(repo_query, (repoID,))
            if repo_check and repo_check[0][0] > 0:
                print(f"Error: Repository ID '{repoID}' already exists.")
                self.send_json_response(409, {'error': 'Repository ID already exists'})
                return
            
            # If the repo doesn't already exist and has no errors. The repo will be created!
            insert_query = """
                INSERT INTO Repository (RepoID, DateCreated, RepoName, collabLeader, Passw, IsPublic, ReadMe)
                VALUES (?, ?, ?, ?, ?, NULL, ?)
                """
              # Ensure repoName is passed correctly (and not a list or any invalid type)
            if isinstance(repoName, list):
                print("Error: repoName should be a string, not a list!")
                return {"success": False, "message": "Invalid repoName type"}

            # Pass the correct parameters to the query, ensuring the number of parameters matches the placeholders
            self.send_SQL_query(insert_query, (repoID, DateCreated, repoName, collabLeader, None, description))


            print(f"Repository created successfully: RepoID={repoID}, CollabLeader={collabLeader}")

            # Send a success response (to let me know that im not going crazy)
            self.send_json_response(201, {
                'success': True,
                'repo_id': repoID,
                'leader': collabLeader,
                'creation_time': DateCreated
            })

        except Exception as e:
            # Log and respond to any unexpected errors
            print(f"Error creating repository: {e}")
            self.send_json_response(500, {'error': 'Internal server error'})
                
    def changeUI(self, username, primary_color, secondary_color, tertiary_color, font_type, theme, repo_id):
        try:
        # Print all received values for debugging
            print(f"Username: {username}")
            print(f"PrimaryColor: {primary_color}")
            print(f"SecondaryColor: {secondary_color}")
            print(f"TertiaryColor: {tertiary_color}")
            print(f"FontType: {font_type}")
            print(f"Theme: {theme}")
            print(f"RepoID: {repo_id}")

        # Insert directly into the database
            insert_query = """
                INSERT INTO UI (UiID, UserName, PrimaryColor, SecondaryColor, TertiaryColor, FontType, Theme, RepoID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            ui_id = random.randint(1, 1000000)  # Generate a unique ID

        # Execute the query
            self.send_SQL_query(
                insert_query,
                (ui_id, username, primary_color, secondary_color, tertiary_color, font_type, theme, repo_id)
            )

        # Send success response
            self.send_json_response(200, {"success": True, "message": "UI settings inserted successfully"})

        except Exception as e:
            print(f"Error in changeUI: {e}")
            self.send_json_response(500, {"error": "Internal server error"})



    def getUsersRepos(self, username, usernameHost):
        if usernameHost and username.lower() == usernameHost.lower() or usernameHost is None:
            query = "SELECT RepoName FROM Repository WHERE CollabLeader = ?"
            params = (username,)
        else:
            query = "SELECT RepoName FROM Repository WHERE CollabLeader = ? and isPublic = True"
            params = (usernameHost,)
        results = self.send_SQL_query(query, params)
        results = list(map(lambda x: {'name': x[0], 'description': '', 'url': f'/repo/{x[0]}'}, results))
        for i in results:
            print(i)
        self.send_json_response(200, {'success': True, "repos":results})
    

    def searchBar(self,word):
        query = "SELECT RepoName FROM Repository WHERE RepoName LIKE ?"
        params = (word+'%',)
        results = self.send_SQL_query(query, params)
        results = list(map(lambda x: {'name': x[0], 'description': '', 'url': f'/repo/{x[0]}'}, results))
        self.send_json_response(200, {'success': True, "repos":results})
            
    def getCollab(self,RepoID):
        query = "SELECT UserName FROM Collaborator WHERE RepoID LIKE ?"
        params=(RepoID,)
        results=self.send_SQL_query(query, params)
        usernames = [row[0] for row in results]
        for i in usernames:
            print(i)
        self.send_json_response(200, {'success': True,"collabs":usernames})
        
    def addCollab(self, username, RepoID, accessLevel, change):   
        # accessLevel 0 is viewer and 1 is editor
        query = "SELECT LastLogin FROM securityInfo WHERE UserName=?"
        lastActive = self.send_SQL_query(query, (username,))
        if lastActive:
            lastActive[0]=lastActive[0][0]
        else:
            lastActive.append(0)
        if change:
            query = "UPDATE Collaborator SET UserName = ?, RepoID = ?, LastLogin = ?, accessLevel = ? WHERE username=?"
            params = (username, RepoID, lastActive[0], accessLevel, username)
        else:
            check_query = "SELECT COUNT(*) FROM Collaborator WHERE UserName = ? AND RepoID = ?"
            exists = self.send_SQL_query(check_query, (username, RepoID))
            print(exists)
            if (exists[0][0] == 0):
                query = 'INSERT INTO Collaborator (UserName, RepoID, LastLogin, accessLevel) VALUES (?, ?, ?, ?)'
                params = (username, RepoID, lastActive[0], accessLevel)
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
            storedHashedPassword = usernamePass[0][1]
            # check if password is correct
            if not bcrypt.checkpw(password.encode('utf-8'), storedHashedPassword): 
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
            self.send_SQL_query('INSERT INTO User (UserName) VALUES (?)', (username,))
            self.DB_CONN.commit()
            # initialize anything needed for a new account

            # create a new session
            sessionID = random.randbytes(32).hex()
            sessions[str(sessionID)] = ConnectedClient(username, sessionID)
            self.send_json_response(200, {'success': True}, {'Set-Cookie': f"{SESS_COOKIE_NAME}={sessionID}; HttpOnly"})

    
    def logout(self, sessionID):
        if sessionID in sessions:
            del sessions[sessionID]
        else:
            self.send_json_response(401, {'error': 'Not logged in'})


    def send_json_response(self, status_code, data, extra_headers=None):
        self.send_response(status_code)
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


    def send_SQL_query(self, query, params=()):
        results = None
        try:
            cursor = self.DB_CONN.cursor()
            cursor.execute(query, params)
            return (results := cursor.fetchall())
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            if not results:
                self.DB_CONN.commit()

with http.server.HTTPServer(("", PORT), customRequestHandler) as httpd:
    print("serving at port", PORT)
    print("http://127.0.0.1:" + str(PORT))
    httpd.serve_forever()