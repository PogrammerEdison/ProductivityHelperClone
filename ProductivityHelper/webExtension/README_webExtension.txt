This folder contains the code for the web extension client code, and the relay code for communicating with the application.

Setup Instructions for Google Chrome:
1.  Firstly we're going to allow the chrome extension to communicate with the app. Open the Registry Editor (search for it in windows search)
2.  Using the folders on the left pane, go to Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Google\Chrome\NativeMessagingHosts
3.  Right click on the NativeMessagingHosts, go to New -> Key
4.  Set the name of the new folder that appears to com.bath.group14.productivity_helper_extension
5.  Make sure that that folder is now selected. Right click on (Default) in the main pane, and click Modify
6.  Set the value data to the path to the relay manifest.json (NOT the extension manifest.json). For me its:
    C:\Users\Theo\OneDrive - University of Bath\Documents\University\CM10313 - Software Processes and Modelling\repo\ProductivityHelper\webExtension\relay\manifest.json
    but for you it'll be different
7.  Now we're going to add the web extension to chrome. Enter chrome://extensions/ into the address bar.
8.  Enable Developer Mode using the toggle in the top Right
9.  Click Load unpacked
10. Give it the folder that contains the web extension. For me it's:
    C:\Users\Theo\OneDrive - University of Bath\Documents\University\CM10313 - Software Processes and Modelling\repo\ProductivityHelper\webExtension\extension
    but for you it'll be different