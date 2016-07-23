from awss3.dto import Bucket, ObjectMetadata

class Factory:
  pass

class BucketFactory(Factory):

  object_metadata_factory = None
  
  def __init__(self, object_metadata_factory):
    """constructor

    Args:
      object_metadata_factory: An awss3.factory.ObjectMetadataFactory
    """
    self.object_metadata_factory = object_metadata_factory
    pass

  def build_bucket(self, s3_bucket):
    """build a bucket dto object from a boto3 s3_bucket object
    Args:
      s3_bucket: A boto3 s3 bucket object
    Returns:
      awss3.dto.Bucket
    """
    b = Bucket()
    b.name = s3_bucket.name
    b.date_created = s3_bucket.creation_date
    return b

  def build_bucket_with_object_metadata(self, s3_bucket):
    """build a bucket dto object from a boto3 s3_bucket object
    This will also parse every objects of the given s3_bucket.

    Args:
      s3_bucket: A boto3 s3 bucket object

    Returns:
      awss3.dto.Bucket
    """
    b = self.build_bucket(s3_bucket)
    b.object_metadata = self.object_metadata_factory.build_object_metadata(s3_bucket)
    return b

class ObjectMetadataFactory(Factory):

  def build_object_metadata(self, s3_bucket):
    """Parse all objects from the given s3_bucket and build an object metadata dto.

    Args:
      s3_bucket: A boto3 s3 bucket object

    Returns:
      awss3.dto.ObjectMetadata
    """
    last_modified_date = s3_bucket.creation_date
    storage_classes = {}
    cpt = 0
    total_size = 0
    for s3_object in s3_bucket.objects.all():
      cpt += 1
      total_size += s3_object.size
      if last_modified_date < s3_object.last_modified:
        last_modified_date = s3_object.last_modified
      storage_classes[s3_object.storage_class] = storage_classes.setdefault(s3_object.storage_class, 0) + 1
    o = ObjectMetadata()
    o.number_of_object = cpt
    o.last_modified_date = last_modified_date
    o.total_size = total_size
    o.total_storage_classes = storage_classes
    return o
