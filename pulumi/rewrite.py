import pulumi
import pulumi_aws as aws

def create_rewrite_lambda(rewrite_rules):
    """
    Creates a Lambda function for handling 302 redirects with the given rules.

    :param rewrite_rules: List of dictionaries with 'source' and 'target' keys for redirects
    :return: AWS Lambda Function resource
    """
    # Generate the Lambda function code dynamically based on redirect rules
    lambda_code = """
import json

def handler(event, context):
    request = event['Records'][0]['cf']['request']
    rewrites = {
"""
    for rule in rewrite_rules:
        lambda_code += f"        '{rule['source']}': '{rule['target']}',\n"

    lambda_code += """
    }
    if request['uri'] in rewrites:
        target = rewrites[request['uri']]
        print("Redirecting:", request['uri'], "->", target)  # Debug log

        # Return a 302 redirect response
        return {
            'status': '302',
            'statusDescription': 'Found',
            'headers': {
                'location': [{'key': 'Location', 'value': target}],
                'cache-control': [{'key': 'Cache-Control', 'value': 'no-cache'}],
            },
        }

    # If no rewrite rule matches, proceed with the original request
    return request
"""

    # Create IAM role for Lambda
    lambda_role = aws.iam.Role("rewriteLambdaRole",
        assume_role_policy="""{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "lambda.amazonaws.com",
                            "edgelambda.amazonaws.com"
                        ]
                    }
                }
            ]
        }"""
    )

    aws.iam.RolePolicyAttachment("rewriteLambdaPolicyAttachment",
        role=lambda_role.name,
        policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    )

    # Create the Lambda function in us-east-1
    rewrite_lambda = aws.lambda_.Function("rewriteLambda",
        role=lambda_role.arn,
        runtime="python3.12",  # Using python3.12 runtime
        handler="index.handler",
        code=pulumi.AssetArchive({
            "index.py": pulumi.StringAsset(lambda_code),
        }),
        publish=True,
        opts=pulumi.ResourceOptions(provider=aws.Provider("us-east-1", region="us-east-1"))
    )

    return rewrite_lambda
