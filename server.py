import http.server
import sqlite3
import json
import time
import bcrypt

SESS_COOKIE_NAME = 'sessionID'

# ConnectedClient Class
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

# Global session and database connection
sessions = {}
DB_CONN = sqlite3.connect("mydatabase.db")

# Request Handler Class
class customRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.DB_CONN = DB_CONN
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/home':
            self.path = '/index.html'
            super().do_GET()
        elif self.path == '/repos':  # Endpoint to fetch all repositories
            self.get_repositories()
        elif self.path == '/test_db_connection':  # Test database connection
            self.test_database_connection()
        else:
            super().do_GET()
            print(f"Received GET request for path: {self.path}")

    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/create_repo':  # Endpoint to create a repository
            self.create_repository()
        else:
            super().do_POST()

    
    def test_database_connection(self):
        """Test the connection to the SQLite database."""
        try:
            cursor = self.DB_CONN.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            # Send the list of tables as a response
            self.respond_with_json({"tables": [table[0] for table in tables]})
        except Exception as e:
            self.respond_with_json({"error": str(e)}, status_code=500)

    def get_repositories(self):
        """Fetch all repositories from the database."""
        try:
            cursor = self.DB_CONN.cursor()
            cursor.execute("SELECT RepoID, RepoName FROM Repository")
            repos = [{"RepoID": row[0], "RepoName": row[1]} for row in cursor.fetchall()]
            self.respond_with_json(repos)
        except Exception as e:
            self.respond_with_json({"error": str(e)}, status_code=500)

    def create_repository(self):
        """Create a new repository."""
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        try:
            cursor = self.DB_CONN.cursor()
            cursor.execute(
                "INSERT INTO Repository (RepoID, DateCreated, RepoName, collabLeader, IsPublic) "
                "VALUES (?, datetime('now'), ?, ?, ?)",
                (post_data["RepoID"], post_data["RepoName"], post_data["collabLeader"], post_data["IsPublic"])
            )
            self.DB_CONN.commit()
            self.respond_with_json({"message": "Repository created successfully"})
        except Exception as e:
            self.respond_with_json({"error": str(e)}, status_code=500)

 
 
    def respond_with_json(self, data, status_code=200):
        """Helper method to send JSON responses."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


if __name__ == '__main__':
    PORT = 8042
    server = http.server.HTTPServer(('localhost', PORT), customRequestHandler)
    print(f"Server running on port {PORT}")
    print("http://127.0.0.1:" + str(PORT))
    server.serve_forever() 
