import pulumi
import pulumi_aws as aws
import pulumi_cloudflare as cloudflare
from datetime import datetime, timedelta
from pulumi import FileAsset
from rewrite import create_rewrite_lambda

# Config
config = pulumi.Config()
domain_name = config.require("domain")
zone_id = config.require("zone_id")
certificate_arn = config.require("certificate_arn")
notifications_file_path = config.require("notifications_file_path")  # ../stage/notifications.json
schema_file_path = config.require("schema_file_path")

name_prefix = pulumi.get_project() + "-" + pulumi.get_stack()

# Define rewrite rules
rewrite_rules = [
    {"source": "/notifications.json", "target": "/2.0/notifications.json"},
    {"source": "/latest/notifications.json", "target": "/2.0/notifications.json"},
]

# Create the rewrite Lambda function using the rules
rewrite_lambda = create_rewrite_lambda(rewrite_rules)

# Create an S3 bucket for hosting without ACLs
bucket = aws.s3.Bucket(
    name_prefix,
    bucket=name_prefix,
    website={
        'index_document': 'notifications.json',
    }
)

# Create a CloudFront Origin Access Identity (OAI)
origin_access_identity = aws.cloudfront.OriginAccessIdentity(
    "origin_access_identity",
    comment="OAI for accessing S3 notifications bucket"
)

# Create a bucket policy using aws.iam.get_policy_document
bucket_policy_document = aws.iam.get_policy_document(
    statements=[{
        "effect": "Allow",
        "actions": ["s3:GetObject"],
        "principals": [{
            "type": "AWS",
            "identifiers": [origin_access_identity.iam_arn],
        }],
        "resources": [
            f"arn:aws:s3:::{name_prefix}",
            f"arn:aws:s3:::{name_prefix}/*",
        ],
    }]
)

# Apply the bucket policy to allow CloudFront OAI access to the S3 bucket
bucket_policy = aws.s3.BucketPolicy(
    "bucketPolicy",
    bucket=bucket.id,
    policy=bucket_policy_document.json
)

# Upload the notifications.json file without ACLs
notifications_file = aws.s3.BucketObject(
    'notifications_json',
    bucket=bucket.id,
    key='2.0/notifications.json',
    source=FileAsset(notifications_file_path),
    content_type='application/json',
    metadata={"cache-control": "max-age=21600"}  # Cache for 6 hours
)

# Upload the notifications.json file without ACLs
schema_file = aws.s3.BucketObject(
    'schema_json',
    bucket=bucket.id,
    key='schemas/1.0/schema.json',
    source=FileAsset(schema_file_path),
    content_type='application/json',
    metadata={"cache-control": "max-age=21600"}  # Cache for 6 hours
)

# Calculate Expires header: current time + 6 hours
expires_time = (datetime.utcnow() + timedelta(hours=6)).strftime("%a, %d %b %Y %H:%M:%S GMT")

# Create a Response Headers Policy for Cache-Control and Expires
response_headers_policy = aws.cloudfront.ResponseHeadersPolicy(
    "cacheControlAndExpiresPolicy",
    name="cacheControlAndExpiresPolicy",
    comment="Set Cache-Control and Expires headers for all responses",
    custom_headers_config={
        "items": [
            {
                "header": "Cache-Control",
                "value": "max-age=21600",  # Cache for 6 hours
                "override": True  # Override any origin headers
            },
            {
                "header": "Expires",
                "value": expires_time,  # Static expires value
                "override": True  # Override any origin headers
            }
        ]
    }
)

# CloudFront distribution using the OAI for S3 access
cloudfront_distribution = aws.cloudfront.Distribution(
    'notifications_cf_distribution',
    origins=[{
        'domain_name': bucket.bucket_regional_domain_name,
        'origin_id': bucket.id,
        's3_origin_config': {
            'origin_access_identity': origin_access_identity.cloudfront_access_identity_path
        },
    }],
    comment=name_prefix,
    enabled=True,
    default_root_object='notifications.json',
    default_cache_behavior={
        'allowed_methods': ['GET', 'HEAD'],
        'cached_methods': ['GET', 'HEAD'],
        'target_origin_id': bucket.id,
        'viewer_protocol_policy': 'redirect-to-https',
        'forwarded_values': {
            'query_string': False,
            'cookies': {
                'forward': 'none'
            },
        },
        'lambda_function_associations': [{
            'event_type': 'origin-request',
            'lambda_arn': pulumi.Output.all(
                arn=rewrite_lambda.arn,
                version=rewrite_lambda.version
            ).apply(
                lambda values: f"{values['arn']}:{values['version']}"
            )
        }],
        'response_headers_policy_id': response_headers_policy.id
    },
    viewer_certificate={
        'acm_certificate_arn': certificate_arn,
        'ssl_support_method': 'sni-only',
        'minimum_protocol_version': 'TLSv1.2_2019',
    },
    restrictions={
        'geo_restriction': {
            'restriction_type': 'none',
        },
    },
    aliases=[domain_name],
)

# Create a Cloudflare DNS entry pointing to the CloudFront distribution
dns_record = cloudflare.Record(
    'notifications_dns_record',
    zone_id=zone_id,
    name=domain_name,
    type='CNAME',
    content=cloudfront_distribution.domain_name,
)

# Export the CloudFront distribution URL (SSL-enabled)
pulumi.export('cloudfront_url', cloudfront_distribution.domain_name)
