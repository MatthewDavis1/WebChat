chrome.runtime.onInstalled.addListener(() => {
    // Create context menu for explaining selected text
    chrome.contextMenus.create({
        id: "explainText",
        title: "Explain with WebChat",
        contexts: ["selection"]
    });

    // Create context menu for adding webpage to RAG DB
    chrome.contextMenus.create({
        id: "addWebpage",
        title: "Add Page to WebChat Database",
        contexts: ["page"]
    });

    // Create context menu for clearing RAG DB
    chrome.contextMenus.create({
        id: "clearDatabase",
        title: "Clear WebChat Database",
        contexts: ["action"]
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "explainText") {
        const selectedText = info.selectionText;
        fetch('http://localhost:5000/explain_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: selectedText })
        })
        .then(response => response.json())
        .then(data => {
            if(data.explanation){
                chrome.tabs.sendMessage(tab.id, { type: 'EXPLANATION', payload: data.explanation });
            } else {
                alert(`Error: ${data.detail || 'Unknown error'}`);
            }
        })
        .catch(error => alert(`Error: ${error}`));
    }

    if (info.menuItemId === "addWebpage") {
        const pageUrl = info.pageUrl;
        fetch('http://localhost:5000/add_webpage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: pageUrl })
        })
        .then(response => response.json())
        .then(data => {
            if(data.message){
                alert(data.message);
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => alert(`Error: ${error}`));
    }

    if (info.menuItemId === "clearDatabase") {
        if(confirm("Are you sure you want to clear the WebChat database? This action cannot be undone.")){
            fetch('http://localhost:5000/clear_vector_store', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if(data.message){
                    alert(data.message);
                } else {
                    alert(`Error: ${data.error}`);
                }
            })
            .catch(error => alert(`Error: ${error}`));
        }
    }
});
