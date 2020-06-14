import boto3
import sys
import click
from botocore.exceptions import ClientError
session = boto3.Session(profile_name='travis')
s3 = session.resource('s3')

@click.group()
def cli():
	"webotron deploys web to aws"
	pass

@cli.command('list-buckets')
def list_buckets():
	"List all s3 buckets"
	for bucket in s3.buckets.all():
		print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
	"list objects in an s3"
	bucket = s3.Bucket(bucket)
	for obj in bucket.objects.all():
		print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
	"Create and configure s3 bucket"
	s3_bucket = None

	try:
		s3_bucket = s3.create_bucket(Bucket=bucket)
	except ClientError as e:
		if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
			s3_bucket=s3.Bucket(bucket)
		else:
			raise 3

	policy = """
	{
	"Version":"2012-10-17",
	"Statement":[
	{
	  "Sid":"PublicRead",
	  "Effect":"Allow",
	  "Principal": "*",
	  "Action":["s3:GetObject"],
	  "Resource":["arn:aws:s3:::%s/*"]
	}
	]
	}
	"""% s3_bucket.name
	policy = policy.strip()
	pol = s3_bucket.Policy()
	pol.put(Policy=policy)

	ws = s3_bucket.Website()
	ws.put(WebsiteConfiguration={
	        'ErrorDocument': {
	            'Key': 'error.html'
	        },
	        'IndexDocument': {
	            'Suffix': 'index.html'
	        }})

	return


if __name__ == '__main__':
	cli()
