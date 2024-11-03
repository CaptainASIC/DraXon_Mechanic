# DraXon Mechanic

A Discord bot designed to collect and display system specifications. This bot provides simple commands to gather and show system information in an attractive, easy-to-read format.

## Features

- `/system-collect`: Captures current system specifications
- `/system-show`: Displays the collected system information in a formatted embed

## System Information Collected

- Operating System and Version
- System Architecture
- Processor Information
- Memory Usage (Total and Available)
- Disk Usage
- Collection Timestamp

## Setup

1. Clone the repository:
```bash
git clone https://github.com/CaptainASIC/DraXon_Mechanic.git
cd DraXon_Mechanic
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Discord bot:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section and create a bot
   - Copy the bot token

4. Configure environment variables:
   - Copy `.env.example` to `.env` in the env directory
   ```bash
   cp env/.env.example env/.env
   ```
   - Edit `.env` and set your Discord bot token and other configurations
   ```bash
   nano env/.env
   ```

5. Run the bot:
```bash
python src/bot.py
```

## Configuration

The bot can be configured using the following environment variables in the `env/.env` file:

- `DISCORD_TOKEN` (Required): Your Discord bot token
- `DEBUG` (Optional): Enable debug mode (true/false)
- `CMD_PREFIX` (Optional): Command prefix for legacy commands if implemented

## Project Structure

```
DraXon_Mechanic/
├── src/             # Source code directory
│   ├── bot.py      # Main bot implementation
│   └── utils/      # Utility modules
│       └── constants.py  # Constants and configuration
├── env/            # Environment configuration
│   ├── .env       # Your configuration (create this)
│   └── .env.example # Example environment variables
├── requirements.txt # Project dependencies
├── LICENSE         # GPL3 license
└── README.md       # This file
```

## Usage

1. Invite the bot to your server using the OAuth2 URL generator in the Discord Developer Portal
2. Use `/system-collect` to gather system information
3. Use `/system-show` to display the collected information

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE) file for details.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Contact

For questions or issues:
- GitHub Issues: [Create an issue](https://github.com/CaptainASIC/DraXon_Mechanic/issues)
- DraXon Discord: [Join our server](https://discord.gg/bjFZBRhw8Q)

Created by DraXon (DraXon Industries)
