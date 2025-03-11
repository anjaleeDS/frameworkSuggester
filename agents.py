import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class BaseAgent:
    """
    Base agent class that all other agents inherit from.
    
    This class provides the fundamental functionality for interacting with language models.
    It handles authentication, API calls, and response processing, allowing derived agent
    classes to focus on their specific tasks rather than the mechanics of API interaction.
    
    The BaseAgent establishes a consistent interface for all agents in the system and
    centralizes configuration like model selection and token limits.
    """
    
    def __init__(self, model="gpt-4o-mini", max_tokens=1024):
        """
        Initialize the BaseAgent with model configuration.
        
        Args:
            model (str): The name of the language model to use (default: "gpt-4o-mini")
            max_tokens (int): Maximum number of tokens in the response (default: 1024)
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = model
        self.max_tokens = max_tokens
        
    def call_llm(self, messages):
        """
        Call the language model with the given messages.
        
        This method handles the API request to the language model service,
        including authentication and error handling.
        
        Args:
            messages (list): A list of message objects with 'role' and 'content' keys
                            following the chat completion format
        
        Returns:
            dict: The JSON response from the language model API or an error object
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': messages,
            'max_tokens': self.max_tokens
        }
        
        # Log the data being sent to the LLM
        print("Data sent to LLM:")
        print(json.dumps(data, indent=4))
        
        response = requests.post('https://api.openai.com/v1/chat/completions', 
                                headers=headers, 
                                json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to call LLM: {response.text}"}


class FrameworkSuggesterAgent(BaseAgent):
    """
    Agent that suggests decision-making frameworks based on user input.
    
    This agent analyzes the user's situation and recommends appropriate decision-making
    frameworks that would be most helpful for their specific context. It provides
    a curated list of frameworks with descriptions and explanations of why each
    framework is relevant to the user's situation.
    
    The FrameworkSuggesterAgent serves as the entry point for users seeking guidance
    on which decision-making approaches might be most effective for their needs.
    """
    
    def __init__(self, model="gpt-4o-mini", max_tokens=1024):
        """
        Initialize the FrameworkSuggesterAgent with model configuration.
        
        Args:
            model (str): The name of the language model to use (default: "gpt-4o-mini")
            max_tokens (int): Maximum number of tokens in the response (default: 1024)
        """
        super().__init__(model, max_tokens)
        
    def get_system_prompt(self):
        """
        Define the system prompt that instructs the language model how to respond.
        
        This prompt guides the model to act as a decision-making framework expert
        and format its responses in a consistent JSON structure.
        
        Returns:
            str: The system prompt for the language model
        """
        return """You are a decision-making framework expert. Your task is to suggest the most appropriate 
        decision-making frameworks for the user's situation. For each framework, provide:
        1. The name of the framework
        2. A brief description of the framework
        3. The key strengths of the framework for this specific situation
        
        Format your response as a JSON array of objects, with each object containing 'name', 'description', and 'strengths' fields.
        
        IMPORTANT: Your entire response must be valid JSON that can be parsed with json.loads(). Do not include any explanatory text before or after the JSON.
        """
    
    def suggest_frameworks(self, user_input):
        """
        Suggest frameworks based on user input.
        
        This method analyzes the user's situation and returns a list of recommended
        decision-making frameworks that would be most helpful.
        
        Args:
            user_input (str): The user's description of their situation or decision-making challenge
        
        Returns:
            list: A list of framework objects, each containing 'name', 'description', and 'strengths'
                 or a dict with an 'error' key if something went wrong
        """
        messages = [
            {'role': 'system', 'content': self.get_system_prompt()},
            {'role': 'user', 'content': user_input}
        ]
        
        response = self.call_llm(messages)
        
        if "error" in response:
            return response
        
        try:
            # Extract the content from the response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                
                # Log the extracted content
                print("Extracted Content in suggest_frameworks:")
                print(content)
                
                # Parse the JSON from the content
                frameworks = json.loads(content)
                return frameworks
            else:
                return {"error": "No valid choices in LLM response"}
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print("Content that failed to parse:")
            print(content)
            return {"error": f"Failed to parse JSON from LLM response: {str(e)}"}
        except Exception as e:
            return {"error": f"Error processing LLM response: {str(e)}"}


class FrameworkExplainerAgent(BaseAgent):
    """
    Agent that explains a specific framework in detail.
    
    This agent provides comprehensive information about a particular decision-making
    framework, including how it works, step-by-step application instructions,
    example scenarios where it's effective, and potential limitations.
    
    The FrameworkExplainerAgent helps users understand the theoretical foundations
    and practical applications of a framework they're interested in exploring further.
    """
    
    def __init__(self, model="gpt-4o-mini", max_tokens=1024):
        """
        Initialize the FrameworkExplainerAgent with model configuration.
        
        Args:
            model (str): The name of the language model to use (default: "gpt-4o-mini")
            max_tokens (int): Maximum number of tokens in the response (default: 1024)
        """
        super().__init__(model, max_tokens)
        
    def get_system_prompt(self):
        """
        Define the system prompt that instructs the language model how to respond.
        
        This prompt guides the model to provide detailed explanations of decision-making
        frameworks and format its responses in a consistent JSON structure.
        
        Returns:
            str: The system prompt for the language model
        """
        return """You are a decision-making framework expert. Your task is to explain the specified framework
        in detail, including:
        1. A comprehensive explanation of how the framework works
        2. Step-by-step instructions for applying the framework
        3. Examples of when this framework is most effective
        4. Potential limitations or challenges when using this framework
        
        Format your response as a JSON object with 'explanation', 'steps', 'examples', and 'limitations' fields.
        The 'steps', 'examples', and 'limitations' should be arrays of strings.
        
        IMPORTANT: Your entire response must be valid JSON that can be parsed with json.loads(). Do not include any explanatory text before or after the JSON.
        """
    
    def explain_framework(self, framework_name):
        """
        Explain a specific framework in detail.
        
        This method provides comprehensive information about the requested framework,
        including its methodology, application steps, use cases, and limitations.
        
        Args:
            framework_name (str): The name of the framework to explain
        
        Returns:
            dict: A dictionary containing 'explanation', 'steps', 'examples', and 'limitations'
                 or a dict with an 'error' key if something went wrong
        """
        messages = [
            {'role': 'system', 'content': self.get_system_prompt()},
            {'role': 'user', 'content': f"Explain the {framework_name} framework in detail."}
        ]
        
        response = self.call_llm(messages)
        
        if "error" in response:
            return response
        
        try:
            # Extract the content from the response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                
                # Log the extracted content
                print("Extracted Content in explain_framework:")
                print(content)
                
                # Parse the JSON from the content
                explanation = json.loads(content)
                return explanation
            else:
                return {"error": "No valid choices in LLM response"}
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print("Content that failed to parse:")
            print(content)
            return {"error": f"Failed to parse JSON from LLM response: {str(e)}"}
        except Exception as e:
            return {"error": f"Error processing LLM response: {str(e)}"}


class FrameworkApplicationAgent(BaseAgent):
    """
    Agent that helps apply a framework to a specific situation.
    
    This agent guides users through the process of applying a particular decision-making
    framework to their unique situation. It provides tailored questions to gather
    necessary information, a structured template for organizing their analysis,
    and guidance on interpreting the results.
    
    The FrameworkApplicationAgent bridges the gap between theoretical knowledge of
    frameworks and their practical application to real-world scenarios.
    """
    
    def __init__(self, model="gpt-4o-mini", max_tokens=1024):
        """
        Initialize the FrameworkApplicationAgent with model configuration.
        
        Args:
            model (str): The name of the language model to use (default: "gpt-4o-mini")
            max_tokens (int): Maximum number of tokens in the response (default: 1024)
        """
        super().__init__(model, max_tokens)
        
    def get_system_prompt(self):
        """
        Define the system prompt that instructs the language model how to respond.
        
        This prompt guides the model to provide practical application guidance for
        decision-making frameworks and format its responses in a consistent JSON structure.
        
        Returns:
            str: The system prompt for the language model
        """
        return """You are a decision-making framework application expert. Your task is to help the user apply
        the specified framework to their specific situation. Provide:
        1. Tailored questions to gather the necessary information for the framework
        2. A structured template for applying the framework to their situation
        3. Guidance on interpreting the results
        
        Format your response as a JSON object with 'questions', 'template', and 'interpretation_guidance' fields.
        The 'questions' field should be an array of strings.
        
        IMPORTANT: Your entire response must be valid JSON that can be parsed with json.loads(). Do not include any explanatory text before or after the JSON.
        """
    
    def apply_framework(self, framework_name, user_situation):
        """
        Help apply a framework to a specific situation.
        
        This method provides tailored guidance for applying the specified framework
        to the user's unique situation, including relevant questions to consider,
        a structured template for analysis, and interpretation guidance.
        
        Args:
            framework_name (str): The name of the framework to apply
            user_situation (str): The user's description of their situation
        
        Returns:
            dict: A dictionary containing 'questions', 'template', and 'interpretation_guidance'
                 or a dict with an 'error' key if something went wrong
        """
        messages = [
            {'role': 'system', 'content': self.get_system_prompt()},
            {'role': 'user', 'content': f"Help me apply the {framework_name} framework to this situation: {user_situation}"}
        ]
        
        response = self.call_llm(messages)
        
        if "error" in response:
            return response
        
        try:
            # Extract the content from the response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                
                # Log the extracted content
                print("Extracted Content in apply_framework:")
                print(content)
                
                # Parse the JSON from the content
                application = json.loads(content)
                return application
            else:
                return {"error": "No valid choices in LLM response"}
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print("Content that failed to parse:")
            print(content)
            return {"error": f"Failed to parse JSON from LLM response: {str(e)}"}
        except Exception as e:
            return {"error": f"Error processing LLM response: {str(e)}"}


class FrameworkComparisonAgent(BaseAgent):
    """
    Agent that compares multiple frameworks for a specific situation.
    
    This agent analyzes several decision-making frameworks in the context of the user's
    specific situation, highlighting the relative strengths and weaknesses of each.
    It provides a comparative analysis to help users select the most appropriate
    framework for their needs.
    
    The FrameworkComparisonAgent helps users make informed decisions about which
    framework(s) to use when multiple options seem viable.
    """
    
    def __init__(self, model="gpt-4o-mini", max_tokens=1024):
        """
        Initialize the FrameworkComparisonAgent with model configuration.
        
        Args:
            model (str): The name of the language model to use (default: "gpt-4o-mini")
            max_tokens (int): Maximum number of tokens in the response (default: 1024)
        """
        super().__init__(model, max_tokens)
        
    def get_system_prompt(self):
        """
        Define the system prompt that instructs the language model how to respond.
        
        This prompt guides the model to compare multiple decision-making frameworks
        and format its responses in a consistent JSON structure.
        
        Returns:
            str: The system prompt for the language model
        """
        return """You are a decision-making framework comparison expert. Your task is to compare the specified
        frameworks for the user's situation. Provide:
        1. A comparison of the key features of each framework
        2. The pros and cons of each framework for this specific situation
        3. A recommendation on which framework(s) would be most effective and why
        
        Format your response as a JSON object with 'comparison', 'pros_cons', and 'recommendation' fields.
        
        IMPORTANT: Your entire response must be valid JSON that can be parsed with json.loads(). Do not include any explanatory text before or after the JSON.
        """
    
    def compare_frameworks(self, framework_names, user_situation):
        """
        Compare multiple frameworks for a specific situation.
        
        This method analyzes and compares several frameworks in the context of the
        user's situation, highlighting their relative strengths and weaknesses and
        providing a recommendation on which to use.
        
        Args:
            framework_names (list): A list of framework names to compare
            user_situation (str): The user's description of their situation
        
        Returns:
            dict: A dictionary containing 'comparison', 'pros_cons', and 'recommendation'
                 or a dict with an 'error' key if something went wrong
        """
        frameworks_list = ", ".join(framework_names)
        messages = [
            {'role': 'system', 'content': self.get_system_prompt()},
            {'role': 'user', 'content': f"Compare these frameworks for my situation: {frameworks_list}. My situation: {user_situation}"}
        ]
        
        response = self.call_llm(messages)
        
        if "error" in response:
            return response
        
        try:
            # Extract the content from the response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                
                # Log the extracted content
                print("Extracted Content in compare_frameworks:")
                print(content)
                
                # Parse the JSON from the content
                comparison = json.loads(content)
                return comparison
            else:
                return {"error": "No valid choices in LLM response"}
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print("Content that failed to parse:")
            print(content)
            return {"error": f"Failed to parse JSON from LLM response: {str(e)}"}
        except Exception as e:
            return {"error": f"Error processing LLM response: {str(e)}"}


# Example usage
if __name__ == "__main__":
    # Test the FrameworkSuggesterAgent
    suggester = FrameworkSuggesterAgent()
    frameworks = suggester.suggest_frameworks("I'm considering a career change but I'm not sure if I should prioritize salary or work-life balance.")
    print(json.dumps(frameworks, indent=2))