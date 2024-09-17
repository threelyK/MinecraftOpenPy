# Discord Minecraft Server Opener

## Overview

This Discord bot allows users to launch a Minecraft server using bash scripts executed remotely through Discord slash commands. The bot interacts with a remote server to start, stop, and manage the Minecraft server, providing a seamless integration for Discord communities.

## Features

- Command cooldowns to stop spamming
- Ability to authorize certain servers
- Player counter to see how many are online
- Simple and easy-to-use Discord slash commands

## Prerequisites

- A remote server with SSH access (https://blogs.oracle.com/developers/post/how-to-set-up-and-run-a-really-powerful-free-minecraft-server-in-the-cloud)
- Minecraft server files on the remote server
- Python 3.8+
- Discord bot token
- Bash scripts to manage the Minecraft server including a server-start, server-stop, server-backup, and player-count

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/threelyK/MinecraftOpenPy.git
    cd MinecraftOpenPy
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
    AUTHORISED_SERVER_IDS=[your-authorised-server-ids]
    ```

5. **Set up your bash scripts on the remote server:**
    Ensure you have the following scripts on your remote server:
    - `start_minecraft.sh`: Script to start the Minecraft server
    - `stop_minecraft.sh`: Script to stop the Minecraft server
    - `backup_minecraft.sh`: Script to backup world files
    - `check_count_minecraft.sh`: Script to check the number of players currently on the Minecraft server
  
## Commands

- `/server_start`: Launch the Minecraft server
- `/server_stop`: Stop the Minecraft server
- `/server_backup`: Backup the world folder
- `/server_player_count`: Output the number of players on the Minecraft server

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
