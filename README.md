# Daily Hora Timings - macOS Menu Bar Widget

A native macOS menu bar application that displays daily Vedic astrology hora timings with automatic updates. Features a beautiful widget interface that shows the current planetary hora in your menu bar.

**Data powered by [Free Astrology API](https://freeastrologyapi.com)**

## Features

- 🕉️ **Native macOS Menu Bar Widget** - Lives in your menu bar like system apps
- ⏰ **Auto-updates every minute** - Always shows current hora
- 📅 **Daily automatic refresh** - Fetches new data at 6 AM using launchd
- 🌟 **Planet emojis** - Visual representation of each hora lord
- 💾 **Efficient caching** - Only 1 API call per day
- 🔔 **Native notifications** - macOS notifications for updates
- 🎯 **Current hora highlighting** - Easy to see which hora is active

## Prerequisites

- macOS (tested on macOS 10.13+)
- Python 3.7 or higher
- Free Astrology API key from [freeastrologyapi.com](https://freeastrologyapi.com)

## Setup

### 1. Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Your API Key and Location

Create a `.env` file in the project directory:

```bash
# Your Free Astrology API key (get one from freeastrologyapi.com)
ASTROLOGY_API_KEY=your_api_key_here

# Your location coordinates (default: Austin, TX)
LATITUDE=30.2672
LONGITUDE=-97.7431
TIMEZONE=-6
```

**Note:** Never commit your `.env` file or API key to version control!

### 3. Set Up Automatic Daily Updates

The project includes a launchd configuration that automatically fetches new hora data at 6:00 AM daily.

```bash
# Copy the plist file to LaunchAgents
cp com.horafetcher.plist ~/Library/LaunchAgents/

# Load the scheduled job
launchctl load ~/Library/LaunchAgents/com.horafetcher.plist

# Verify it's loaded
launchctl list | grep horafetcher
```

## Usage

### Running the Menu Bar Widget

```bash
# Make sure you're in the project directory
cd /path/to/hora

# Activate virtual environment
source venv/bin/activate

# Load environment variables and run the widget
export $(cat .env | xargs) && python hora_gui.py
```

The widget will appear in your menu bar (top-right corner) with:
- 🕉️ symbol or current planet emoji (☀️, 🌙, ♂️, ☿️, ♃, ♀️, ♄)
- Click to see menu with current hora and all day's timings
- "Refresh Now" to manually fetch new data
- "Today's Horas" to see all 24 horas with current one highlighted

### Making the Widget Auto-Start on Login

To have the widget start automatically when you log in:

1. Open **System Preferences** → **Users & Groups** → **Login Items**
2. Click the **+** button
3. Navigate to your project and add a startup script, or:

Create a startup script:
```bash
#!/bin/zsh
cd /Users/vasikarlanaresh/workspace/hora
source venv/bin/activate
export $(cat .env | xargs)
python hora_gui.py
```

Save as `start_hora_widget.sh`, make it executable:
```bash
chmod +x start_hora_widget.sh
```

Then add it to Login Items.

### Manual Fetch (Without Widget)

```bash
# Activate virtual environment
source venv/bin/activate

# Load environment variables and run fetcher
export $(cat .env | xargs) && python hora_fetcher.py
```

## Managing the Scheduled Job

```bash
# Check if the job is running
launchctl list | grep horafetcher

# Stop the scheduled job
launchctl unload ~/Library/LaunchAgents/com.horafetcher.plist

# Start the scheduled job
launchctl load ~/Library/LaunchAgents/com.horafetcher.plist

# Run the job immediately (test)
launchctl start com.horafetcher

# View logs
tail -f hora_cron.log
tail -f hora_cron_error.log
```

## File Structure

```
hora/
├── hora_fetcher.py          # Core API fetcher script
├── hora_gui.py              # macOS menu bar widget application
├── requirements.txt         # Python dependencies
├── com.horafetcher.plist    # launchd configuration for scheduled fetching
├── .env                     # Environment variables (API key, coordinates)
├── hora_results.json        # Cached hora data
├── hora_cron.log           # Scheduled job output log
├── hora_cron_error.log     # Scheduled job error log
└── README.md               # This file
```

## API Response Format

The Free Astrology API returns hora timings in the following format:

```json
{
  "statusCode": 200,
  "output": {
    "1": {
      "lord": "Sun",
      "starts_at": "2025-11-16 06:57:38",
      "ends_at": "2025-11-16 07:57:40.125000"
    },
    "2": {
      "lord": "Venus",
      "starts_at": "2025-11-16 07:57:40.125000",
      "ends_at": "2025-11-16 08:57:42.250000"
    }
    // ... 24 horas total
  },
  "fetched_at": "2025-11-16T17:46:48.166863"
}
```

Each day contains 24 horas, with each hora lasting approximately 1 hour.

## Customization

### Changing Location

Edit the `.env` file with your city's coordinates:

```bash
# Example: New York City
LATITUDE=40.7128
LONGITUDE=-74.0060
TIMEZONE=-5
```

### Changing Fetch Time

Edit `com.horafetcher.plist` and change the hour:

```xml
<key>Hour</key>
<integer>6</integer>  <!-- Change to desired hour (0-23) -->
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.horafetcher.plist
launchctl load ~/Library/LaunchAgents/com.horafetcher.plist
```

### Changing Update Frequency

Edit `hora_gui.py` line with `time.sleep(60)` to change how often the widget checks for current hora (in seconds).

## Troubleshooting

### Widget not showing in menu bar
- Make sure rumps and PyObjC are installed: `pip install rumps PyObjC`
- Check if Python has accessibility permissions in System Preferences

### "API key not provided" error
- Verify `.env` file exists and contains `ASTROLOGY_API_KEY=your_key`
- Make sure you're exporting variables: `export $(cat .env | xargs)`

### Scheduled job not running
- Check if loaded: `launchctl list | grep horafetcher`
- View error logs: `cat hora_cron_error.log`
- Test manually: `launchctl start com.horafetcher`

### No data at startup
- Run manual fetch first: `python hora_fetcher.py`
- Check `hora_results.json` exists

## API Usage & Limits

**Free Astrology API Limits:**
- 50 requests per day
- 1 request per second

This application is optimized to use only **1 API request per day** (at 6 AM), well within the free tier limits.

## Credits

- **API Provider**: [Free Astrology API](https://freeastrologyapi.com) - Thank you for providing free Vedic astrology data!
- **Menu Bar Framework**: [rumps](https://github.com/jaredks/rumps) - Ridiculously Uncomplicated macOS Python Statusbar apps

## License

This project is open source and available for personal use. Please respect the Free Astrology API terms of service.

## Support

For issues with:
- This application: Open an issue on GitHub
- The Free Astrology API: Visit [freeastrologyapi.com](https://freeastrologyapi.com)
