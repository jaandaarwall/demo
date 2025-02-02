import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows cross-origin requests

# Load student marks data
with open('student_marks.json') as f:
    students_data = json.load(f)

# Helper function to get marks by name
def get_marks_by_name(names):
    result = []
    for name in names:
        marks = next((student['marks'] for student in students_data if student['name'] == name), None)
        result.append(marks if marks is not None else "Not found")
    return result
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the API"})

@app.route('/api', methods=['GET'])
def get_marks():
    names = request.args.getlist('name')
    if not names:
        return jsonify({"error": "No names provided"}), 400
    
    marks = get_marks_by_name(names)
    return jsonify({"marks": marks})

if __name__ == '__main__':
    app.run(debug=True)
