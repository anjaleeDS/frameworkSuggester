import config from './config.js'; // Import the config file

/**
 * Main event listener for the submit button.
 * This function handles the initial user input and calls the framework suggester agent.
 */
document.getElementById('submitBtn').addEventListener('click', async () => {
    const inputText = document.getElementById('inputText').value; // Get user input
    const resultDiv = document.getElementById('result');

    // Clear previous results
    resultDiv.innerHTML = '<p>Loading...</p>';

    try {
        // Call the framework suggester agent via the /parse endpoint
        const response = await fetch('http://127.0.0.1:5000/parse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                // Keep the commented mock data for reference
                // response: JSON.stringify([
                //     { name: "SWOT Analysis", description: "A framework for identifying strengths, weaknesses, opportunities, and threats.", strengths: "Helps in strategic planning." },
                //     { name: "Decision Matrix", description: "A tool for evaluating and prioritizing options based on specific criteria.", strengths: "Provides a clear comparison." },
                //     { name: "Cost-Benefit Analysis", description: "A method for comparing the costs and benefits of different choices.", strengths: "Helps in financial decision-making." }
                // ]),
                response: inputText,
                num_frameworks: 3 // Show 3 frameworks by default
            }),
        });

        if (response.ok) {
            const data = await response.json();
            
            // Validate JSON format
            if (!validateJSON(JSON.stringify(data))) {
                resultDiv.innerHTML = '<p>Error: Invalid JSON format received.</p>';
                return;
            }

            resultDiv.innerHTML = `<h2>Recommended Frameworks:</h2>`;
            data.forEach((framework, index) => {
                // Check if strengths is an array and handle it appropriately
                let strengthsHtml = '';
                if (Array.isArray(framework.strengths)) {
                    strengthsHtml = `
                        <p><strong>Strengths:</strong></p>
                        <ul>
                            ${framework.strengths.map(strength => `<li>${strength}</li>`).join('')}
                        </ul>
                    `;
                } else {
                    strengthsHtml = `<p><strong>Strengths:</strong> ${framework.strengths}</p>`;
                }
                
                resultDiv.innerHTML += `
                    <div class="framework-card">
                        <h3>${framework.name}</h3>
                        <p>${framework.description}</p>
                        ${strengthsHtml}
                        <div class="framework-actions">
                            <button onclick="explainFramework('${framework.name}')">Explain in Detail</button>
                            <button onclick="applyFramework('${framework.name}', '${encodeURIComponent(inputText)}')">Apply to My Situation</button>
                        </div>
                    </div>
                `;
            });

            // Add comparison button if more than one framework is returned
            if (data.length > 1) {
                const frameworkNames = data.map(f => f.name);
                resultDiv.innerHTML += `
                    <div class="comparison-section">
                        <h3>Compare Frameworks</h3>
                        <button onclick="compareFrameworks(${JSON.stringify(frameworkNames)}, '${encodeURIComponent(inputText)}')">
                            Compare All Frameworks
                        </button>
                    </div>
                `;
            }

            // Add global functions for the buttons
            window.explainFramework = explainFramework;
            window.applyFramework = applyFramework;
            window.compareFrameworks = compareFrameworks;
        } else {
            const errorData = await response.json();
            resultDiv.innerHTML = `<p>Error: ${errorData.error}</p>`;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        resultDiv.innerHTML = '<p>Error retrieving response. Please try again.</p>';
    }
});

