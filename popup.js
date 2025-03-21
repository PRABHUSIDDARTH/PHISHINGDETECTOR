document.addEventListener("DOMContentLoaded", () => {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.type === "getResult") {
        chrome.storage.local.get(["lastResult"], (data) => {
          const result = data.lastResult || {};
          const status = document.getElementById("status");
          if (result.domain) {
            status.textContent = `Domain: ${result.domain}\nScore: ${result.score}\n${
              result.is_phishing ? "Phishing Detected!" : "Safe"
            }`;
          } else {
            status.textContent = "No recent checks.";
          }
          sendResponse({ received: true });
        });
        return true;
      }
    });
  
    // Request the latest result when popup opens
    chrome.runtime.sendMessage({ type: "getResult" });
  });