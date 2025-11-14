# Usage Examples

This document provides real-world examples of using Gateway-Ripper.

## Table of Contents

1. [Basic Analysis](#basic-analysis)
2. [Saving Output](#saving-output)
3. [Using Generated Code](#using-generated-code)
4. [Integration Examples](#integration-examples)
5. [Advanced Scenarios](#advanced-scenarios)

---

## Basic Analysis

### Example 1: Analyze a Single Website

```bash
python ripper.py --url https://example-shop.com
```

**Expected Output:**
```
   ______      __                                 ____  _                      
  / ____/___ _/ /____ _      ______ ___  __      / __ \(_)___  ____  ___  _____
 / / __/ __ `/ __/ _ \ | /| / / __ `/ / / /_____/ /_/ / / __ \/ __ \/ _ \/ ___/
/ /_/ / /_/ / /_/  __/ |/ |/ / /_/ / /_/ /_____/ _, _/ / /_/ / /_/ /  __/ /    
\____/\__,_/\__/\___/|__/|__/\__,_/\__, /     /_/ |_/_/ .___/ .___/\___/_/     
                                  /____/             /_/   /_/                 

Advanced Payment Gateway Analysis Tool
Version 1.0.0

[INFO] [12:34:56] Target validated: https://example-shop.com

============================================================
                  PHASE 1: WEB CRAWLING                    
============================================================

[INFO] [12:34:57] Fetching target: https://example-shop.com
[SUCCESS] [12:34:58] Successfully fetched page (45231 bytes)
[INFO] [12:34:58] Extracting JavaScript files...
[SUCCESS] [12:34:58] Found 12 JavaScript sources
[INFO] [12:34:58] Downloading JavaScript files...
[SUCCESS] [12:35:02] Downloaded 10 JavaScript files

============================================================
                PHASE 2: GATEWAY DETECTION                 
============================================================

[INFO] [12:35:02] Analyzing content for payment gateways...
[SUCCESS] [12:35:03] Detected gateway: STRIPE (confidence score: 18)
[SUCCESS] [12:35:03] Total gateways detected: 1

============================================================
           PHASE 3: CONFIGURATION EXTRACTION               
============================================================

[INFO] [12:35:03] Extracting API keys...
[SUCCESS] [12:35:03] Extracted 1 key(s) for STRIPE
[INFO] [12:35:03] Extracting additional configuration...
[SUCCESS] [12:35:03] Configuration extraction complete

============================================================
                PHASE 4: CODE GENERATION                   
============================================================

[SUCCESS] [12:35:03] Successfully generated code for STRIPE

============================================================
                   ANALYSIS RESULTS                        
============================================================

✓ Primary Gateway: STRIPE
✓ Confidence Score: 18

Extracted API Keys:
  • pk_live_ABCD************WXYZ

Detected Currencies: USD

------------------------------------------------------------

[Generated Python code follows...]
```

---

## Saving Output

### Example 2: Save Generated Code to File

```bash
python ripper.py --url https://example.com --output stripe_payment.py
```

This will:
1. Analyze the website
2. Generate the code
3. Save it to `stripe_payment.py`
4. Display success message

**Using the saved file:**

```bash
python stripe_payment.py
```

---

## Using Generated Code

### Example 3: Basic Card Check

After running Gateway-Ripper and getting the code, create a file `test_payment.py`:

```python
from stripe_payment import StripePaymentProcessor

# Initialize processor
processor = StripePaymentProcessor()

# Check a test card (Stripe test card number)
result = processor.check_card(
    card_number="4242424242424242",
    exp_month="12",
    exp_year="2025",
    cvc="123"
)

print(f"Status: {result['status']}")
print(f"Message: {result['message']}")
print(f"Card Brand: {result.get('card_brand', 'N/A')}")
```

**Output:**
```json
{
  "status": "valid",
  "message": "Card details are valid",
  "token": "tok_1A2B3C4D5E6F7G8H",
  "card_brand": "visa",
  "card_last4": "4242"
}
```

### Example 4: Testing Multiple Cards

```python
from stripe_payment import StripePaymentProcessor

processor = StripePaymentProcessor()

# Get test cards
test_cards = processor.get_test_cards()

# Test each scenario
for scenario, card_number in test_cards.items():
    print(f"\nTesting: {scenario}")
    result = processor.check_card(
        card_number=card_number,
        exp_month="12",
        exp_year="2025",
        cvc="123"
    )
    print(f"Result: {result['status']} - {result['message']}")
```

**Output:**
```
Testing: success
Result: valid - Card details are valid

Testing: declined
Result: declined - Your card was declined

Testing: insufficient_funds
Result: declined - Your card has insufficient funds

Testing: expired
Result: declined - Your card has expired
```

---

## Integration Examples

### Example 5: Telegram Bot Integration

```python
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from stripe_payment import StripePaymentProcessor

processor = StripePaymentProcessor()

def check_card(update: Update, context: CallbackContext):
    """Handle /check command"""
    try:
        # Parse card details from message
        # Format: /check 4242424242424242|12|25|123
        card_data = context.args[0].split('|')
        
        card_number = card_data[0]
        exp_month = card_data[1]
        exp_year = card_data[2]
        cvc = card_data[3]
        
        # Check card
        result = processor.check_card(card_number, exp_month, exp_year, cvc)
        
        # Format response
        if result['status'] == 'valid':
            message = f"✅ Card Valid\n"
            message += f"Brand: {result['card_brand']}\n"
            message += f"Last 4: {result['card_last4']}"
        else:
            message = f"❌ Card Declined\n"
            message += f"Reason: {result['message']}"
        
        update.message.reply_text(message)
        
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def main():
    updater = Updater("YOUR_BOT_TOKEN")
    updater.dispatcher.add_handler(CommandHandler("check", check_card))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
```

### Example 6: Flask Web Application

```python
from flask import Flask, request, jsonify
from stripe_payment import StripePaymentProcessor

app = Flask(__name__)
processor = StripePaymentProcessor()

@app.route('/api/check-card', methods=['POST'])
def check_card():
    """API endpoint to check card validity"""
    data = request.json
    
    result = processor.check_card(
        card_number=data['card_number'],
        exp_month=data['exp_month'],
        exp_year=data['exp_year'],
        cvc=data['cvc']
    )
    
    return jsonify(result)

@app.route('/api/test-cards', methods=['GET'])
def get_test_cards():
    """Get list of test cards"""
    return jsonify(processor.get_test_cards())

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Advanced Scenarios

### Example 7: Batch Card Checking

```python
import csv
from stripe_payment import StripePaymentProcessor

processor = StripePaymentProcessor()

# Read cards from CSV
with open('cards.csv', 'r') as f:
    reader = csv.DictReader(f)
    cards = list(reader)

# Check each card
results = []
for card in cards:
    result = processor.check_card(
        card_number=card['number'],
        exp_month=card['exp_month'],
        exp_year=card['exp_year'],
        cvc=card['cvc']
    )
    results.append({
        'card_last4': result['card_last4'],
        'status': result['status'],
        'message': result['message']
    })

# Save results
with open('results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['card_last4', 'status', 'message'])
    writer.writeheader()
    writer.writerows(results)

print(f"Checked {len(results)} cards. Results saved to results.csv")
```

### Example 8: Automated Testing with Retry Logic

```python
import time
from stripe_payment import StripePaymentProcessor

processor = StripePaymentProcessor()

def check_card_with_retry(card_number, exp_month, exp_year, cvc, max_retries=3):
    """Check card with automatic retry on errors"""
    for attempt in range(max_retries):
        try:
            result = processor.check_card(card_number, exp_month, exp_year, cvc)
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2)  # Wait 2 seconds before retry
            else:
                return {
                    'status': 'error',
                    'message': f'Failed after {max_retries} attempts: {str(e)}'
                }

# Usage
result = check_card_with_retry("4242424242424242", "12", "2025", "123")
print(result)
```

### Example 9: Logging and Monitoring

```python
import logging
from datetime import datetime
from stripe_payment import StripePaymentProcessor

# Setup logging
logging.basicConfig(
    filename='payment_checks.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

processor = StripePaymentProcessor()

def check_and_log(card_number, exp_month, exp_year, cvc):
    """Check card and log the result"""
    logging.info(f"Checking card ending in {card_number[-4:]}")
    
    result = processor.check_card(card_number, exp_month, exp_year, cvc)
    
    if result['status'] == 'valid':
        logging.info(f"Card valid - Brand: {result['card_brand']}")
    else:
        logging.warning(f"Card declined - Reason: {result['message']}")
    
    return result

# Usage
result = check_and_log("4242424242424242", "12", "2025", "123")
```

---

## Tips and Best Practices

### 1. Always Use Test Cards

```python
# Good: Using official test cards
processor = StripePaymentProcessor()
test_cards = processor.get_test_cards()
result = processor.check_card(test_cards['success'], "12", "2025", "123")

# Bad: Never use real card numbers
# result = processor.check_card("1234567890123456", ...)  # DON'T DO THIS
```

### 2. Handle Errors Gracefully

```python
try:
    result = processor.check_card(card_number, exp_month, exp_year, cvc)
    if result['status'] == 'valid':
        print("Card is valid")
    else:
        print(f"Card declined: {result['message']}")
except Exception as e:
    print(f"Error occurred: {e}")
```

### 3. Rate Limiting

```python
import time

cards = [...]  # List of cards to check

for card in cards:
    result = processor.check_card(...)
    time.sleep(1)  # Wait 1 second between requests
```

---

## Need More Help?

- Check the [README.md](README.md) for general information
- Read the [INSTALL.md](INSTALL.md) for installation issues
- Open an issue on GitHub for bugs or feature requests
