from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import json
import os
from dotenv import load_dotenv
import requests  # Assuming you are using requests to call the LLM
from agents import FrameworkSuggesterAgent, FrameworkExplainerAgent, FrameworkApplicationAgent, FrameworkComparisonAgent

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize agents
# These agents handle different aspects of the framework suggestion and application process
suggester_agent = FrameworkSuggesterAgent()  # Suggests appropriate frameworks based on user input
explainer_agent = FrameworkExplainerAgent()  # Provides detailed explanations of specific frameworks
application_agent = FrameworkApplicationAgent()  # Helps apply frameworks to specific situations
comparison_agent = FrameworkComparisonAgent()  # Compares multiple frameworks for a specific situation

@app.route('/')
def home():
    """Serve the main HTML page of the application."""
    return render_template('index.html')  # Serve the HTML file

# Keep the original parse_response function for reference and backward compatibility
def parse_response(response_content, num_frameworks):
    """
    Parse the response from the LLM to extract framework suggestions.
    
    This is the original parsing function that processes raw LLM responses.
    It's kept for reference and backward compatibility.
    
    Args:
        response_content (dict): The raw response from the LLM
        num_frameworks (int): The number of frameworks to return
        
    Returns:
        list or dict: A list of selected frameworks or an error dictionary
    """
    try:
        # Check if 'choices' exists and is not empty
        if 'choices' in response_content and response_content['choices']:
            frameworks_text = response_content['choices'][0].get('text', '')
            frameworks = frameworks_text.split(',')  # Split the text into a list
            
            if num_frameworks < 1 or num_frameworks > 3:
                return {"error": "Please select a number between 1 and 3."}
            
            selected_frameworks = frameworks[:num_frameworks]
            return selected_frameworks
        else:
            return {"error": "No choices returned from LLM."}

    except Exception as e:
        return {"error": str(e)}

