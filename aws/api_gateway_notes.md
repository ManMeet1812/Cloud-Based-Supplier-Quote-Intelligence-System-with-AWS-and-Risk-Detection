# API Gateway Notes

## API Name

SupplierQuoteAPI

## API Type

HTTP API

## Purpose

API Gateway acts as the public entry point between the frontend website and AWS Lambda functions.

## Routes

| Method | Route | Lambda Function | Purpose |
|---|---|---|---|
| POST | /submit-quote | SubmitQuoteFunction | Submits a new supplier quote |
| GET | /quotes | GetQuotesFunction | Retrieves saved supplier quotes |

## CORS Configuration

CORS was enabled so the S3-hosted frontend can call the API Gateway endpoint from the browser.

Allowed settings:

```text
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: content-type,authorization
Access-Control-Allow-Methods: GET,POST,OPTIONS
