import config from './config.js'; // Import the config file

document.getElementById('submitBtn').addEventListener('click', async () => {
    const inputText = document.getElementById('inputText').value;
    const resultDiv = document.getElementById('result');

    // Clear previous results
    resultDiv.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch('http://127.0.0.1:5000/parse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                response: JSON.stringify([
                    { name: "SWOT Analysis", description: "A framework for identifying strengths, weaknesses, opportunities, and threats.", strengths: "Helps in strategic planning." },
                    { name: "Decision Matrix", description: "A tool for evaluating and prioritizing options based on specific criteria.", strengths: "Provides a clear comparison." },
                    { name: "Cost-Benefit Analysis", description: "A method for comparing the costs and benefits of different choices.", strengths: "Helps in financial decision-making." }
                ]),
                num_frameworks: 2 // Change this as needed
            }),
        });

        if (response.ok) {
            const data = await response.json();
            
            // Validate JSON format
            if (!validateJSON(JSON.stringify(data))) {
                resultDiv.innerHTML = '<p>Error: Invalid JSON format received.</p>';
                return;
            }

            resultDiv.innerHTML = `<h2>Frameworks:</h2>`;
            data.forEach(framework => {
                resultDiv.innerHTML += `
                    <div>
                        <h3>${framework.name}</h3>
                        <p>${framework.description}</p>
                        <p><strong>Strengths:</strong> ${framework.strengths}</p>
                    </div>
                `;
            });
        } else {
            const errorData = await response.json();
            resultDiv.innerHTML = `<p>Error: ${errorData.error}</p>`;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        resultDiv.innerHTML = '<p>Error retrieving response. Please try again.</p>';
    }
});

let selectedFramework = null; // Variable to store the selected framework

function selectFramework(frameworkName) {
    selectedFramework = frameworkName; // Save the selected framework
    alert(`You have selected: ${frameworkName}`);
    
    // Show the NEXT button
    document.getElementById('nextButton').style.display = 'block';
}

function goToNext() {
    if (selectedFramework) {
        alert(`Proceeding with: ${selectedFramework}`);
        // Add logic here to handle what happens next
    } else {
        alert('Please select a framework first.');
    }
}

function parseFrameworks(responseContent) {
    try {
        // First parse the string to get a JSON string
        const jsonString = JSON.parse(responseContent);
        // Then parse the JSON string to get the actual array
        const frameworksArray = JSON.parse(jsonString);
        return frameworksArray;
    } catch (error) {
        console.error('Parsing error:', error);
        return null; // Return null if parsing fails
    }
}

const mockResponse = JSON.stringify([
    { name: "SWOT Analysis", description: "A framework for identifying strengths, weaknesses, opportunities, and threats.", strengths: "Helps in strategic planning." },
    { name: "Decision Matrix", description: "A tool for evaluating and prioritizing options based on specific criteria.", strengths: "Provides a clear comparison." },
    { name: "Cost-Benefit Analysis", description: "A method for comparing the costs and benefits of different choices.", strengths: "Helps in financial decision-making." }
]);

const frameworksArray = parseFrameworks(mockResponse);
console.log(frameworksArray); // Test the parser with mock data

function storeResponse(responseContent) {
    // Here you can implement logic to send the response to a backend service
    // For example, using fetch to send it to a Python server
    console.log('Storing response for further processing:', responseContent);
    
    // Example of sending to a backend (assuming you have a server set up)
    /*
    fetch('http://your-backend-endpoint/store', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ response: responseContent })
    })
    .then(res => res.json())
    .then(data => console.log('Response stored:', data))
    .catch(err => console.error('Error storing response:', err));
    */
}

function callPythonParser(responseContent) {
    const numFrameworks = prompt("How many frameworks would you like to see? (1-3):");
    
    fetch('http://localhost:5000/parse', { // Ensure this URL is correct
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ response: responseContent, num_frameworks: parseInt(numFrameworks) })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        return res.json();
    })
    .then(frameworks => {
        // Display the frameworks with descriptions
        resultDiv.innerHTML += `<h2>Parsed Frameworks:</h2>`;
        frameworks.forEach((framework, index) => {
            resultDiv.innerHTML += `
                <div class="framework-box">
                    <h3 class="framework-title">Framework ${index + 1}: ${framework.name}</h3>
                    <p class="framework-description">${framework.description}</p>
                    <p><strong>Strengths:</strong> ${framework.strengths}</p>
                </div>
            `;
        });
    })
    .catch(err => {
        console.error('Error calling Python parser:', err);
        resultDiv.innerHTML += `<p>Error calling Python parser: ${err.message}</p>`;
    });
}

function validateJSON(jsonString) {
    try {
        JSON.parse(jsonString);
        return true; // Valid JSON
    } catch (e) {
        console.error('Invalid JSON format:', e);
        return false; // Invalid JSON
    }
}