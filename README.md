delete-discord

WARNING: This script violates the Discord Terms of Service if used for a non-bot account! ONLY use for bot accounts!


What this does:
It lists all the servers and the channels on your server that your bot account is a part of. Then, it can delete all of your messages in a server or in a specific channel on a server. This is useful to free up hard disk space on Discord's servers, and so on.


How to use:
Python 3.5+ required.

Install discord, e.g. python3 -m pip install discord.py

Run the script.

Enter your username/password that you use to login to discord.

At the menu, you can choose the following:

"1. Select a server"
Provide the name of the server (not the ID). You can get a list of servers by using menu option 3.

"2. Select a channel"
Provide the index of the channel (not the name). You can get a list of channels by using menu option 4.

"3. Print a list of all servers this account has joined"
Pretty self-explanatory.

"4. Print a list of all channels on the selected server"
Pretty self-explanatory. A server must be selected with menu option 1.

"5. Delete all messages on the selected server (wow!)"
Delete all messages that your bot wrote on all channels in the selected server. Takes a while!
A server must be selected with menu option 1.

"6. Delete all messages in the selected channel on the selected server"
Delete all messages that your bot wrote on the selected channels in the selected server. Takes a while! 
A server must be selected with menu option 1, and a channel must be selected with option 2.

"7. Quit"
Quit.


Comments:
The lazy script creator overlaid a blocking event loop onto an async event loop, so you get predictably disastrous logic and structure, such as logging in and logging out every time you choose a new option. He also didn't implement a good credentials system. Sorry.