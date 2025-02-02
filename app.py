# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # This allows cross-origin requests

# # Load student marks data
# with open('student_marks.json') as f:
#     students_data = json.load(f)

# # Helper function to get marks by name
# def get_marks_by_name(names):
#     result = []
#     for name in names:
#         marks = next((student['marks'] for student in students_data if student['name'] == name), None)
#         result.append(marks if marks is not None else "Not found")
#     return result
# @app.route('/')
# def index():
#     return jsonify({"message": "Welcome to the API"})

# @app.route('/api', methods=['GET'])
# def get_marks():
#     names = request.args.getlist('name')
#     if not names:
#         return jsonify({"error": "No names provided"}), 400
    
#     marks = get_marks_by_name(names)
#     return jsonify({"marks": marks})

# if __name__ == '__main__':
#     app.run(debug=True)

#####

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Load the data
with open("student_marks.json", "r") as f:
    data = json.load(f)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/api":
            query_params = urllib.parse.parse_qs(parsed_path.query)
            names = query_params.get("name", [])

            marks = [student["marks"] for student in data if student["name"] in names]

            response = json.dumps({"marks": marks})

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # CORS header
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
