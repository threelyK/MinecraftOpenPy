# Discord Minecraft Server Opener

## Overview

This Discord bot allows users to launch a Minecraft server using bash scripts executed remotely through Discord slash commands. The bot interacts with a remote server to start, stop, and manage the Minecraft server, providing a seamless integration for Discord communities.

## Features

- Launch and stop a Minecraft server remotely
- Check number of players online
- Simple and easy-to-use Discord slash commands

## Prerequisites

- A remote server with SSH access
- Minecraft server setup on the remote server
- Python 3.8+
- Discord bot token
- Bash scripts to manage the Minecraft server

## Installation

1. **Clone the repository:**
    ```bash
    git clone REPO-URL-GOES-HERE
    cd discord-minecraft-server-bot
    ```

2. **Set up a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```
    DISCORD_TOKEN=your-discord-bot-token
    AUTHORISED_SERVER_IDS=your-authorised-server-ids
    ```

5. **Set up your bash scripts on the remote server:**
    Ensure you have the following scripts on your remote server:
    - `start_minecraft.sh`: Script to start the Minecraft server
    - `stop_minecraft.sh`: Script to stop the Minecraft server
    - `check_count_minecraft.sh`: Script to check the number of players currently on the Minecraft server
  
## Commands

- `/server_start`: Launch the Minecraft server
- `/server_stop`: Stop the Minecraft server
- `/server_list`: Check the number of players currently on the Minecraft server

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
