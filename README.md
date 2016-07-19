# AWSS3

Simple python script to gather intel on amazon S3 buckets

## Fair warning

This program abuse in some ways the boto3 s3 bucket api. Especially the `--with-metadata` flag which will parse *every* objects of every bucket that fit the given filters. This could potentially cost you money.

You have been warned.

## Credentials

Credentials are auto-discovered by boto3. You should create the `~/.aws` directory and add your credentials in `~/.aws/credentials` file.

```
[default]
aws_access_key_id = you_key_id
aws_secret_access_key = your_secret_access_key
```

The region can be specified in the `~/.aws/config` file.

```
[default]
region=us-east-1
```

See [boto3 documentation](http://boto3.readthedocs.io/en/latest/guide/configuration.html) for more details.

## Installation

Running `make && make dev` will install the development version into `/usr/local/bin/awss3`.

## Developement

To install dependencies, `make`.

To install the development version, `make dev`.

To clean the install and start over, `make clean`.

To test, `make test`.

## TODOs

 - Packaging (deb, rpm, arch)
 - Threading (bucket output generation, object iteration)
 - Credentials (profile, credentials, region)
 - Move main into another module
 - Filters option (return bucket data based on object data i.e. return bucket data containing object name abc)
 - Add linter (pylint or other)
