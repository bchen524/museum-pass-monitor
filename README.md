# Seattle Library Museum Pass Monitor

Monitors the Seattle Public Library museum pass website for Seattle Aquarium weekend availability and sends email notifications.

## Features

- 🔍 Monitors Seattle Public Library museum pass system
- 🎟️ Specifically tracks Seattle Aquarium passes
- 📅 Filters for weekend availability only (Saturday/Sunday)
- 📧 Email notifications when slots become available
- ⏰ Configurable check intervals
- 🔄 Continuous monitoring mode

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings

1. Copy `config.json.example` to `config.json`:
   ```bash
   copy config.json.example config.json
   ```

2. Edit `config.json` with your email settings:

#### For Gmail:
- Use your Gmail address as `from_email`
- Generate an App Password (not your regular password):
  1. Go to Google Account settings
  2. Security → 2-Step Verification (must be enabled)
  3. App passwords → Generate new
  4. Use the generated 16-character password in `config.json`

#### For Other Email Providers:
Update `smtp_server` and `smtp_port` accordingly:
- **Outlook/Hotmail**: `smtp-mail.outlook.com`, port `587`
- **Yahoo**: `smtp.mail.yahoo.com`, port `587`
- **Custom SMTP**: Use your provider's settings

### 3. Configure Monitoring Settings

Edit `config.json`:

```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "from_email": "youremail@gmail.com",
    "to_email": "recipient@gmail.com",
    "password": "your-app-password-here"
  },
  "check_interval_minutes": 30,
  "api_url": null,
  "notify_on_weekends_only": true
}
```

- `check_interval_minutes`: How often to check (default: 30 minutes)
- `notify_on_weekends_only`: Only notify for weekend slots (default: true)

## Usage

### Continuous Monitoring

Run the monitor continuously (checks every configured interval):

```bash
python monitor.py
```

This will:
- Check the website every 30 minutes (or your configured interval)
- Look for Seattle Aquarium passes
- Filter for weekend dates only
- Send email alerts when found
- Continue running until stopped (Ctrl+C)

### Single Check (Testing)

Run a one-time check to test your setup:

```bash
python monitor.py --once
```

## How It Works

1. **Web Scraping**: Connects to Seattle Public Library's museum pass system
2. **Parsing**: Searches for Seattle Aquarium availability
3. **Date Filtering**: Identifies weekend dates (Saturday/Sunday)
4. **Notification**: Sends HTML email with available dates
5. **Deduplication**: Tracks notified dates to avoid spam

## Important Notes

### Website Structure
The Seattle Public Library website structure may change. If the monitor stops working:
1. Visit the website manually: https://www.spl.org/programs-and-services/learning/museum-passes
2. Inspect the HTML structure using browser developer tools
3. Update the parsing logic in `monitor.py` if needed

### Email Security
- Never commit `config.json` with real credentials to version control
- Use app-specific passwords, not your main email password
- Keep your `config.json` file secure

### Rate Limiting
- Default check interval is 30 minutes to be respectful to the website
- Don't set the interval too low to avoid being blocked
- Consider checking less frequently during off-hours

## Troubleshooting

### No Emails Received
1. Check your email credentials in `config.json`
2. Verify spam/junk folder
3. Test with `--once` flag to see console output
4. Ensure 2FA and app passwords are set up correctly (for Gmail)

### Connection Errors
- Check your internet connection
- Verify the website URL is still correct
- The library website might be temporarily down

### No Availability Found
- The passes might genuinely be unavailable
- The website structure may have changed (requires code update)
- Run with `--once` to see console output for debugging

## Scheduling

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup")
4. Action: Start a program
5. Program: `python`
6. Arguments: `c:\Museum Pass Website Monitor\monitor.py`

### Keep Running 24/7
For continuous monitoring, just keep the Python script running in a terminal. Consider:
- Running in a `screen` or `tmux` session (Linux/Mac)
- Using Windows Task Scheduler to restart on system boot
- Running on a always-on device or cloud server

## Customization

To monitor different museums or venues, edit `monitor.py`:
- Change `aquarium_search_url` to the desired venue
- Update search terms in `check_availability()`
- Modify email subject/body text

## License

Free to use and modify for personal use.