@app.route('/parse', methods=['POST'])
def parse():
    """
    Endpoint to parse user input and suggest appropriate frameworks.
    
    This endpoint receives the user's situation description, processes it using
    the FrameworkSuggesterAgent, and returns a list of recommended frameworks.
    
    Request JSON format:
    {
        "response": "User's situation description",
        "num_frameworks": 2  // Optional, defaults to 2
    }
    
    Response JSON format:
    [
        {
            "name": "Framework Name",
            "description": "Framework description",
            "strengths": "Framework strengths for this situation"
        },
        ...
    ]
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        user_input = data.get('response')
        num_frameworks = data.get('num_frameworks', 2)  # Default to 2

        # Log the input data
        print("User Input:")
        print(json.dumps({"User Input": user_input}, indent=4))

        # Use the FrameworkSuggesterAgent to get frameworks
        response = suggester_agent.call_llm([
            {'role': 'system', 'content': suggester_agent.get_system_prompt()},
            {'role': 'user', 'content': user_input}
        ])
        
        # Log the raw response from the LLM
        print("Raw LLM Response:")
        print(json.dumps(response, indent=4))
        
        # Check for errors in the LLM response
        if "error" in response:
            return jsonify({"error": response["error"]}), 400
            
        try:
            # Extract the content from the response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                
                # Log the extracted content
                print("Extracted Content:")
                print(content)
                
                # Parse the JSON from the content
                frameworks = json.loads(content)
                
                # Log the output after parsing
                print("Output after parsing:")
                print(json.dumps(frameworks, indent=4))
                
                # Limit the number of frameworks based on user request
                limited_frameworks = frameworks[:num_frameworks] if isinstance(frameworks, list) else frameworks
                
                return jsonify(limited_frameworks)
            else:
                error_msg = "No valid choices in LLM response"
                print(f"Error: {error_msg}")
                return jsonify({"error": error_msg}), 400
                
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON from LLM response: {str(e)}"
            print(f"Error: {error_msg}")
            print("Content that failed to parse:")
            print(content)
            return jsonify({"error": error_msg}), 400
        except Exception as e:
            error_msg = f"Error processing LLM response: {str(e)}"
            print(f"Error: {error_msg}")
            return jsonify({"error": error_msg}), 400

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg}), 500  # Return the error message

# Keep the original call_llm function for reference, but comment it out
# def call_llm(input_data):
#     api_key = os.getenv('OPENAI_API_KEY')
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json'
#     }
#     
#     # Format the data for the chat model
#     data = {
#         'model': 'gpt-4o-mini',
#         'messages': [
#             {'role': 'system', 'content': 'You are a helpful assistant.'},
#             {'role': 'user', 'content': input_data}
#         ],
#         'max_tokens': 1024
#     }
#     
#     # Log the data being sent to the LLM
#     print("Data sent to LLM:")
#     print(json.dumps(data, indent=4))  # Pretty print the data sent
# 
#     # Change the endpoint to the chat completions endpoint
#     response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
#     
#     # Log the response for debugging
#     print("Response from LLM:")
#     print(json.dumps(response.json(), indent=4))  # Pretty print the raw response text
#     
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": "Failed to call LLM"}

@app.route('/explain', methods=['POST'])
def explain():
    """
    Endpoint to get a detailed explanation of a specific framework.
    
    This endpoint receives a framework name, processes it using the
    FrameworkExplainerAgent, and returns comprehensive information about
    the framework, including how it works, application steps, examples,
    and limitations.
    
    Request JSON format:
    {
        "framework_name": "Name of the framework to explain"
    }
    
    Response JSON format:
    {
        "explanation": "Comprehensive explanation of how the framework works",
        "steps": ["Step 1", "Step 2", ...],
        "examples": ["Example 1", "Example 2", ...],
        "limitations": ["Limitation 1", "Limitation 2", ...]
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        framework_name = data.get('framework_name')
        if not framework_name:
            return jsonify({"error": "No framework name provided"}), 400

        # Log the input data
        print("Explain Request:")
        print(json.dumps({"framework_name": framework_name}, indent=4))

        # Call the LLM directly to get the raw response
        response = explainer_agent.call_llm([
            {'role': 'system', 'content': explainer_agent.get_system_prompt()},
            {'role': 'user', 'content': f"Explain the {framework_name} framework in detail."}
        ])
        
        # Log the raw response from the LLM
        print("Raw LLM Response (Explain):")
        print(json.dumps(response, indent=4))
        
        # Check for errors in the LLM response
        if "error" in response:
            return jsonify({"error": response["error"]}), 400
            
        try:
            # Extract the content from the response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                
                # Log the extracted content
                print("Extracted Content (Explain):")
                print(content)
                
                # Parse the JSON from the content
                explanation = json.loads(content)
                
                # Log the output after parsing
                print("Output after parsing (Explain):")
                print(json.dumps(explanation, indent=4))
                
                return jsonify(explanation)
            else:
                error_msg = "No valid choices in LLM response"
                print(f"Error: {error_msg}")
                return jsonify({"error": error_msg}), 400
                
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON from LLM response: {str(e)}"
            print(f"Error: {error_msg}")
            print("Content that failed to parse:")
            print(content)
            return jsonify({"error": error_msg}), 400
        except Exception as e:
            error_msg = f"Error processing LLM response: {str(e)}"
            print(f"Error: {error_msg}")
            return jsonify({"error": error_msg}), 400

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg}), 500

