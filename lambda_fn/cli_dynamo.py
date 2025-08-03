# lamda_fn/cli_dynamo.py

import boto3
from decimal import Decimal
import argparse
from tabulate import tabulate

# DynamoDB table name
TABLE_NAME = "SneakerTracker"

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def add_sneaker(sku, name, target_price):
    table.put_item(
        Item={
            'sku': sku,
            'name': name,
            'target_price': Decimal(str(target_price)),
            'last_price': Decimal("0.0")
        }
    )
    print(f"✅ Added sneaker: {name} (SKU: {sku}) with target price ${target_price}")

def update_target(sku, new_price):
    response = table.update_item(
        Key={'sku': sku},
        UpdateExpression="SET target_price = :p",
        ExpressionAttributeValues={':p': Decimal(str(new_price))},
        ReturnValues="UPDATED_NEW"
    )
    print(f"✅ Updated SKU {sku} to new target price: ${new_price}")

def list_sneakers():
    response = table.scan()
    items = response.get('Items', [])
    if not items:
        print("⚠️ No sneakers found in table.")
        return

    table_data = [
        [s['sku'], s['name'], s.get('target_price', 'N/A'), s.get('last_price', 'N/A')]
        for s in items
    ]
    print(tabulate(table_data, headers=["SKU", "Name", "Target Price", "Last Price"]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Silent Scalper CLI for DynamoDB")
    subparsers = parser.add_subparsers(dest="command")

    # Add sneaker
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--sku", required=True)
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--target_price", required=True, type=float)

    # Update sneaker
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--sku", required=True)
    update_parser.add_argument("--target_price", required=True, type=float)

    # List sneakers
    subparsers.add_parser("list")

    args = parser.parse_args()

    if args.command == "add":
        add_sneaker(args.sku, args.name, args.target_price)
    elif args.command == "update":
        update_target(args.sku, args.price)
    elif args.command == "list":
        list_sneakers()
    else:
        parser.print_help()
