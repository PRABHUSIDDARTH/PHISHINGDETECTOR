chrome.webRequest.onBeforeRequest.addListener(
    async (details) => {
      const url = new URL(details.url);
      const domain = url.hostname;
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ domain })
      });
      const result = await response.json();
      chrome.storage.local.set({ lastResult: result });
      if (result.is_phishing) {
        return { cancel: true };
      }
      return { cancel: false };
    },
    { urls: ["<all_urls>"] },
    ["blocking"]
  );
  
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "getResult") {
      chrome.storage.local.get(["lastResult"], (data) => {
        sendResponse(data.lastResult || {});
      });
      return true;
    }
  });