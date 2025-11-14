# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gateway-ripper.git
cd gateway-ripper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install requests beautifulsoup4 lxml colorama pyfiglet validators fake-useragent
```

### 3. Verify Installation

```bash
python ripper.py --version
```

You should see:
```
Gateway-Ripper v1.0.0
```

## Installation on Termux (Android)

### 1. Install Termux
Download from F-Droid: https://f-droid.org/en/packages/com.termux/

### 2. Update Packages
```bash
pkg update && pkg upgrade
```

### 3. Install Python and Git
```bash
pkg install python git
```

### 4. Clone and Install
```bash
git clone https://github.com/yourusername/gateway-ripper.git
cd gateway-ripper
pip install -r requirements.txt
```

### 5. Run the Tool
```bash
python ripper.py --url https://example.com
```

## Common Issues

### SSL Certificate Errors
If you encounter SSL errors, the tool automatically disables SSL verification warnings. However, you can also:

```bash
pip install --upgrade certifi
```

### Permission Denied
If you get permission errors during installation:

```bash
pip install --user -r requirements.txt
```

### Module Not Found
Make sure you're using Python 3:

```bash
python3 ripper.py --url https://example.com
```

## Updating

To update to the latest version:

```bash
cd gateway-ripper
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

```bash
cd ..
rm -rf gateway-ripper
```

## Next Steps

After installation, check out:
- [README.md](README.md) for usage examples
- [EXAMPLES.md](EXAMPLES.md) for real-world scenarios
- [API.md](API.md) for programmatic usage
