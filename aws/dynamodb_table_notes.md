
---

# `aws/dynamodb_table_notes.md`

```markdown
# DynamoDB Table Notes

## Table Name

SupplierQuotes

## Purpose

DynamoDB stores supplier quote records submitted through the frontend website.

## Key Design

The table stores quote records with a unique quote ID and timestamp.

Main fields stored:

```text
quoteId
supplierName
materialName
unitPrice
quantity
totalPrice
deliveryDays
region
fileUrl
riskStatus
riskReason
createdAt
