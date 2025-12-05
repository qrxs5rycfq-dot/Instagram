# Instagram Account Creation Tool

A Python script for Instagram account creation with advanced anti-detection features.

## Requirements

- Python 3.8+
- Internet connection

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/qrxs5rycfq-dot/Instagram.git
   cd Instagram
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with:
```bash
python3 bipas6.py
```

The script provides a CLI interface with the following main options:
- **Create Single Account** - Create one Instagram account
- **Create Batch Accounts** - Create multiple accounts at once
- **Run Diagnostics** - Test all system components
- **View System Status** - Check current system health
- **Test Systems** - Test individual components (email, IP, etc.)

## Features

- Multiple email service providers for verification
- Advanced anti-detection fingerprinting
- Dynamic IP generation and rotation
- Browser behavior simulation
- Rate limiting and circuit breaker patterns

## Configuration

The script will create necessary directories on first run:
- `sessions/` - Session storage
- `logs/` - Log files
- `accounts/` - Created account records

A default configuration file `config_2025.json` will be created with sensible defaults.

## Notes

- This tool is for educational purposes only
- Respect Instagram's Terms of Service
- Use responsibly and ethically

## Troubleshooting

If you encounter import errors, ensure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```

For aiohttp-related issues:
```bash
pip install aiohttp[speedups]
```