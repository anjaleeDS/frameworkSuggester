# How to Run the Framework Suggester Application

This guide will walk you through setting up and running the Framework Suggester application on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)
- A modern web browser (Chrome, Firefox, Safari, or Edge)

## Step 1: Clone or Download the Repository

If you're using Git:
```bash
git clone <repository-url>
cd <repository-directory>
```

Or download and extract the ZIP file from the repository.

## Step 2: Set Up a Virtual Environment (Recommended)

Creating a virtual environment helps keep dependencies isolated:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

## Step 4: Set Up Your OpenAI API Key

Create a `.env` file in the root directory of the project:

```bash
touch .env
```

Open the `.env` file in a text editor and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual OpenAI API key. You can obtain an API key by signing up at [OpenAI's platform](https://platform.openai.com/).

## Step 5: Run the Application

Start the Flask server:

```bash
python app.py
```

You should see output similar to:
```
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

## Step 6: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

You should see the Framework Suggester interface.

## Step 7: Using the Application

1. **Enter Your Situation**:
   - In the text area, describe your decision-making challenge or situation
   - Click "Get Frameworks" to receive recommendations

2. **Explore Frameworks**:
   - Review the suggested frameworks
   - Click "Explain in Detail" to learn more about a specific framework
   - Click "Apply to My Situation" to get guidance on using a framework

3. **Compare Frameworks**:
   - If multiple frameworks are suggested, you can click "Compare All Frameworks" to see a comparative analysis

## Troubleshooting

### API Key Issues
If you see errors related to authentication:
- Verify your API key is correct in the `.env` file
- Ensure the `.env` file is in the root directory of the project
- Restart the application after making changes to the `.env` file

### Package Installation Issues
If you encounter errors during package installation:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Port Already in Use
If port 5000 is already in use, you can modify the port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to an available port
```

### JSON Parsing Errors
If you see JSON parsing errors in the console:
- This is usually due to the LLM not returning properly formatted JSON
- Try submitting your query again
- If the issue persists, check the server logs for the raw response

## Development Notes

- The application uses Flask for the backend and vanilla JavaScript for the frontend
- All styles are in `static/styles.css`
- Frontend logic is in `static/script.js`
- Agent definitions are in `agents.py`
- Main application logic is in `app.py`

## Shutting Down

To stop the application, press `CTRL+C` in the terminal where the Flask server is running.

To deactivate the virtual environment:
```bash
# On Windows/macOS/Linux
deactivate
```
