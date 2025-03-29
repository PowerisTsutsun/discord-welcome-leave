# discord-welcome-leave

## AFK & Welcome Discord Bot

This Discord bot extension adds fun and useful functionality to your server by allowing users to mark themselves as AFK, sending custom welcome messages to new members, and logging member join/leave events along with ban notifications.

## Features

- **AFK Command (`^afk on/off`):**  
  Users can mark themselves as AFK. When someone mentions an AFK user, the bot notifies them that the user is currently AFK.

- **Welcome Messages (`^welcome on/off`):**  
  Toggle welcome messages in the current channel. When enabled, the bot sends a styled welcome embed to new members joining your server.  
  *Only the designated admin (ID: 92423311505510400) can toggle welcome messages.*

- **Log Channel Toggle (`^datato on/off`):**  
  Set the current channel as the log channel where new member data (join/leave events and bans) is logged.  
  *Only the designated admin (ID: 92423311505510400) can toggle data logging.*

- **Member Logging:**
  - **Join Logging:** The bot logs when a new member joins, including their Discord creation date and server join date.
  - **Leave Logging:** The bot logs when a member leaves or is kicked.
  - **Ban Logging:** The bot logs ban events, optionally including the ban reason if available.

- **Customizable Welcome Embed:**  
  The welcome embed references important channels by their IDs:
  - **Roles:** 1044975458116194304
  - **Introductions:** 670671010613166090
  - **Info:** 1045002655652646953
  - **Lounge:** 669880850174836746

## Requirements

- Python 3.8 or higher
- [discord.py](https://discordpy.readthedocs.io/en/stable/) (v2.x recommended)
- A Discord bot token (stored in your `.env` file as `DISCORD_TOKEN`)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/your-bot-repo.git
   cd your-bot-repo
