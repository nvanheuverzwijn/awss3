import re
import argparse

class store_regex(argparse.Action):
  def __call__(self, parser, args, values, option_string=None):
    try:
      p = re.compile(values)
      setattr(args, self.dest, p)
    except:
      parser.error("argument {}: invalid regex".format(option_string))

