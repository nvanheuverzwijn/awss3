import datetime
import unittest
from unittest.mock import Mock
from awss3.factory import BucketFactory, ObjectMetadataFactory

class BucketFactoryTestCase(unittest.TestCase):

  def setUp(self):
    self.bucket_factory = BucketFactory(Mock(spec=ObjectMetadataFactory))

  def test_givenS3Bucket_whenBuildBucket_thenBucketDTOCorrectlyReflectS3Bucket(self):
    s3_bucket = self._givenS3Bucket()

    b = self.bucket_factory.build_bucket(s3_bucket)

    self.assertEqual(s3_bucket.name, b.name)
    self.assertEqual(s3_bucket.creation_date, b.date_created)
    self.assertEqual(None, b.object_metadata)

  def test_givenS3BucketWithOneObject_whenBuildBucketWithMetadata_thenBucketDTOObjectMetadataIsNotNone(self):
    s3_bucket = self._givenS3BucketWithOneObject()

    b = self.bucket_factory.build_bucket_with_object_metadata(s3_bucket)

    self.assertNotEqual(None, b.object_metadata)

  def _givenS3Bucket(self):
    s3_bucket = Mock()
    s3_bucket.name = "444-test"
    s3_bucket.creation_date = datetime.datetime(2016, 1, 1, 0, 0, 0)
    return s3_bucket

  def _givenS3BucketWithOneObject(self):
    mock_object_metadata_factory = Mock(spec=ObjectMetadataFactory)
    mock_object_metadata_factory.build_object_metadata.return_value = Mock()
    self.bucket_factory = BucketFactory(mock_object_metadata_factory)
    return self._givenS3Bucket()

class ObjectMetadataFactoryTestCase(unittest.TestCase):

  def setUp(self):
    self.object_metadata_factory = ObjectMetadataFactory()

  def test_givenS3BucketWithOneObject_whenBuildObjectMetadata_thenObjectMetadataCorrectlyReflectS3BucketObjects(self):
    s3_object = self._givenS3Object(datetime.datetime(2016, 1, 1, 0, 0, 0), 3782)
    s3_bucket = self._givenS3Bucket([s3_object])

    object_metadata = self.object_metadata_factory.build_object_metadata(s3_bucket)

    self.assertEqual(1, object_metadata.number_of_object)
    self.assertEqual(s3_object.last_modified, object_metadata.last_modified_date)
    self.assertEqual(s3_object.size, object_metadata.total_size)

  def test_givenS3BucketWithTwoObject_whenBuildObjectMetadata_thenSizeCorrectlyAddUp(self):
    s3_objects = [
      self._givenS3Object(datetime.datetime(2016, 1, 1, 0, 0, 0), 3782),
      self._givenS3Object(datetime.datetime(2016, 1, 1, 0, 0, 0), 5722)
    ]
    s3_bucket = self._givenS3Bucket(s3_objects)

    object_metadata = self.object_metadata_factory.build_object_metadata(s3_bucket)

    self.assertEqual(s3_objects[0].size + s3_objects[1].size, object_metadata.total_size)

  def test_givenS3BucketWithTwoObjectHavingDifferentModfiedDate_whenBuildObjectMetadata_thenLastModfiedDateIsSetToLatestDate(self):
    s3_objects = [
      self._givenS3Object(datetime.datetime(2016, 1, 1, 0, 0, 0), 3782),
      self._givenS3Object(datetime.datetime.max, 5722)
    ]
    s3_bucket = self._givenS3Bucket(s3_objects)

    object_metadata = self.object_metadata_factory.build_object_metadata(s3_bucket)

    self.assertEqual(datetime.datetime.max, object_metadata.last_modified_date)

  def test_givenS3BucketWithoutObject_whenBuildObjectMetadata_thenLastModifiedDateIsSetToBucketCreationDate(self):
    s3_bucket = self._givenS3Bucket()

    object_metadata = self.object_metadata_factory.build_object_metadata(s3_bucket)

    self.assertEqual(s3_bucket.creation_date, object_metadata.last_modified_date)

  def _givenS3Object(self, last_modified, size):
    s3_object = Mock()
    s3_object.last_modified = last_modified
    s3_object.size = size
    return s3_object

  def _givenS3Bucket(self, s3_objects = []):
    s3_bucket = Mock()
    s3_bucket.creation_date = datetime.datetime(2016, 1, 1, 0, 0, 0)
    s3_bucket.objects.all.return_value = s3_objects

    return s3_bucket    
