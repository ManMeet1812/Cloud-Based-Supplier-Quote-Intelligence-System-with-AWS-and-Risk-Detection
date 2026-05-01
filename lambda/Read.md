# Lambda Functions

This folder contains the AWS Lambda function code used in the backend.  
`SubmitQuoteFunction` processes supplier quotes, calculates total price, applies risk detection, saves records to DynamoDB, and triggers SNS alerts for anomaly quotes.  
`GetQuotesFunction` retrieves saved quote records for the dashboard.
