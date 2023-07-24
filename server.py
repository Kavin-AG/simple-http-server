import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import base64
import urllib.parse
import html
import sys
import socket

IP_ADDRESS = '0.0.0.0'  # Listen on all available network interfaces
PORT = 8000

# Replace 'my_folder' with the name of your folder containing the files you want to serve.
BASE_DIRECTORY = os.path.join(os.getcwd(), 'my_folder')

# Authentication credentials (for demonstration purposes only).
USERNAME = 'admin'
PASSWORD = 'password'

# getting system ip address
def get_ip_address():
    try:
        # Get the local host name.
        host_name = socket.gethostname()

        # Get the IP address corresponding to the local host name.
        ip_address = socket.gethostbyname(host_name)

        return ip_address
    except socket.error as e:
        print(f"Error while getting the IP address: {e}")
        return None
    
ip = get_ip_address()

# Custom request handler class with authentication and alphabetical sorting.
class CustomHandler(SimpleHTTPRequestHandler):
    def do_authenticate(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Login Required"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # Check for authentication headers.
        if 'Authorization' not in self.headers:
            self.do_authenticate()
            return

        # Check the authentication credentials.
        auth_header = self.headers['Authorization']
        if not auth_header.startswith('Basic '):
            self.do_authenticate()
            return

        encoded_credentials = auth_header[len('Basic '):].strip()
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)

        if username != USERNAME or password != PASSWORD:
            self.do_authenticate()
            return

        # If authenticated, proceed with the file serving.
        super().do_GET()

    def list_directory(self, path):
        # Override the default directory listing to sort entries alphabetically.
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path, errors='surrogatepass')
            displaypath = html.escape(displaypath, quote=False)
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % displaypath

        # Add custom CSS styles for dark theme and text colors.
        style = """
        <style>
        body {
            background-color: #212121;
            color: #fff;
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
            margin-top: 30px;
            margin-bottom: 30px;
        }
        li {
            list-style-type: none;
            padding: 5px;
            border-bottom: 1px solid #444;
        }
        a {
            color: #00bcd4;
            text-decoration: none;
        }
        a:hover {
            color: #fff;
            background-color: #00bcd4;
            padding: 5px;
            border-radius: 5px;
        }
        </style>
        """

        r.append('<!DOCTYPE html>')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>' % title)
        r.append(style)  # Add the custom CSS styles to the head section.
        r.append('</head>\n<body>')
        r.append('<h1>%s</h1>' % title)
        r.append('<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append '/' for directories or '@' for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
            # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>'
                     % (urllib.parse.quote(linkname, errors='surrogatepass'),
                        html.escape(displayname, quote=False)))
        r.append('</ul>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, errors='surrogateescape')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

def run_server():
    # Use the custom handler for requests.
    handler = CustomHandler

    # Bind the server to the IP address and port.
    server = HTTPServer((IP_ADDRESS, PORT), handler)

    print(f"Serving at http://{ip}:{PORT}/")
    try:
        # Start the server, which will keep running until interrupted.
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()

if __name__ == "__main__":
    run_server()
