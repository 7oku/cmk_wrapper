#!/usr/bin/env python
import argparse
import sys
import os
import csv
import time
import subprocess

if __name__ == '__main__':

  # Get args
  parser = argparse.ArgumentParser(description="Run a check_mk plugin with a defined interval")
  parser.add_argument("-p", "--plugin", help="Full Path to the plugin (e.g. /var/lib/check_apt)",required=True)
  parser.add_argument("-i", "--interval", help="Interval in seconds (e.g. 3600)",required=True)
  args = parser.parse_args()

  plugin_filename = os.path.basename(args.plugin)
  statusfile = "/tmp/"+plugin_filename+".cmkwrap"
  plugin = args.plugin
  interval = int(args.interval)

  ts = time.time()

  # Wrapper
  def toberun(ts,interval):
    ''' Determine if we need to give the plugin a new run'''    
 
   # Create sample Data if not there!
    if not os.path.exists(statusfile):
      f = csv.writer(open(statusfile, "w"))
      samplestatus = { 'lastts': 0, 'statuscode': "2", 'message':  plugin_filename+" check never ran!\n" }
      for key,value in samplestatus.items():
        f.writerow([key, value])
      return True;

    # read contents
    else:
      laststatus = {}
      for key, value in csv.reader(open(statusfile, "r")):
        laststatus[key] = value

      # should we run?
      delta = ts - float(laststatus['lastts'])
      if delta < interval:
        status_message = laststatus['message']+" (Checked %d seconds ago)\n" % delta
        sys.stdout.write(status_message)
        sys.exit(int(laststatus['statuscode']))

      else:
        return True;

if toberun(ts,interval):
  
  plugin_proc = subprocess.Popen([plugin], stdout=subprocess.PIPE)
  plugin_output = plugin_proc.communicate()[0]
  plugin_rcode = plugin_proc.returncode

  status = { 'lastts': ts, 'statuscode': plugin_rcode, 'message': plugin_output.rstrip('\n') }
  f = csv.writer(open(statusfile, "w"))
  for key,value in status.items():
    f.writerow([key, value])
  sys.stdout.write(plugin_output)
  sys.exit(int(plugin_rcode))
