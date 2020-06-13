import boto3
import sys
import click
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

if __name__ == '__main__':
	cli()