// Keep the original code commented out for reference
// let selectedFramework = null; // Variable to store the selected framework
// 
// function selectFramework(frameworkName) {
//     selectedFramework = frameworkName; // Save the selected framework
//     alert(`You have selected: ${frameworkName}`);
//     
//     // Show the NEXT button
//     document.getElementById('nextButton').style.display = 'block';
// }
// 
// function goToNext() {
//     if (selectedFramework) {
//         alert(`Proceeding with: ${selectedFramework}`);
//         // Add logic here to handle what happens next
//     } else {
//         alert('Please select a framework first.');
//     }
// }
// 
// function parseFrameworks(responseContent) {
//     try {
//         // First parse the string to get a JSON string
//         const jsonString = JSON.parse(responseContent);
//         // Then parse the JSON string to get the actual array
//         const frameworksArray = JSON.parse(jsonString);
//         return frameworksArray;
//     } catch (error) {
//         console.error('Parsing error:', error);
//         return null; // Return null if parsing fails
//     }
// }
// 
// const mockResponse = JSON.stringify([
//     { name: "SWOT Analysis", description: "A framework for identifying strengths, weaknesses, opportunities, and threats.", strengths: "Helps in strategic planning." },
//     { name: "Decision Matrix", description: "A tool for evaluating and prioritizing options based on specific criteria.", strengths: "Provides a clear comparison." },
//     { name: "Cost-Benefit Analysis", description: "A method for comparing the costs and benefits of different choices.", strengths: "Helps in financial decision-making." }
// ]);
// 
// const frameworksArray = parseFrameworks(mockResponse);
// console.log(frameworksArray); // Test the parser with mock data
// 
// function storeResponse(responseContent) {
//     // Here you can implement logic to send the response to a backend service
//     // For example, using fetch to send it to a Python server
//     console.log('Storing response for further processing:', responseContent);
//     
//     // Example of sending to a backend (assuming you have a server set up)
//     /*
//     fetch('http://your-backend-endpoint/store', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ response: responseContent })
//     })
//     .then(res => res.json())
//     .then(data => console.log('Response stored:', data))
//     .catch(err => console.error('Error storing response:', err));
//     */
// }
// 
// function callPythonParser(responseContent) {
//     const numFrameworks = prompt("How many frameworks would you like to see? (1-3):");
//     
//     fetch('http://localhost:5000/parse', { // Ensure this URL is correct
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ response: responseContent, num_frameworks: parseInt(numFrameworks) })
//     })
//     .then(res => {
//         if (!res.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return res.json();
//     })
//     .then(frameworks => {
//         // Display the frameworks with descriptions
//         resultDiv.innerHTML += `<h2>Parsed Frameworks:</h2>`;
//         frameworks.forEach((framework, index) => {
//             resultDiv.innerHTML += `
//                 <div class="framework-box">
//                     <h3 class="framework-title">Framework ${index + 1}: ${framework.name}</h3>
//                     <p class="framework-description">${framework.description}</p>
//                     <p><strong>Strengths:</strong> ${framework.strengths}</p>
//                 </div>
//             `;
//         });
//     })
//     .catch(err => {
//         console.error('Error calling Python parser:', err);
//         resultDiv.innerHTML += `<p>Error calling Python parser: ${err.message}</p>`;
//     });
// }

/**
 * Function to explain a framework in detail.
 * This function calls the framework explainer agent to get comprehensive information
 * about a specific framework, including how it works, steps to apply it, examples,
 * and limitations.
 * 
 * @param {string} frameworkName - The name of the framework to explain
 */
async function explainFramework(frameworkName) {
    const resultDiv = document.getElementById('result');
    const detailsDiv = document.createElement('div');
    detailsDiv.className = 'framework-details';
    detailsDiv.innerHTML = '<p>Loading explanation...</p>';
    
    // Add the details div after the framework cards
    resultDiv.appendChild(detailsDiv);
    
    try {
        // Call the framework explainer agent via the /explain endpoint
        const response = await fetch('http://127.0.0.1:5000/explain', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                framework_name: frameworkName
            }),
        });

        if (response.ok) {
            const data = await response.json();
            
            detailsDiv.innerHTML = `
                <div class="details-header">
                    <h2>${frameworkName} - Detailed Explanation</h2>
                    <button onclick="this.parentElement.parentElement.remove()">Close</button>
                </div>
                <div class="details-content">
                    <h3>How it Works</h3>
                    <p>${data.explanation}</p>
                    
                    <h3>Steps to Apply</h3>
                    <ol>
                        ${data.steps.map(step => `<li>${step}</li>`).join('')}
                    </ol>
                    
                    <h3>When to Use</h3>
                    <ul>
                        ${data.examples.map(example => `<li>${example}</li>`).join('')}
                    </ul>
                    
                    <h3>Limitations</h3>
                    <ul>
                        ${data.limitations.map(limitation => `<li>${limitation}</li>`).join('')}
                    </ul>
                </div>
            `;
        } else {
            const errorData = await response.json();
            detailsDiv.innerHTML = `<p>Error: ${errorData.error}</p>`;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        detailsDiv.innerHTML = '<p>Error retrieving explanation. Please try again.</p>';
    }
}

