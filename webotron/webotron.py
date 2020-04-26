#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron: Deploy website with AWS.

Webotron automate the process of deploying static websites to AWS.
- Configure AWS S3 buckets
    - Create the buckets
    - Set up buckets for static website hosting
    - Deploy local files to buckets
- Configure DNS with AWS Route 53
- Configure a CDN and SSL with AWS CloudFront
"""



import boto3
import click
from bucket import BucketManager

session = boto3.Session(profile_name='tomking')
bucket_manager = BucketManager(session)
# s3 = session.resource('s3')


@click.group()
def cli():
    """Webtron deploys websites to AWS."""


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an S3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync content of PATHNAME to BUCKET."""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
