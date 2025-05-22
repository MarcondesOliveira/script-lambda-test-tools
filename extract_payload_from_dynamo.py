import json
import sys
import boto3
from boto3.dynamodb.types import TypeDeserializer

deserializer = TypeDeserializer()

def dynamodb_to_dict(ddb_json):
    """Desserializa recursivamente um JSON no formato do DynamoDB para um dicionário comum."""
    def _deserialize(value):
        if isinstance(value, dict) and len(value) == 1:
            return deserializer.deserialize(value)
        elif isinstance(value, dict):
            return {k: _deserialize(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [_deserialize(i) for i in value]
        else:
            return value

    return _deserialize(ddb_json)

def wrap_as_sqs_event(payload_dict):
    """Gera o JSON no formato do Lambda Test Tools para SQS."""
    return {
        "Records": [
            {
                "messageId": "test-message-id",
                "receiptHandle": "test-receipt-handle",
                "body": json.dumps(payload_dict, default=str),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "0",
                    "SenderId": "test-sender",
                    "ApproximateFirstReceiveTimestamp": "0"
                },
                "messageAttributes": {},
                "md5OfBody": "test-md5",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:local:123456789012:test-queue",
                "awsRegion": "us-east-1"
            }
        ]
    }

def main():
    # Detecta se recebeu arquivo via argumento ou stdin
    if len(sys.argv) < 2:
        print("Uso: python extract_payload_from_dynamo.py <arquivo_dynamo.json>")
        sys.exit(1)

    input_path = sys.argv[1]
    with open(input_path, "r", encoding="utf-8") as f:
        dynamo_raw = json.load(f)

    # Desserializa do formato DynamoDB
    reconstructed = dynamodb_to_dict(dynamo_raw)

    # Gera evento para o Lambda Test Tools
    event = wrap_as_sqs_event(reconstructed)

    # Salva resultado em arquivo
    output_path = "sqs_event_for_lambda_test_tools.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(event, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Evento gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    main()
