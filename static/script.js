async function createRule() {
    const ruleString = document.getElementById('ruleInput').value;
    try {
        const response = await fetch('/api/rules/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rule_string: ruleString })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to create rule');
        }

        const result = await response.json();
        document.getElementById('ruleOutput').textContent = JSON.stringify(result, null, 2);
        document.getElementById('ruleOutput').style.borderColor = '#28a745';
    } catch (error) {
        document.getElementById('ruleOutput').textContent = `Error: ${error.message}`;
        document.getElementById('ruleOutput').style.borderColor = '#dc3545';
        console.error('Error:', error);
    }
}

async function evaluateRule() {
    try {
        const ruleOutput = document.getElementById('ruleOutput').textContent;
        if (!ruleOutput) {
            throw new Error('Please create a rule first');
        }

        const ruleJson = JSON.parse(ruleOutput);
        const dataInput = document.getElementById('dataInput').value;
        const dataJson = JSON.parse(dataInput);

        const response = await fetch('/api/rules/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                rule: ruleJson,
                data: dataJson
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Evaluation failed');
        }

        const result = await response.json();
        const resultElement = document.getElementById('evaluationResult');
        resultElement.textContent = `Result: ${result.result ? 'TRUE' : 'FALSE'}`;
        resultElement.className = result.result ? 'success' : 'error';
    } catch (error) {
        const resultElement = document.getElementById('evaluationResult');
        resultElement.textContent = `Error: ${error.message}`;
        resultElement.className = 'error';
        console.error('Error:', error);
    }
}

// Add example data on page load
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('ruleInput').value = 'age > 30 AND department = \'Sales\'';
    document.getElementById('dataInput').value = JSON.stringify({
        "age": 35,
        "department": "Sales"
    }, null, 2);
});