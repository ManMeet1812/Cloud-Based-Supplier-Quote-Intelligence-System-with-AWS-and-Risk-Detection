
---

# `aws/sns_notes.md`

```markdown
# SNS Notes

## SNS Topic Name

QuoteAlerts

## Purpose

Amazon SNS sends email alerts when Lambda detects an anomaly supplier quote.

## Subscription

An email subscription was created and confirmed.

## Alert Trigger

SNS is triggered only when:

```text
riskStatus = Anomaly
