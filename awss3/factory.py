from awss3.dto import Bucket, ObjectMetadata

class Factory:
  pass

class BucketFactory(Factory):

  object_metadata_factory = None
  
  def __init__(self, object_metadata_factory):
    self.object_metadata_factory = object_metadata_factory
    pass

  def build_bucket(self, s3_bucket):
    b = Bucket()
    b.name = s3_bucket.name
    b.date_created = s3_bucket.creation_date
    return b

  def build_bucket_with_object_metadata(self, s3_bucket):
    b = self.build_bucket(s3_bucket)
    b.object_metadata = self.object_metadata_factory.build_object_metadata(s3_bucket)
    return b

class ObjectMetadataFactory(Factory):
  def build_object_metadata(self, s3_bucket):
    last_modified_date = s3_bucket.creation_date
    cpt = 0
    total_size = 0
    for obj in s3_bucket.objects.all():
      cpt += 1
      total_size += obj.size
      if last_modified_date < obj.last_modified:
        last_modified_date = obj.last_modified
    o = ObjectMetadata()
    o.number_of_object = cpt
    o.last_modified_date = last_modified_date
    o.total_size = total_size
    return o