@app.route('/apply', methods=['POST'])
def apply():
    """
    Endpoint to get guidance on applying a framework to a specific situation.
    
    This endpoint receives a framework name and situation description, processes
    it using the FrameworkApplicationAgent, and returns tailored guidance for
    applying the framework, including questions to consider, a structured template,
    and interpretation guidance.
    
    Request JSON format:
    {
        "framework_name": "Name of the framework to apply",
        "situation": "Description of the user's situation"
    }
    
    Response JSON format:
    {
        "questions": ["Question 1", "Question 2", ...],
        "template": "Structured template for applying the framework",
        "interpretation_guidance": "Guidance on interpreting the results"
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        framework_name = data.get('framework_name')
        user_situation = data.get('situation')
        
        if not framework_name:
            return jsonify({"error": "No framework name provided"}), 400
        if not user_situation:
            return jsonify({"error": "No situation provided"}), 400

        # Log the input data
        print("Apply Request:")
        print(json.dumps({"framework_name": framework_name, "situation": user_situation}, indent=4))

        # Call the LLM directly to get the raw response
        response = application_agent.call_llm([
            {'role': 'system', 'content': application_agent.get_system_prompt()},
            {'role': 'user', 'content': f"Help me apply the {framework_name} framework to this situation: {user_situation}"}
        ])
        
        # Log the raw response from the LLM
        print("Raw LLM Response (Apply):")
        print(json.dumps(response, indent=4))
        
        # Check for errors in the LLM response
        if "error" in response:
            return jsonify({"error": response["error"]}), 400
            
        try:
            # Extract the content from the response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                
                # Log the extracted content
                print("Extracted Content (Apply):")
                print(content)
                
                # Parse the JSON from the content
                application = json.loads(content)
                
                # Log the output after parsing
                print("Output after parsing (Apply):")
                print(json.dumps(application, indent=4))
                
                return jsonify(application)
            else:
                error_msg = "No valid choices in LLM response"
                print(f"Error: {error_msg}")
                return jsonify({"error": error_msg}), 400
                
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON from LLM response: {str(e)}"
            print(f"Error: {error_msg}")
            print("Content that failed to parse:")
            print(content)
            return jsonify({"error": error_msg}), 400
        except Exception as e:
            error_msg = f"Error processing LLM response: {str(e)}"
            print(f"Error: {error_msg}")
            return jsonify({"error": error_msg}), 400

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg}), 500

@app.route('/compare', methods=['POST'])
def compare():
    """
    Endpoint to compare multiple frameworks for a specific situation.
    
    This endpoint receives a list of framework names and a situation description,
    processes it using the FrameworkComparisonAgent, and returns a comparative
    analysis of the frameworks, including their features, pros and cons, and
    a recommendation on which to use.
    
    Request JSON format:
    {
        "framework_names": ["Framework 1", "Framework 2", ...],
        "situation": "Description of the user's situation"
    }
    
    Response JSON format:
    {
        "comparison": "Comparison of the key features of each framework",
        "pros_cons": "Pros and cons of each framework for this situation",
        "recommendation": "Recommendation on which framework(s) would be most effective"
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        framework_names = data.get('framework_names')
        user_situation = data.get('situation')
        
        if not framework_names or not isinstance(framework_names, list):
            return jsonify({"error": "No framework names provided or invalid format"}), 400
        if not user_situation:
            return jsonify({"error": "No situation provided"}), 400

        # Log the input data
        print("Compare Request:")
        print(json.dumps({"framework_names": framework_names, "situation": user_situation}, indent=4))

        # Call the LLM directly to get the raw response
        frameworks_list = ", ".join(framework_names)
        response = comparison_agent.call_llm([
            {'role': 'system', 'content': comparison_agent.get_system_prompt()},
            {'role': 'user', 'content': f"Compare these frameworks for my situation: {frameworks_list}. My situation: {user_situation}"}
        ])
        
        # Log the raw response from the LLM
        print("Raw LLM Response (Compare):")
        print(json.dumps(response, indent=4))
        
        # Check for errors in the LLM response
        if "error" in response:
            return jsonify({"error": response["error"]}), 400
            
        try:
            # Extract the content from the response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                
                # Log the extracted content
                print("Extracted Content (Compare):")
                print(content)
                
                # Parse the JSON from the content
                comparison = json.loads(content)
                
                # Log the output after parsing
                print("Output after parsing (Compare):")
                print(json.dumps(comparison, indent=4))
                
                return jsonify(comparison)
            else:
                error_msg = "No valid choices in LLM response"
                print(f"Error: {error_msg}")
                return jsonify({"error": error_msg}), 400
                
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON from LLM response: {str(e)}"
            print(f"Error: {error_msg}")
            print("Content that failed to parse:")
            print(content)
            return jsonify({"error": error_msg}), 400
        except Exception as e:
            error_msg = f"Error processing LLM response: {str(e)}"
            print(f"Error: {error_msg}")
            return jsonify({"error": error_msg}), 400

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)
