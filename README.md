# AWSS3

Simple python script to gather intel on amazon S3 buckets

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
