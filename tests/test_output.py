import json
import datetime
import unittest
from unittest.mock import Mock
from awss3.output import HumanReadable, JSON
from awss3.dto import Bucket, ObjectMetadata

class HumanReadableTestCase(unittest.TestCase):

  def setUp(self):
    self.output = HumanReadable()

  def test_givenDTOBucket_whenOutputBucket_thenBucketDTONameIsInOutput(self):
    bucket = self._givenDTOBucket()

    output = self.output.output_bucket(bucket)

    self.assertIn(bucket.name, output)
    self.assertIn("name", output)

  def test_givenDTOBucket_whenOutputBucket_thenBucketDTODateCreatedIsInOutput(self):
    bucket = self._givenDTOBucket()

    output = self.output.output_bucket(bucket)

    self.assertIn(str(bucket.date_created), output)
    self.assertIn("date_created", output)

  def test_givenDTOBucketWithObjectMetadata_whenOutputBucket_thenObjectMetadataNumberOfObjectIsInOutput(self):
    object_metadata = self._givenDTOObjectMetadata()
    bucket = self._givenDTOBucket(object_metadata)

    output = self.output.output_bucket(bucket)

    self.assertIn(str(bucket.object_metadata.number_of_object), output)
    self.assertIn("number_of_object", output)

  def test_givenDTOBucketWithObjectMetadata_whenOutputBucket_thenObjectMetadataLastModifiedDateIsInOutput(self):
    object_metadata = self._givenDTOObjectMetadata()
    bucket = self._givenDTOBucket(object_metadata)

    output = self.output.output_bucket(bucket)

    self.assertIn(str(bucket.object_metadata.last_modified_date), output)
    self.assertIn("last_modified_date", output)

  def test_givenDTOBucketWithObjectMetadata_whenOutputBucketWithFilesizeToByte_thenObjectMetadataTotalSizeIsInOutputAsByte(self):
    object_metadata = self._givenDTOObjectMetadata()
    bucket = self._givenDTOBucket(object_metadata)

    self.output.filesize_unit = "B"
    output_byte = self.output.output_bucket(bucket)

    self.assertIn(str(bucket.object_metadata.total_size), output_byte)
    self.assertIn("total_size", output_byte)

  def test_givenDTOBucketWithObjectMetadata_whenOutputBucketWithDifferentFilesizeFormat_thenObjectMetadataTotalSizeIsInOutputWithProperFileSize(self):
    object_metadata = self._givenDTOObjectMetadata()
    bucket = self._givenDTOBucket(object_metadata)

    self.output.filesize_unit = "B"
    output_byte = self.output.output_bucket(bucket)
    self.output.filesize_unit = "KB"
    output_kilobyte = self.output.output_bucket(bucket)
    self.output.filesize_unit = "MB"
    output_megabyte = self.output.output_bucket(bucket)
    self.output.filesize_unit = "GB"
    output_gigabyte = self.output.output_bucket(bucket)
    self.output.filesize_unit = "ANYTHINELSE"
    output_anythingelsebyte = self.output.output_bucket(bucket)

    self.assertIn("B", output_kilobyte)
    self.assertIn("KB", output_kilobyte)
    self.assertIn("MB", output_megabyte)
    self.assertIn("GB", output_gigabyte)
    self.assertIn("TB", output_anythingelsebyte)

  def _givenDTOBucket(self, object_metadata = None):
    bucket = Bucket()
    bucket.name = "444-test"
    bucket.date_created = datetime.datetime(2016, 1, 1, 0, 0, 0)
    bucket.object_metadata = object_metadata
    return bucket

  def _givenDTOObjectMetadata(self):
    object_metadata = ObjectMetadata()
    object_metadata.number_of_object = 2
    object_metadata.last_modified_date = datetime.datetime(2016, 1, 1, 0, 0, 0)
    object_metadata.total_size = 2000
    return object_metadata

class JSONTestCase(unittest.TestCase):

  def setUp(self):
    self.output = JSON()

  def test_givenDTOBucket_whenOutputJson_thenProperlySerialized(self):
    bucket = self._givenDTOBucket()
    
    output = self.output.output_bucket(bucket)

    deserialized_bucket = json.loads(output)   
    self.assertEqual(bucket.name, deserialized_bucket["name"])
    self.assertEqual(str(bucket.date_created), deserialized_bucket["date_created"])

  def test_givenDTOObjectMetadata_whenOutputJson_thenProperlySerialized(self):
    object_metadata = self._givenDTOObjectMetadata()

    output = self.output.output_object_metadata(object_metadata)

    deserialized_object_metadata = json.loads(output)   
    self.assertEqual(object_metadata.number_of_object, deserialized_object_metadata["number_of_object"])
    self.assertEqual(str(object_metadata.last_modified_date), deserialized_object_metadata["last_modified_date"])
    self.assertEqual(object_metadata.total_size, deserialized_object_metadata["total_size"])

  def _givenDTOBucket(self, object_metadata = None):
    bucket = Bucket()
    bucket.name = "444-test"
    bucket.date_created = datetime.datetime(2016, 1, 1, 0, 0, 0)
    bucket.object_metadata = object_metadata
    return bucket

  def _givenDTOObjectMetadata(self):
    object_metadata = ObjectMetadata()
    object_metadata.number_of_object = 2
    object_metadata.last_modified_date = datetime.datetime(2016, 1, 1, 0, 0, 0)
    object_metadata.total_size = 2000
    return object_metadata
