import json
import datetime

class Output:
  def output_bucket(self, o, prefix = ""):
    pass
  def output_object_metadata(self, o, prefix = ""):
    pass

class HumanReadable(Output):
  def output_bucket(self, b):
    output = "-----Bucket-----\n"
    output += self._bucket_format(b)
    if b.object_metadata:
      output += self._object_metadata_format(b.object_metadata)
      
    return output

  def output_object_metadata(self, o, prefix = ""):
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
    output += "{}: {}\n".format("total_size", self._filesize_format(o.total_size))
    return output

  def _filesize_format(self, num):
    for unit in ['B','KB','MB','GB']:
        if abs(num) < 1000.0:
            return "%3.2f%s" % (num, unit)
        num /= 1000.0
    return "%.2f%s" % (num, 'TB')

class JSON(Output):
  def output_bucket(self, b):
    return json.dumps(b.__dict__, default=self._json_serial)

  def output_object_metadata(self, o):
    return json.dumps(o.__dict__, default=self._json_serial)

  def _json_serial(self, obj):
    if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial
    if isinstance(obj, object):
      return obj.__dict__
    else:
      return obj
    raise TypeError ("Type not serializable")
