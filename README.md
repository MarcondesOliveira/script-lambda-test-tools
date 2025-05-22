# 🧪 Lambda Test Tools — Gerar Evento SQS a partir de Item do DynamoDB

Este utilitário permite transformar um **item exportado do DynamoDB** (no formato JSON com tipos `"S"`, `"M"`, `"N"`, etc.) em um **evento SQS completo**, pronto para testes com [AWS Lambda Test Tools](https://github.com/aws/aws-lambda-dotnet/tree/master/Tools/LambdaTestTool).

---

## 📦 Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Acesso ao item do DynamoDB (via Console ou CLI)

---

## ⚙️ Instalação

```bash
# 1. Crie um ambiente virtual
python -m venv venv

# 2. Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# 3. Instale o boto3 (necessário para desserializar o JSON do DynamoDB)
pip install boto3
```

---

## 📁 Estrutura esperada

```
.
├── extract_payload_from_dynamo.py          # ← Script principal
├── dynamo_item.json                        # ← JSON copiado do DynamoDB
└── sqs_event_for_lambda_test_tools.json    # ← Arquivo gerado para o Lambda Test Tools
```

---

## 📝 Exportando o Item do DynamoDB

1. Acesse o [Console do AWS DynamoDB](https://console.aws.amazon.com/dynamodb/).
2. Navegue até a tabela e clique no item desejado.
3. Clique em **"View item as JSON"**.
4. Copie o conteúdo e cole no arquivo `dynamo_item.json`.

⚠️ O JSON precisa manter os tipos DynamoDB, como `"S"` para strings, `"N"` para números, `"M"` para mapas, etc.

---

## 🚀 Rodando o Script

```bash
python extract_payload_from_dynamo.py dynamo_item.json
```

Ao executar:

- O item do Dynamo será desserializado para JSON puro;
- O payload será empacotado no formato SQS;
- Um novo arquivo `sqs_event_for_lambda_test_tools.json` será criado.

---

## ✅ Verificando o Resultado

Abra o arquivo `sqs_event_for_lambda_test_tools.json`. Você verá algo como:

```json
{
  "Records": [
    {
      "messageId": "test-message-id",
      "receiptHandle": "test-receipt-handle",
      "body": "{ \"UniqueId\": \"abc123\", \"Amount\": 1000.0, ... }",
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
```

---

## 🧪 Usando no AWS .NET Core Mock Lambda Test Tool

![AWS .NET Core Mock Lambda Test Tool](https://raw.githubusercontent.com/aws/aws-lambda-dotnet/refs/heads/master/Tools/LambdaTestTool/Resources/TestHarness.png)

1. Abra o **AWS .NET Core Mock Lambda Test Tool** (dotnet-lambda-test-tool), conforme a imagem acima.

2. No campo **Function Input**, cole o conteúdo de `sqs_event_for_lambda_test_tools.json`.

3. Clique em **"Execute Function"** para simular a execução da sua Lambda.
