# lambda_fn/pricetracker.py

import sys
import os
import logging
import json
import boto3
from decimal import Decimal

# Add root path so Python can find the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.stockx_scraper import fetch_sneaker_data  # Update this import if your structure differs

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients (region_name ensures local runs work properly)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
ses = boto3.client('ses', region_name='us-east-1')

# Target table
table = dynamodb.Table('SneakerTracker')

def lambda_handler(event, context):
    response = table.scan()
    sneakers = response.get('Items', [])

    for sneaker in sneakers:
        sku = sneaker['sku']
        name = sneaker['name']
        target_price = float(sneaker['target_price'])
        url = f"https://stockx.com/search?s={sku.replace(' ', '%20')}"

        logger.info(f"🔍 Checking {name} (SKU: {sku}) with target price ${target_price}...")

        current_price = fetch_sneaker_data(url)

        if current_price and isinstance(current_price, list):
            try:
                # Extract and clean price
                price_str = current_price[0]['price']  # e.g., "$210"
                price_value = float(price_str)

                logger.info(f"Current price of {name}: ${price_value}")

                if price_value <= target_price:
                    logger.info(f"🔥 Price Alert: {name} dropped to ${price_value}!")

                    # Send SES alert
                    ses.send_email(
                        Source='mjcolon218@gmail.com',
                        Destination={'ToAddresses': ['mauricecolon68@gmail.com']},
                        Message={
                            'Subject': {'Data': f"🔥 Price Drop Alert: {name}"},
                            'Body': {
                                'Text': {
                                    'Data': f"Current Price: ${price_value}\nTarget Price: ${target_price}\nLink: {url}"
                                }
                            }
                        }
                    )

                # Update last_price in DynamoDB
                table.update_item(
                    Key={'sku': sku},
                    UpdateExpression="set last_price = :p",
                    ExpressionAttributeValues={':p': Decimal(str(price_value))}
                )
            except Exception as e:
                logger.error(f"❌ Error processing {name} (SKU: {sku}): {e}")
        else:
            logger.warning(f"⚠️ No valid price data returned for {name} (SKU: {sku})")

    return {
        'statusCode': 200,
        'body': json.dumps('Sneaker price check complete.')
    }

# Local testing support
if __name__ == "__main__":
    lambda_handler({}, {})
