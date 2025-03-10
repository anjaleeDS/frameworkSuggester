from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

def parse_response(response_content, num_frameworks):
    try:
        frameworks = json.loads(response_content)
        if num_frameworks < 1 or num_frameworks > 3:
            return {"error": "Please select a number between 1 and 3."}
        
        selected_frameworks = frameworks[:num_frameworks]
        return selected_frameworks

    except json.JSONDecodeError as e:
        return {"error": str(e)}

@app.route('/parse', methods=['POST'])
def parse():
    data = request.json
    print("Received data:", data)  # Log the received data

    if not data:
        print("No data received.")
        return jsonify({"error": "No data received"}), 400  # Return an error if no data is received

    response_content = data.get('response')
    num_frameworks = data.get('num_frameworks', 3)  # Default to 3 if not provided

    print("Response content:", response_content)  # Log the response content
    print("Number of frameworks requested:", num_frameworks)  # Log the number of frameworks

    frameworks = parse_response(response_content, num_frameworks)
    
    if isinstance(frameworks, dict) and "error" in frameworks:
        print("Error in parsing response:", frameworks)
        return jsonify(frameworks), 400  # Return error if parsing fails

    print("Parsed frameworks:", frameworks)  # Log the parsed frameworks
    return jsonify(frameworks)

if __name__ == '__main__':
    app.run(debug=True)
