import json
import datetime

class Output:
  def output_bucket(self, o, prefix = ""):
    pass
  def output_object_metadata(self, o, prefix = ""):
    pass

class HumanReadable(Output):

  filesize_unit = ""

  def __init__(self, filesize_unit = ""):
  """constructor.

  Args:
    filesize_unit: A string value representing a filesize. Supported size are `B`, `KB`, `MB`, `GB` and `TB`.
      An empty value will convert the filesize to a fitting size.
      Any other values than the mentionned will be defaulted to `TB`. 
  """
    self.filesize_unit = filesize_unit

  def output_bucket(self, b):
    """Output a dto bucke object.
    
    Args:
      b: A awss3.dto.Bucket object.
    
    Returns:
        A string representing the given awss3.dto.Bucket object.
    """
    output = "-----Bucket-----\n"
    output += self._bucket_format(b)
    if b.object_metadata:
      output += self._object_metadata_format(b.object_metadata)
      
    return output

  def output_object_metadata(self, o, prefix = ""):
    """
    Args:
      o: A awss3.dto.ObjectMetadata object.

    Returns:
      A string representing the given awss3.dto.ObjectMetadata object.
    """
    output = "-----ObjectMetadata-----\n"
    output += self._object_metadata_format(o)
    return output

  def _bucket_format(self, b):
    output = ""
    output += "{}: {}\n".format("name", b.name)
    output += "{}: {}\n".format("date_created", b.date_created)
    return output

  def _object_metadata_format(self, o):
    output = ""
    output += "{}: {}\n".format("last_modified_date", o.last_modified_date)
    output += "{}: {}\n".format("number_of_object", o.number_of_object)
    output += "{}: {}\n".format("total_size", self._filesize_format(o.total_size, self.filesize_unit))
    output += "{}: {}\n".format("total_storage_classes", str(o.total_storage_classes))
    return output

  def _filesize_format(self, num, specific_unit = ""):
    for unit in ['B','KB','MB','GB']:
        if specific_unit:
          if specific_unit == unit:
            return "%3.2f%s" % (num, unit)
        elif abs(num) < 1000.0:
            return "%3.2f%s" % (num, unit)
        num /= 1000.0
    return "%.2f%s" % (num, 'TB')

class JSON(Output):
  def output_bucket(self, b):
  """Output a dto bucket object.
  
  Args:
    b: A awss3.dto.Bucket object.
  
  Returns:
      A json string representing the given awss3.dto.Bucket object.
  """

    return json.dumps(b.__dict__, default=self._json_serial)

  def output_object_metadata(self, o):
  """Output a dto object metadata object.
  
  Args:
    b: A awss3.dto.ObjectMetadata object.
  
  Returns:
      A json string representing the given awss3.dto.ObjectMetadata object.
  """
    return json.dumps(o.__dict__, default=self._json_serial)

  def _json_serial(self, obj):
    if isinstance(obj, datetime.datetime):
      return str(obj)
    if isinstance(obj, object):
      return obj.__dict__
    else:
      return obj
    raise TypeError ("Type not serializable")