/**
 * Function to apply a framework to the user's situation.
 * This function calls the framework application agent to get tailored guidance
 * for applying a specific framework to the user's unique situation.
 * 
 * @param {string} frameworkName - The name of the framework to apply
 * @param {string} situationEncoded - URL-encoded description of the user's situation
 */
async function applyFramework(frameworkName, situationEncoded) {
    const situation = decodeURIComponent(situationEncoded);
    const resultDiv = document.getElementById('result');
    const applicationDiv = document.createElement('div');
    applicationDiv.className = 'framework-application';
    applicationDiv.innerHTML = '<p>Loading application guide...</p>';
    
    // Add the application div after the framework cards
    resultDiv.appendChild(applicationDiv);
    
    try {
        // Call the framework application agent via the /apply endpoint
        const response = await fetch('http://127.0.0.1:5000/apply', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                framework_name: frameworkName,
                situation: situation
            }),
        });

        if (response.ok) {
            const data = await response.json();
            
            applicationDiv.innerHTML = `
                <div class="application-header">
                    <h2>Applying ${frameworkName} to Your Situation</h2>
                    <button onclick="this.parentElement.parentElement.remove()">Close</button>
                </div>
                <div class="application-content">
                    <h3>Key Questions to Answer</h3>
                    <ul>
                        ${data.questions.map(question => `<li>${question}</li>`).join('')}
                    </ul>
                    
                    <h3>Application Template</h3>
                    <div class="template">
                        ${data.template}
                    </div>
                    
                    <h3>Interpreting Results</h3>
                    <p>${data.interpretation_guidance}</p>
                </div>
            `;
        } else {
            const errorData = await response.json();
            applicationDiv.innerHTML = `<p>Error: ${errorData.error}</p>`;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        applicationDiv.innerHTML = '<p>Error retrieving application guide. Please try again.</p>';
    }
}

/**
 * Function to compare multiple frameworks for a specific situation.
 * This function calls the framework comparison agent to get a comparative analysis
 * of multiple frameworks in the context of the user's situation.
 * 
 * @param {Array} frameworkNames - Array of framework names to compare
 * @param {string} situationEncoded - URL-encoded description of the user's situation
 */
async function compareFrameworks(frameworkNames, situationEncoded) {
    const situation = decodeURIComponent(situationEncoded);
    const resultDiv = document.getElementById('result');
    const comparisonDiv = document.createElement('div');
    comparisonDiv.className = 'frameworks-comparison';
    comparisonDiv.innerHTML = '<p>Loading comparison...</p>';
    
    // Add the comparison div after the framework cards
    resultDiv.appendChild(comparisonDiv);
    
    try {
        // Call the framework comparison agent via the /compare endpoint
        const response = await fetch('http://127.0.0.1:5000/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                framework_names: frameworkNames,
                situation: situation
            }),
        });

        if (response.ok) {
            const data = await response.json();
            
            comparisonDiv.innerHTML = `
                <div class="comparison-header">
                    <h2>Framework Comparison</h2>
                    <button onclick="this.parentElement.parentElement.remove()">Close</button>
                </div>
                <div class="comparison-content">
                    <h3>Feature Comparison</h3>
                    <div class="comparison-table">
                        ${data.comparison}
                    </div>
                    
                    <h3>Pros and Cons for Your Situation</h3>
                    <div class="pros-cons">
                        ${data.pros_cons}
                    </div>
                    
                    <h3>Recommendation</h3>
                    <p>${data.recommendation}</p>
                </div>
            `;
        } else {
            const errorData = await response.json();
            comparisonDiv.innerHTML = `<p>Error: ${errorData.error}</p>`;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        comparisonDiv.innerHTML = '<p>Error retrieving comparison. Please try again.</p>';
    }
}

/**
 * Utility function to validate JSON format.
 * 
 * @param {string} jsonString - The JSON string to validate
 * @returns {boolean} - True if valid JSON, false otherwise
 */
function validateJSON(jsonString) {
    try {
        JSON.parse(jsonString);
        return true; // Valid JSON
    } catch (e) {
        console.error('Invalid JSON format:', e);
        return false; // Invalid JSON
    }
}