

# Common backend utilities

import json
from decimal import Decimal

#Custom encoder for Decimal (DynamoDB numeric types)
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def response(status_code, body):
    """Format Lambda HTTP response"""
    return {
        "statusCode": status_code,
        "body": json.dumps(body, cls=DecimalEncoder),
        "headers": {"Content-Type": "application/json"}
    }