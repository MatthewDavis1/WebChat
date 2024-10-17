document.getElementById('chatButton').addEventListener('click', () => {
    const userQuestion = prompt("Enter your question:");
    if(userQuestion){
        fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userQuestion })
        })
        .then(response => response.json())
        .then(data => {
            if(data.answer){
                alert(`Answer: ${data.answer}`);
            } else {
                alert(`Error: ${data.detail || 'Unknown error'}`);
            }
        })
        .catch(error => alert(`Error: ${error}`));
    }
});
