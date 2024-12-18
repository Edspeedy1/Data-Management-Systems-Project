import http.server
import bcrypt
import random
import sqlite3
import time
import json
import os
from multipart import MultipartParser
from io import BytesIO
import mimetypes
import zipfile

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
        if '/api/download/' in self.path:
            return self.downloadFile(self.path)
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

                repo_id = None
                description = None
                repoName = None
                files = []
                # Loop through the parts parsed by MultipartParser
                for part in parser.parts():
                    if part.name == 'repoID':  # This should match the form field name in your HTML form
                        repo_id = part.value
                    elif part.name == 'description':  # This should match the form field name for description
                        description = part.value
                    elif part.name == "repoName":
                        repoName = part.value
                    elif part.name == 'files':
                        try:
                            value = part.value
                        except:
                            value = part.raw
                        files.append({
                            'filename': part.filename,
                            'content_type': part.content_type,
                            'content': value
                        })
                        
                    # Call repoCreate with the collected data
                    # Ensure repo_id and description are not None
                if repo_id and description: 
                    self.repoCreate(username, repo_id, description, repoName, files)
             

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
                data.get('repoID')                     
            )

        if self.path == '/api/getUsername':
            self.send_json_response(200, {'success': True, 'username': username})
        
        if self.path == '/api/getNumberOfRepos':
            results = self.send_SQL_query("SELECT COUNT(*) FROM Repository WHERE collabLeader = ?", (username,))
            self.send_json_response(200, {'success': True, 'number': results[0][0]})

        if self.path == '/api/addCollab':
            data = json.loads(post_data)
            change = False
            self.addCollab(data['username'], data['repoID'], data['accessLevel'], change)

        if self.path == '/api/removeCollab':
            data = json.loads(post_data)
            change = True
            self.removeCollab(data['username'], data['repoID'])   
            
        if self.path == '/api/getUsersRepos':
            data = json.loads(post_data)
            self.getUsersRepos(username, data['username'] if data['username'] else None)   
        
        if self.path == '/api/searchBar':
            data = json.loads(post_data)
            self.searchBar(data['word'], username) 
        
        if self.path == '/api/getCollab':
            data = json.loads(post_data)
            self.getCollab(data['repoID']) 
            
        if self.path == '/api/logout':
            self.logout(session)

        if self.path == '/api/folderCreate':
            data = json.loads(post_data)
            self.folderCreate(data['collabLeader'], data['repoID'], data['folderID'])
        
        if self.path == '/api/repoPublic':
            data = json.loads(post_data)
            self.repoPublic(data['repoID'], data['isPublic'], data['get'])
        
        if self.path == '/api/getRepoDescription':
            data = json.loads(post_data)
            self.getRepoDescription(data['repoID'])

        if self.path == '/api/getFileNames':
            data = json.loads(post_data)
            self.getFileNames(data['repoID'])


        if self.path == '/api/UploadFile':
            content_type = self.headers.get('Content-Type')
            boundary = content_type.split('boundary=')[1]
            parser = MultipartParser(BytesIO(post_data), boundary=boundary)

            repo_id = None
            files = []
            for part in parser.parts():
                    if part.name == 'repoID':  
                        repo_id = part.value
                    elif part.name == 'files':
                        try:
                            value = part.value
                        except Exception as e:
                            value = part.raw
                        files.append({
                            'filename': part.filename,
                            'content_type': part.content_type,
                            'content': value
                        })
                        
            self.UploadFile(repo_id, repo_id, files, sendResponse=True)

    #---------------------------------------------------------------------------

    def getRepoDescription(self, repoID):
        repoID = repoID.replace('%20', ' ')
        repoQuery = "SELECT ReadMe FROM Repository WHERE RepoID = ?"
        result = self.send_SQL_query(repoQuery, (repoID,))      
        # Check if any result is returned
        if not result or len(result) == 0:
            print(f"Error: Repository with RepoID '{repoID}' does not exist.")
            results = {"error": "Repository not found"}
            self.send_json_response(409, {"repoID": repoID, "description": readme, "ERROR": True})
        # Extract the ReadMe from the result
        readme = result[0][0]  # Assuming result is a list of tuples        
        # Send the ReadMe to results
        results = {"repoID": repoID, "description": readme}
        print(f"Results: {results}")
        self.send_json_response(200, {"repoID": repoID, "description": readme})

