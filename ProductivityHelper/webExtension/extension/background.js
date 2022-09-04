var port;

function sendMessage(msg) {
    message = {"text": msg};
    console.log("Sending " + message)
    port.postMessage(message);
}

function onReceive(msg) {
    console.log("Received " + msg);
}

function onDisconnect() {
    console.log("Disconnected");
}

function connect() {
    port = chrome.runtime.connectNative("com.bath.group14.productivity_helper_extension");
    port.onMessage.addListener(onReceive);
    port.onDisconnect.addListener(onDisconnect);
}

connect();

var lastActiveWindow = chrome.windows.WINDOW_ID_NONE;

setInterval(() => {
    chrome.windows.getCurrent({}, (window) => {
        let activeWindow = window.focused ? window.id : chrome.windows.WINDOW_ID_NONE;
        if (activeWindow != lastActiveWindow) {
            lastActiveWindow = activeWindow;
            if (activeWindow == chrome.windows.WINDOW_ID_NONE) {
                sendMessage("");
            }
            else {
                chrome.tabs.query({ windowId: activeWindow }, (tabs) => {
                    let activeTab = tabs.find(tab => tab.active);
                    if (activeTab) {
                        sendMessage(activeTab.url);
                    }
                    else {
                        sendMessage("");
                    }
                });
            }
        }
    });
}, 1000);



chrome.tabs.onActivated.addListener((activeInfo) => {
    chrome.windows.get(activeInfo.windowId, {}, (window) => {
        if (window.focused) {
            lastActiveWindow = activeInfo.windowId;
            chrome.tabs.get(activeInfo.tabId, (tab) => {
                sendMessage(tab.url);
            });
        }
    });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    //Send a message if the tab's URL has changed
    if (changeInfo.url && tab.active) {
        chrome.windows.get(tab.windowId, {}, (window) => {
            if (window.focused) {
                lastActiveWindow = tab.windowId;
                sendMessage(changeInfo.url);
            }
        });
    }
});

