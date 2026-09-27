import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from aws.lambda_function import lambda_handler

def run_simulation():
    print("=" * 70)
    print(" SIMULATING AWS S3 -> AWS LAMBDA DATA VALIDATION PIPELINE")
    print("=" * 70)

    base_dir = os.path.dirname(__file__)
    valid_csv_path = os.path.join(base_dir, 'sample_s3_events', 'batch_orders_valid.csv')
    corrupted_csv_path = os.path.join(base_dir, 'sample_s3_events', 'batch_orders_corrupted.csv')

    # 1. Processing Valid Batch
    print("\n[SCENARIO 1] Ingesting Clean Batch: 'batch_orders_valid.csv' via S3 Event")
    with open(valid_csv_path, 'r') as f:
        valid_content = f.read()

    event_valid = {
        'Records': [{'s3': {'bucket': {'name': 'retail-orders-s3'}, 'object': {'key': 'incoming/batch_orders_valid.csv'}}}],
        'mock_s3_file_content': valid_content
    }

    resp_valid = lambda_handler(event_valid)
    print(f"Status Code: {resp_valid['statusCode']}")
    print(f"Summary: {json.dumps(resp_valid['summary'], indent=2)}")
    print(f"Successfully processed {len(resp_valid['valid_records'])} valid order records.")

    # 2. Processing Corrupted Batch
    print("\n[SCENARIO 2] Ingesting Corrupted Batch: 'batch_orders_corrupted.csv' (Data Quality Injection)")
    with open(corrupted_csv_path, 'r') as f:
        corrupted_content = f.read()

    event_corrupted = {
        'Records': [{'s3': {'bucket': {'name': 'retail-orders-s3'}, 'object': {'key': 'incoming/batch_orders_corrupted.csv'}}}],
        'mock_s3_file_content': corrupted_content
    }

    resp_corrupted = lambda_handler(event_corrupted)
    print(f"Status Code: {resp_corrupted['statusCode']}")
    print(f"Summary: {json.dumps(resp_corrupted['summary'], indent=2)}")
    print(f"Rejected Records Count: {len(resp_corrupted['rejected_records'])}")
    for item in resp_corrupted['rejected_records']:
        print(f"  - Row {item.get('row_number')}: {item.get('reasons')}")

    print("\n Pipeline simulation executed successfully without errors.")

if __name__ == '__main__':
    run_simulation()