#-------------------------------------------
        
    def repoPublic(self, repoID, isPublic, get):
        repoID = repoID.replace('%20', ' ')
        print(f"repoID: {repoID}, isPublic: {isPublic}, get: {get}")
        if not get:
            query = "UPDATE Repository SET IsPublic = ? WHERE RepoID = ?"
            self.send_SQL_query(query, (isPublic, repoID))
            self.send_json_response(200, {'success': True, 'isPublic': isPublic})
        else:
            query = "SELECT IsPublic FROM Repository WHERE RepoID = ?"
            results = self.send_SQL_query(query, (repoID,))[0][0]
            self.send_json_response(200, {'success': True, 'isPublic': results})

#-------------------------------------------

    def repoCreate(self, collabLeader, repoID, description, repoName, files):
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
                
            
            # If the repo doesn't already exist and has no errors. The repo will be created!
            insert_query = """
                INSERT INTO Repository (RepoID, DateCreated, RepoName, collabLeader, Passw, IsPublic, ReadMe)
                VALUES (?, ?, ?, ?, ?, NULL, ?)
                """
              # Ensure repoName is passed correctly (and not a list or any invalid type)
            if isinstance(repoName, list):
                print("Error: repoName should be a string, not a list!")
                

            # Pass the correct parameters to the query, ensuring the number of parameters matches the placeholders
            self.send_SQL_query(insert_query, (repoID, DateCreated, repoName, collabLeader, None, description))

            # Call folderCreate for the initial folder creation
            folderID = f"{repoID}"
            result = self.folderCreate(collabLeader, repoID, folderID, files[0])
            if result:
                print(f"Error creating root folder: {result}")
                self.send_json_response(500, {'error': 'Internal server error'})
                return
            
            self.UploadFile(repoID, folderID, files)

            # files_metadata = [{'fileID': f"{folderID}_{file['filename']}"} for file in files] if files else []

            print(f"Repository created successfully: RepoID={repoID}, CollabLeader={collabLeader}")
            # Send a success response (to let me know that im not going crazy)
            self.send_json_response(201, {
                'success': True,
                'repo_id': repoID,
                'leader': collabLeader,
                'creation_time': DateCreated,
                'URL': "repo/" + repoID,
             #   'Files': files_metadata  # Include only fileIDs (metadata) This json response is being VERY annoying
            })

        except Exception as e:
            # Log and respond to any unexpected errors
            print(f"Error creating repository: {e}")
            self.send_json_response(500, {'error': 'Internal server error'})

#-------------------------------------------

    def UploadFile(self, repoID, folderID, files, sendResponse=False):
        folderID = folderID.replace('%20', ' ')
        repoID = repoID.replace('%20', ' ')
        try:
            repo_query = "SELECT RepoID FROM Repository WHERE RepoID = ?"
            repo_result = self.send_SQL_query(repo_query, (repoID,))
            if not repo_result:
                self.send_json_response(404, {'error': 'Repository not found'})
                return

            # Prepare to upload files
            for file in files:
                # Ensure file content is bytes-like
                if isinstance(file['content'], str):
                    file_content = file['content'].encode('utf-8')  # Convert to bytes
                else:
                    file_content = file['content']

                # Generate the storage path
                upload_path = os.path.join(UPLOAD_FOLDER, folderID)
                os.makedirs(upload_path, exist_ok=True)  # Ensure the folder exists

                file_path = os.path.join(upload_path, file['filename'])

                # Save the file content
                with open(file_path, 'wb') as f:
                    f.write(file_content)

                # Record only the file name in the database
                insert_query = """
                    INSERT INTO codeStorage (folderID, repoID, fileID, lastUpdated, fileSuggestions)
                    VALUES (?, ?, ?, ?, NULL)
                """
                fileID = file['filename']  # Use file name as ID
                last_updated = time.time()

                self.send_SQL_query(insert_query, (folderID, repoID, fileID, last_updated))

            print(f"Files uploaded successfully to folder '{folderID}' in repo '{repoID}'.")
            if sendResponse:
                self.send_json_response(200, {'success': True})

        except Exception as e:
            print(f"Error uploading files: {e}")
      


