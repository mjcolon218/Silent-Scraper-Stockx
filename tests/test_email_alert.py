import boto3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Replace these with VERIFIED emails in your SES sandbox
FROM_EMAIL = "mjcolon218@gmail.com"
TO_EMAIL = "mauricecolon68@gmail.com"

# Sample test data
sneaker_name = "Air Jordan 4 Retro"
current_price = 180
target_price = 200
product_url = "https://stockx.com/air-jordan-4-retro"

# Initialize boto3 SES client
ses = boto3.client('ses', region_name="us-east-1")  # or your correct region

def test_send_mock_alert():
    try:
        response = ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [TO_EMAIL]},
            Message={
                'Subject': {'Data': f"🔥 Price Drop Alert: {sneaker_name}"},
                'Body': {
                    'Text': {
                        'Data': (
                            f"📢 Sneaker: {sneaker_name}\n"
                            f"💸 Current Price: ${current_price}\n"
                            f"🎯 Target Price: ${target_price}\n"
                            f"🔗 Product Link: {product_url}"
                        )
                    }
                }
            }
        )
        print("✅ Mock email sent successfully!")
        print("📧 SES Message ID:", response['MessageId'])

    except Exception as e:
        print("❌ Failed to send mock email:", e)

if __name__ == "__main__":
    test_send_mock_alert()
