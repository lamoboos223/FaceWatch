document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            alert('Face registered successfully!');
            e.target.reset();
        } else {
            alert(data.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during registration');
    }
});

document.getElementById('verifyForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const resultDiv = document.getElementById('result');

    try {
        const response = await fetch('/verify', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            if (data.match) {
                const matchInfo = data.data;
                resultDiv.innerHTML = `
                    <div class="success">
                        ✅ Match found!<br>
                        URL: ${matchInfo.url}<br>
                        Reason: ${matchInfo.reason}<br>
                        Registered: ${new Date(matchInfo.timestamp).toLocaleString()}
                    </div>`;
                resultDiv.className = 'match';
            } else {
                resultDiv.innerHTML = '<div class="error">❌ No match found. Face is not registered.</div>';
                resultDiv.className = 'no-match';
            }
        } else {
            resultDiv.innerHTML = `<div class="error">${data.error || 'Verification failed'}</div>`;
            resultDiv.className = 'error';
        }
        e.target.reset();
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = '<div class="error">An error occurred during verification</div>';
        resultDiv.className = 'error';
    }
}); 