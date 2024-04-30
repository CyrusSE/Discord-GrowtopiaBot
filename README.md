# Discord-GrowtopiaBot

Welcome to the GitHub repository for the Discord-GrowtopiaBot! This project is a Discord bot designed specifically for managing and enhancing the experience on Growtopia Private Servers (GTPS), particularly GTPS 3.

## Project Journey

I started on this project on 2021, with no knowledge of coding or programming languages. Don't judge me for the bad/terrible code, at that time there was no AI bot that helping me solving problems, so i only read Stack Overflow for the errors. Python is first programming language, was both a challenge and a fun to learn. After countless hours of coding, debugging, and learning from Stack Overflow, the project reached its end on June 13, 2023.

This project was not just about coding. It was about overcoming challenges, learning the programming logic, problem-solving, and much more. It was a journey filled with errors, all of which contributed to my growth as a developer.

The bot was developed to serve both public users and staff on the GTPS 3 server, handling over 39,819 JSON player files and operating across different VPS to interact with the GTPS3 panel for database operations with total `65` Public and Private commands.

## Features & Command List

### Public Commands

- `!commands`: Displays all available public commands.
- `!recovery <GrowID> <Email>`: Helps in account recovery, operational only in DM.
- `!verify <GrowID> <Email>`: Assists in joining the Mod Server, operational only in DM.
- `!checkprice <Name Item>`: Fetches the price of a specified item.
  - The price information is stored in the `./price` directory, with the following format: `{"price":"30-50 Diamond Locks", "name":"Dragon of Phoenix", "by":"Cyrus#8000", "last":"1677151388"}`.
- `!suggestprice <Name Item>`: Suggests price changes for items to ensure up-to-date information.
- `!myvalue`: Displays the net worth of your account based on tradeable and untradeable items.
- `!hostpc`, `!hostandroid`, `!hostandroid2`, `!hostios`: Provides tutorials and files for hosting GTPS 3 on various platforms.
- `!invite`: Sends the GTPS 3 Discord link and bot invite link.

### Staff Commands

- `!autodelete <discord user>`: Automatically deletes messages from specified users.
- `!backup`: Backs up important files.
- `!blacklistgrowid <growid>`: Blacklists a GrowID, preventing it from using the verify command.
- `!blacklistuser <discord user>`: Blacklists a Discord user, preventing them from using the verify command.
- `!change2fa <growid> <new 2fa>`: Changes the 2FA of a Growtopia account by sending a request to the GTPS3 panel.
- `!changeemail <growid> <new email>`: Changes the email of a Growtopia account by sending a request to the GTPS3 panel.
- `!changepass <growid> <new password>`: Changes the password of a Growtopia account by sending a request to the GTPS3 panel.
- `!checkdata <growid> <data>`: Checks if the mentioned GrowID contains the specified data.
- `!checkmod <growid>`: Checks if a GrowID has moderator privileges.
- `!clown <discord user>`: Automatically reacts with a clown emoji to messages from specified users.
- `!country <growid>`: Shows the mentioned GrowID's country.
- `!crossban <discord user>`: Bans a user from two GTPS3 Discord servers.
- `!crossunban <discord user>`: Unbans a user from two GTPS3 Discord servers.
- `!deleteaccount <growid>`: Deletes an account associated with a GrowID.
- `!dm <discord id>`: DMs a user.
- `!dnd`: Changes the bot's status to DND.
- `!fetchdata <growid>`: Fetches the newest data from the GTPS3 Panel.
- `!findid <name>`: Finds all item IDs starting with the mentioned name.
- `!getitemid <name item>`: Sends the item ID of the mentioned item name.
- `!givewls <growid> <wls>`: Gives premium WLS to the mentioned GrowID.
- `!idle`: Changes the bot's status to idle.
- `!kickmods`: Scans all Discord users in the Mod Server, checks if their GrowID still has mod privileges or if the player is banned or doesn't exist in the database, and kicks them from the Mod Server if they don't have mod privileges.
- `!manualverify <growid> <discord user>`: Manually verifies a GrowID for a user.
- `!offline`: Changes the bot's status to offline.
- `!online`: Changes the bot's status to online.
- `!poll`: Make a poll.
- `!restart`: Restarts the bot.
- `!removegems <growid>`: Removes the gems from a GrowID.
- `!removegtpswl <growid>`: Removes the mentioned WLS from a GrowID.
- `!removerole <growid>`: Removes all roles from a GrowID.
- `!resetblacklist <discord user>`: Resets a Discord user's blacklist or unblacklists them from the verify command.
- `!resetblacklistgrowid <growid>`: Resets a forced GrowID blacklist or unblacklists a GrowID from the verify command.
- `!resetblacklistuser <discord user>`: Resets a forced blacklist for a Discord user.
- `!resetgrowid <growid>`: Resets a GrowID's blacklist.
- `!resetprice <item id>`: Resets the price of the mentioned item ID.
- `!resetuser <discord id>`: Resets a user from the normal blacklist or unblacklists them from the verify command.
- `!scanmods`: Sends a list of Mod Server members who don't have the Mod role or whose player is banned or doesn't exist in the database.
- `!showalt <growid>`: Sends all alts of the mentioned GrowID if their device MAC, IP, or RID is the same as the mentioned GrowID.
- `!showinv <growid>`: Sends the inventory list of the mentioned GrowID.
- `!showlastworld <growid>`: Sends the last world list of the mentioned GrowID.
- `!silentban <discord user>`: Bans a Discord user without DMing them.
- `!stopautodelete`: Stops auto-deleting someone's message.
- `!stopclown`: Stops clowning someone's message.
- `!trackitemid <item id>`: Tracks the mentioned item ID from the database and lists the players who have it.
- `!unban <discord user>`: Unbans someone from the GTPS3 Discord server.
- `!unbangrowid <growid>`: Unbans a banned GrowID from the server.
- `!up`: Sends the bot's uptime.
- `!updatedata`: Update all `itemid.json` to newest `item.dat` with Growtopia Item Data `decoder.exe`.
- `!update2`: Updates the timer of the last update message.
- `!updateprice <item id> <new price>`: Updates the price of the mentioned item ID to a new price.
- `!who <discord user>`: Sends information about the mentioned Discord user.
- `!whoban <growid>`: Shows who banned the mentioned GrowID.
- `!whyuserisnotallowed <growid> <discord user>`: Shows the reason why the user is not allowed, whether the GrowID is blacklisted or the Discord user is blacklisted.


## Installation

To run this bot, you need to install the required libraries listed in `requirements.txt`. Use the following command to install all dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To start the bot, ensure you have the correct credentials and environment variables set up, then run the main script:

```bash
python gtpsbot.py
```


## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
