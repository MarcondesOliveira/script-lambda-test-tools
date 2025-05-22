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
