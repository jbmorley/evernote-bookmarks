#!/usr/bin/env python

# Copyright (c) 2014 Jason Barrie Morley
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import xml.etree.ElementTree as ElementTree
import datetime
import codecs
import time
import argparse

def datetime_to_epoch(dt):
  epoch = datetime.datetime(1970,1,1)
  et = (dt - epoch).total_seconds()
  return int(et)

def timestamp_to_datetime(ts):
  t = time.strptime(ts, "%Y%m%dT%H%M%SZ")
  dt = datetime.datetime.fromtimestamp(time.mktime(t))
  return dt

def timestamp_to_epoch(ts):
  dt = timestamp_to_datetime(ts)
  et = datetime_to_epoch(dt)
  return et

def convert(notes_file, bookmarks_file):

  bookmarks = []
  tree = ElementTree.parse(notes_file)
  for note in tree.getroot().findall('note'):
    title = note.find('title').text
    created = note.find('created').text
    url = note.find('note-attributes').find('source-url').text
    tags = map(lambda x: x.text, note.findall('tag'))
    bookmarks.append({'title': title, 'created': created, 'url': url, 'tags': tags})

  count = 0
  with codecs.open(bookmarks_file, 'w', 'utf-8') as f:
    f.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!--This is an automatically generated file.
    It will be read and overwritten.
    Do Not Edit! -->
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL>
""")

    for bookmark in bookmarks:
      print "%s - Created %s - [%s]" % (bookmark['title'], timestamp_to_datetime(bookmark['created']), ", ".join(bookmark['tags']))
      result = u"    <DT><A HREF=\"%s\" ADD_DATE=\"%d\" TAGS=\"%s\">%s</A>\n" % (bookmark['url'], timestamp_to_epoch(bookmark['created']),  ", ".join(bookmark['tags']), bookmark['title'])
      f.write(result)
      count += 1

    f.write("</DL>\n")

  print "Processed %d bookmarks." % count

def main():

  parser = argparse.ArgumentParser(description = "Convert Evernote XML Format (.enx) to the Netscape Bookmark File Format (bookmarks.html).")
  parser.add_argument('input', help = "Evernote .enx file to convert")
  parser.add_argument('output', help = "Output bookmarks.html file")
  options = parser.parse_args()

  convert(options.input, options.output)

if __name__ == '__main__':
  main()

