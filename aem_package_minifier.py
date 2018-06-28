#!/usr/bin/env python3

import zipfile
import fileinput
from optparse import OptionParser
import sys
import re
import os
import shutil

# Argument definitions
usage = "usage: %prog [options] arg"
parser = OptionParser(usage)
parser.add_option("-f", "--file", dest="filename", help="AEM package file")
options, args = parser.parse_args()
option_dic = vars(options)

def unzip_file(zipname, target_dir):
  print("Unzipping file '%s'..." % zipname)
  os.makedirs(target_dir)
  zipfile.ZipFile(zipname).extractall(target_dir)

def minify_files(path):
  for extension in ['bmp','gif','jpg','mp3','mp4','ogg','pdf','png','zip']:
    print("Start replacing %s files..." % extension)
    replacement_file_path = os.path.join(current_dir_path, 'smallest-files', '%s.%s' % (extension, extension))
    for root, _, files in os.walk(path):
      for f in files:
        file_path = os.path.abspath(os.path.join(root, f))
        if file_path.endswith('original') and re.search('\.(%s)\/_jcr_' % (extension), file_path):
          os.remove(file_path)
          shutil.copyfile(replacement_file_path, file_path)
          print("Replaced file '%s' with '%s'" % (file_path, replacement_file_path))

def create_new_package(target_path, source_dir):
  print("Zipping minified package...")
  shutil.make_archive(target_path, 'zip', source_dir)
  print("Minified package created at '%s'.zip" % target_path)

def alter_package_name(target_path):
  properties_path = os.path.join(target_path, 'META-INF', 'vault', 'properties.xml')
  with fileinput.FileInput(properties_path, inplace=True) as file:
    for line in file:
      match = re.findall('<entry key="name">([^<]+)</entry>', line)
      if match:
        new_package_name = "%s-minified" % match[0]
        print(line.replace(match[0], new_package_name), end='')
      else:
        print(line, end='')
  print("Renamed package name to '%s'" % new_package_name)

def calculate_filesize(filename):
  zip = zipfile.ZipFile(filename)

  size = sum([zinfo.file_size for zinfo in zip.filelist])
  package_size_mb = round(size/1000000, 2)
  print("Package size: %sMB" % package_size_mb)

  total_size = 0
  for zinfo in zip.filelist:
    if not zinfo.filename.endswith('original'):
      continue
    if re.search('\.(bmp|gif|jpg|mp3|mp4|ogg|pdf|png|zip)\/', zinfo.filename):
      total_size += zinfo.file_size
  obsolete_file_size_mb = round(total_size/1000000, 2)
  new_package_file_size_mb = round(package_size_mb - obsolete_file_size_mb, 2)
  print("Total size of files to minify: %sMB" % obsolete_file_size_mb)
  print("Target package size: %sMB (%s%%)" % (new_package_file_size_mb, round(new_package_file_size_mb/package_size_mb*100)))

# Define variables
package_path = option_dic['filename']
package_dir = os.path.dirname(os.path.abspath(package_path))
package_filename_without_extension = os.path.splitext(os.path.basename(package_path))[0]
temp_dir = os.path.join(package_dir, package_filename_without_extension + "-extract")
current_dir_path = os.path.dirname(os.path.realpath(__file__))
target_path_without_extension = os.path.join(package_dir, package_filename_without_extension + "-minified")

if os.path.exists(temp_dir):
  sys.exit("Temp directory '%s' already exists" % temp_dir)

if os.path.exists(target_path_without_extension + ".zip"):
  sys.exit("Target file '%s.zip' already exists" % target_path_without_extension)

# Execute commands
print("Start minifying package '%s'..." % package_path)
calculate_filesize(package_path)
unzip_file(package_path, temp_dir)
minify_files(temp_dir)
alter_package_name(temp_dir)
create_new_package(target_path_without_extension, temp_dir)
shutil.rmtree(temp_dir)
print("Finished minifying package")
