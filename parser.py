import json

def parse_response(response_content, num_frameworks):
    try:
        # Assuming the response is a JSON string
        frameworks = json.loads(response_content)
        
        # Validate the number of frameworks requested
        if num_frameworks < 1 or num_frameworks > 3:
            print("Error: Please select a number between 1 and 3.")
            return
        
        # Process and print the requested number of frameworks
        for framework in frameworks[:num_frameworks]:  # Limit to the requested number of frameworks
            print(f"Framework Name: {framework['name']}")
            print(f"Description: {framework['description']}")
            print(f"Strengths: {framework['strengths']}")
            print()  # Print a newline for better readability

    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)

# Example usage
if __name__ == "__main__":
    # Simulate receiving a response
    mock_response = json.dumps([
        { "name": "SWOT Analysis", "description": "A framework for identifying strengths, weaknesses, opportunities, and threats.", "strengths": "Helps in strategic planning." },
        { "name": "Decision Matrix", "description": "A tool for evaluating and prioritizing options based on specific criteria.", "strengths": "Provides a clear comparison." },
        { "name": "Cost-Benefit Analysis", "description": "A method for comparing the costs and benefits of different choices.", "strengths": "Helps in financial decision-making." }
    ])
    
    # Ask the user how many frameworks they want
    num_frameworks = int(input("How many frameworks would you like to see? (1-3): "))
    parse_response(mock_response, num_frameworks)
