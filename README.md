# Cloud-Based Supplier Quote Intelligence System with AWS and Risk Detection

## Project Overview

This project is a cloud-based supplier quote management and risk detection system built using AWS serverless services.

The system allows suppliers to submit quote information through a web form, stores supplier quote records in DynamoDB, stores quote-related files in S3, evaluates quote risk, displays submitted quotes on a dashboard, and sends email alerts when an anomaly quote is detected.

The purpose of this project is to reduce manual spreadsheet-based quote comparison and improve pricing visibility, supplier quote tracking, and anomaly detection in procurement workflows.

---

## Project Background

This project was inspired by a business case report I developed in my **Entrepreneurship and Innovation Thinking** course. The report identified the need for a more centralized and automated supplier quote comparison system to reduce manual spreadsheet work, improve pricing visibility, and support faster decision-making.

Based on that business problem, I built this cloud-based prototype using AWS serverless services. The goal was to translate the business case into a working technical solution that demonstrates supplier quote submission, cloud storage, risk detection, dashboard viewing, and automated anomaly alerts.

---

## Problem Statement

Many supplier quote comparison processes rely on manual spreadsheets, email attachments, and disconnected records. This can make it difficult to compare supplier prices, identify unusual quotes, track quote documents, and quickly notify decision-makers when a quote requires review.

This project solves that problem by creating a centralized cloud-based system for supplier quote submission, quote storage, risk detection, dashboard viewing, and automated alerting.

---

## Key Features

- Supplier quote submission form
- Serverless backend using AWS Lambda
- API routes using Amazon API Gateway
- Quote record storage using Amazon DynamoDB
- Quote file storage using Amazon S3
- Frontend hosted using S3 Static Website Hosting
- Risk detection for unusual supplier quotes
- Dashboard to view submitted quotes
- SNS email alerts when anomaly quotes are detected
- Synthetic dataset creation for ML experimentation
- Dataset validation and graph analysis
- Locally trained ML model for quote risk classification

---

## AWS Services Used

| AWS Service | Purpose |
|---|---|
| Amazon S3 | Stores quote files and hosts the frontend website |
| Amazon DynamoDB | Stores supplier quote records |
| AWS Lambda | Processes submitted quotes and applies risk detection |
| Amazon API Gateway | Connects frontend requests to Lambda functions |
| Amazon SNS | Sends email alerts for anomaly quotes |
| IAM | Manages permissions for Lambda and AWS services |
| AWS CloudShell | Used to create and publish Lambda layers |
| Amazon CloudWatch | Used for Lambda execution logs and debugging |

---

## System Architecture

```text
Supplier / Admin User
        ↓
S3 Static Website Frontend
        ↓
API Gateway
        ↓
AWS Lambda
        ↓
DynamoDB

Quote File Storage → Amazon S3
Anomaly Alert → Amazon SNS Email
