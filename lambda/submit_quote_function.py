import json
import boto3
import uuid
from datetime import datetime, timezone
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

table = dynamodb.Table("SupplierQuotes")

SNS_TOPIC_ARN = "arn:aws:sns:ca-central-1:126697142801:QuoteAlerts"


def predict_risk(material_name, unit_price, quantity, delivery_days, region):
    material = material_name.strip().lower()
    price = Decimal(str(unit_price))
    qty = Decimal(str(quantity))
    days = int(delivery_days)

    expected_prices = {
        "steel": Decimal("950"),
        "concrete": Decimal("180"),
        "wood": Decimal("75"),
        "aluminum": Decimal("1600"),
        "copper": Decimal("8200")
    }

    large_order_limits = {
        "steel": Decimal("450"),
        "concrete": Decimal("1100"),
        "wood": Decimal("750"),
        "aluminum": Decimal("300"),
        "copper": Decimal("150")
    }

    if material not in expected_prices:
        return "Anomaly", "Unknown material type"

    base_price = expected_prices[material]
    high_threshold = base_price * Decimal("1.35")
    low_threshold = base_price * Decimal("0.55")

    if price > high_threshold and days >= 30:
        return "Anomaly", "High price and slow delivery"

    if price > high_threshold:
        return "Anomaly", "Unit price is much higher than expected"

    if price < low_threshold:
        return "Anomaly", "Unit price is unusually low"

    if days > 30:
        return "Anomaly", "Delivery time is unusually long"

    if qty >= large_order_limits[material] and price > base_price * Decimal("1.15"):
        return "Anomaly", "Large order has unexpectedly high unit price"

    return "Normal", "Quote is within expected range"


def send_anomaly_alert(
    supplier_name,
    material_name,
    unit_price,
    quantity,
    total_price,
    delivery_days,
    region,
    risk_reason,
    quote_id
):
    subject = "Supplier Quote Alert: Anomaly Detected"

    message = f"""
An anomaly supplier quote was detected.

Quote ID: {quote_id}
Supplier: {supplier_name}
Material: {material_name}
Unit Price: {unit_price}
Quantity: {quantity}
Total Price: {total_price}
Delivery Days: {delivery_days}
Region: {region}

Risk Reason:
{risk_reason}

Action:
Please review this supplier quote before approving.
"""

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )


def lambda_handler(event, context):
    try:
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        supplier_name = body["supplierName"]
        material_name = body["materialName"]
        unit_price = Decimal(str(body["unitPrice"]))
        quantity = Decimal(str(body["quantity"]))
        delivery_days = int(body["deliveryDays"])
        region = body.get("region", "Ontario")
        file_url = body.get("fileUrl", "")

        total_price = unit_price * quantity

        risk_status, risk_reason = predict_risk(
            material_name,
            unit_price,
            quantity,
            delivery_days,
            region
        )

        quote_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        item = {
            "materialName": material_name,
            "createdAt": created_at,
            "quoteId": quote_id,
            "supplierName": supplier_name,
            "unitPrice": unit_price,
            "quantity": quantity,
            "totalPrice": total_price,
            "deliveryDays": delivery_days,
            "region": region,
            "fileUrl": file_url,
            "riskStatus": risk_status,
            "riskReason": risk_reason
        }

        table.put_item(Item=item)

        alertSent = False

        if risk_status == "Anomaly":
            send_anomaly_alert(
                supplier_name=supplier_name,
                material_name=material_name,
                unit_price=unit_price,
                quantity=quantity,
                total_price=total_price,
                delivery_days=delivery_days,
                region=region,
                risk_reason=risk_reason,
                quote_id=quote_id
            )
            alertSent = True

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Quote saved successfully",
                "quoteId": quote_id,
                "materialName": material_name,
                "totalPrice": float(total_price),
                "riskStatus": risk_status,
                "riskReason": risk_reason,
                "alertSent": alertSent
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Error saving quote",
                "error": str(e)
            })
        }
