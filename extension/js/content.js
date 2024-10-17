chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'EXPLANATION') {
        alert(`Explanation: ${request.payload}`);
    }
});
