Supplier/Admin User
        ↓
S3 Static Website Frontend
        ↓
API Gateway
        ↓
SubmitQuoteFunction Lambda
        ↓
DynamoDB SupplierQuotes Table

S3 Quote File Bucket
        ↑
Quote file link stored in DynamoDB

If riskStatus = Anomaly
        ↓
SNS QuoteAlerts
        ↓
Admin Email Alert
