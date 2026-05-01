## System Architecture Diagram

```mermaid
flowchart TD
    A[Supplier / Admin User] --> B[S3 Static Website Frontend]

    B -->|Submit quote form| C[API Gateway]
    C -->|POST /submit-quote| D[SubmitQuoteFunction Lambda]
    C -->|GET /quotes| E[GetQuotesFunction Lambda]

    D -->|Calculate total price| D
    D -->|Apply risk detection logic| D
    D -->|Save quote record| F[DynamoDB SupplierQuotes Table]

    E -->|Read quote records| F
    F -->|Return quote data| E
    E -->|Dashboard data| B

    G[S3 Quote File Bucket] -->|Stores quote files| G
    B -->|File URL / S3 URI submitted| D
    D -->|Stores fileUrl in quote record| F

    D -->|If riskStatus = Anomaly| H[SNS QuoteAlerts Topic]
    H -->|Email notification| I[Admin Email Alert]
