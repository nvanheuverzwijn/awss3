class DTO:
  pass

class Bucket(DTO):
  name = ""
  date_created = None
  object_metadata = None

class ObjectMetadata(DTO):
  number_of_object = 0
  last_modified_date = None
  total_size = 0
  total_storage_classes = {}
