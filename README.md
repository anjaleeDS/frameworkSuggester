# Decision-Making Framework Suggester

A web application that suggests appropriate decision-making frameworks based on a user's situation, and helps them apply these frameworks to make better decisions.

## Overview

The Framework Suggester uses AI agents to analyze a user's situation and recommend the most appropriate decision-making frameworks. It then provides detailed explanations, application guidance, and comparative analysis to help users make informed decisions.

## Features

- **Framework Suggestions**: Get personalized framework recommendations based on your specific situation
- **Detailed Explanations**: Learn how each framework works, when to use it, and its limitations
- **Application Guidance**: Receive step-by-step guidance on applying a framework to your situation
- **Framework Comparison**: Compare multiple frameworks to determine which is best for your needs

## Agent Architecture

The application uses a multi-agent system to provide specialized functionality:

### BaseAgent

The foundation for all agents in the system. It handles:
- API authentication and communication with language models
- Response processing and error handling
- Configuration management (model selection, token limits)

### FrameworkSuggesterAgent

Suggests appropriate decision-making frameworks based on user input. This agent:
- Analyzes the user's situation to understand their decision-making needs
- Identifies frameworks that would be most helpful for their specific context
- Provides a curated list with descriptions and explanations of relevance

### FrameworkExplainerAgent

Provides comprehensive information about specific frameworks. This agent:
- Explains how the framework works in detail
- Provides step-by-step instructions for applying the framework
- Lists examples of when the framework is most effective
- Identifies potential limitations or challenges

### FrameworkApplicationAgent

Guides users through applying a framework to their specific situation. This agent:
- Provides tailored questions to gather necessary information
- Creates a structured template for organizing analysis
- Offers guidance on interpreting results

### FrameworkComparisonAgent

Compares multiple frameworks in the context of the user's situation. This agent:
- Analyzes the relative strengths and weaknesses of each framework
- Provides a comparative analysis of features and applicability
- Makes recommendations on which framework(s) would be most effective

## API Endpoints

The application provides the following API endpoints:

- **POST /parse**: Suggests frameworks based on user input
- **POST /explain**: Provides detailed explanations of specific frameworks
- **POST /apply**: Offers guidance on applying frameworks to specific situations
- **POST /compare**: Compares multiple frameworks for a specific situation

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and navigate to `http://127.0.0.1:5000/`

## Usage

1. Enter a description of your situation or decision-making challenge
2. Review the suggested frameworks
3. Click "Explain in Detail" to learn more about a framework
4. Click "Apply to My Situation" to get guidance on using a framework
5. Click "Compare All Frameworks" to see a comparative analysis

## Example Scenarios

The application works well for various decision-making scenarios, such as:

- Career decisions (job changes, education choices)
- Business strategy (market entry, product development)
- Personal finance (investments, major purchases)
- Team management (reorganizations, conflict resolution)
- Life choices (relocations, relationship decisions)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 