#-------------------------------------------------------
                
              # Assuming this is part of your `do_POST` method that handles requests
    def folderCreate(self, collabLeader, repoID, folderID, fileID):
        dateAdded = time.time()
        print(f"Commencing folder creation... folderID: {folderID}")

        try:
            # Check if the user exists
            user_query = "SELECT UserName FROM User WHERE UserName = ? COLLATE NOCASE"
            userExists = self.send_SQL_query(user_query, (collabLeader,))
            if not userExists:
                print(f"Error: User '{collabLeader}' does not exist.")
                return "User does not exist"
            
        # Check if the folderID already exists
            folder_query = "SELECT COUNT(*) FROM codeStorage WHERE folderID = ?"
            folder_check = self.send_SQL_query(folder_query, (folderID,))
            if folder_check and folder_check[0][0] > 0:
                print(f"Error: Folder ID '{folderID}' already exists.")
                return "Folder ID already exists"

        # If the folder doesn't already exist, create it
            insert_query = "INSERT INTO codeStorage (folderID, repoID, fileID, lastUpdated) VALUES (?, ?, ?, ?, )"
            self.send_SQL_query(insert_query, (folderID, repoID, fileID, dateAdded))
            full_path = os.path.join(UPLOAD_FOLDER, folderID)
            os.makedirs(full_path, exist_ok=True)
            

            print(f"Folder created successfully: FolderID={folderID}, CollabLeader={collabLeader}")

        except Exception as e:
        # Log and respond to any unexpected errors
            print(f"Error creating folder: {e}")
            self.send_json_response(500, {'error': 'Internal server error'})

#------------------------------------------
            
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
        self.send_json_response(200, {'success': True, "repos": results})
    

    def searchBar(self, word, username):
        word = word.replace('%20', ' ')
        query = "SELECT RepoName FROM Repository WHERE RepoName LIKE ? and (isPublic = True or CollabLeader = ?)"
        params = ("%" + word + "%", username)
        results = self.send_SQL_query(query, params)
        results = list(map(lambda x: {'name': x[0], 'description': '', 'url': f'/repo/{x[0]}'}, results))
        print(results)
        self.send_json_response(200, {'success': True, "repos": results})
            
    def getCollab(self,RepoID):
        query = "SELECT UserName FROM Collaborator WHERE RepoID LIKE ?"
        params=(RepoID,)
        results=self.send_SQL_query(query, params)
        usernames = [row[0] for row in results]
        self.send_json_response(200, {'success': True, "collabs": usernames})
        
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
            if (exists[0][0] == 0):
                query = 'INSERT INTO Collaborator (UserName, RepoID, LastLogin, accessLevel) VALUES (?, ?, ?, ?)'
                params = (username, RepoID, lastActive[0], accessLevel)
            else:
                self.send_json_response(201, {'success': False})
                return
        self.send_SQL_query(query, params)
        self.getCollab(RepoID)
            
            
    def removeCollab(self, username, RepoID):
        query = "DELETE FROM Collaborator WHERE UserName = ? AND RepoID = ?"
        params = (username, RepoID)
        self.send_SQL_query(query, params)
        self.getCollab(RepoID)

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


    def getFileNames(self, repoID):
        repoID = repoID.replace('%20', ' ')
        query = "SELECT fileID FROM codeStorage WHERE RepoID = ?"
        params = (repoID,)
        results = self.send_SQL_query(query, params)
        print(repoID, results)
        results = list(map(lambda x: {'name': x[0]}, results))
        self.send_json_response(200, {'success': True, "fileNames":results})


    def downloadFile(self, path):
        # Extract the filename from the URL
        filename = path.split('/download/')[-1].replace('%20', ' ').replace('/', '\\')
        print(filename)
        if '_all\\' in filename:
            filename = filename.replace('_all\\', '')
            print(filename)
            # zip together all files in the folder
            filepath = os.path.join(os.getcwd(), 'uploads', filename)
            zip_path = os.path.join(os.getcwd(), 'uploads', filename + '.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(filepath):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), filepath))

            # Serve the zip file with the correct MIME type
            mimetype, _ = mimetypes.guess_type(zip_path)
            self.send_response(200)
            self.send_header('Content-Type', mimetype or 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}.zip"')
            self.end_headers()

            # Open the zip file and send it in chunks to avoid memory overload
            with open(zip_path, 'rb') as file:
                self.wfile.write(file.read())
            return

        filepath = os.path.join(os.getcwd(), 'uploads', filename)

        if os.path.exists(filepath) and os.path.isfile(filepath):
            # Serve the file with the correct MIME type
            mimetype, _ = mimetypes.guess_type(filepath)
            self.send_response(200)
            self.send_header('Content-Type', mimetype or 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.end_headers()

            # Open the file and send it in chunks to avoid memory overload
            with open(filepath, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "File not found")
        
    
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