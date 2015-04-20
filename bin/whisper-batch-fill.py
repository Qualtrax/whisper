#!/usr/bin/env python

import os
import sys
import signal
import optparse
import shutil

whisper_fill = __import__('whisper-fill')

try:
  import whisper
except ImportError:
  raise SystemExit('[ERROR] Please make sure whisper is installed properly')

def main(argv):
  # Ignore SIGPIPE
  signal.signal(signal.SIGPIPE, signal.SIG_DFL)

  option_parser = optparse.OptionParser(
    usage='''%prog [options] from_path to_path''')

  (options, args) = option_parser.parse_args()

  if len(args) < 2:
    option_parser.print_help()
    sys.exit(1)

  src = os.path.abspath(args[0])
  dest = os.path.abspath(args[1])

  srcs = { os.path.relpath(dirpath, src): filenames for (dirpath, dirnames, filenames) in os.walk(src) }
  dests = { os.path.relpath(dirpath, dest): filenames for (dirpath, dirnames, filenames) in os.walk(dest) }

  for rel in srcs.keys():
    if dests.has_key(rel):
      for f in srcs[rel]:
        s = os.path.join(src, rel, f)
        d = os.path.join(dest, rel, f)

        if os.path.exists(d): 
          print 'fill {0} {1}'.format(s, d)
          whisper_fill.main([s, d])
        else:
          print 'copy {0} {1}'.format(s, d)
          shutil.copy(s, d)
    else:
      print 'copytree {0} {1}'.format(s, d)
      s = os.path.join(src, rel)
      d = os.path.join(dest, rel)
      shutil.copytree(s, d)

if __name__ == "__main__":
  main(sys.argv[1:])
