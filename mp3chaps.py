#!/usr/bin/env python
# *-* encoding: utf-8 -*-

"""
Usage:
  mp3chaps.py -h
  mp3chaps.py ( -l | -i | -r ) <filename>

Options:
  -h  Show this help text
  -l  List chapters in <filename>
  -i  Import chapters into <filename> (from <filename[w/o.ext]>.chp)
  -r  Remove chapters from <filename>

"""

from eyed3.id3 import Tag
from eyed3 import core
from docopt import docopt
import os

def to_millisecs(time):
  h, m, s = [float(x) for x in time.split(':')]
  return int((h*60*60 + m*60 + s) * 1000 + 25)
  # correction of +25ms # bug in eyed3 ?

def to_hms(secs):
  s = int(secs) // 1000
  return '{:02}:{:02}:{:02}'.format(s//3600, s%3600//60, s%60)

def list_chaps(tag):
  'list chapters in tag'
  for chap in tag.chapters:
    print(to_hms(chap.times[0]), '-', chap.sub_frames.get(b'TIT2')[0]._text)

def remove_chaps(tag):
  'remove all the chapters and save tag to file'
  chaps = [chap for chap in tag.chapters]
  for chap in chaps:
    print('removing {}'.format(chap.sub_frames.get(b'TIT2')[0]._text))
    tag.chapters.remove(chap.element_id)
  tag.save()

def parse_chapters_file(fname):
  filename, ext = os.path.splitext(fname)
  chapters_fname = '{}.chp'.format(filename)
  #print(chapters_fname)
  chaps = []
  with open(chapters_fname, 'r') as f:
    for line in f.readlines():
      time, title = line.split()[0], ' '.join(line.split()[1:])
      chaps.append((to_millisecs(time), title))
  return chaps

def add_chapters(tag, fname, total_length):
  'add chapters from filename.chp'
  chaps = parse_chapters_file(fname)
  total_length_ms = total_length * 1000
  #print(chaps, total_length_ms)
  tag.setTextFrame(b'TLEN', str(int(total_length_ms)))
  chaps_ = []
  for i, chap in enumerate(chaps):
    if i < (len(chaps)-1):
      chaps_.append( ((chap[0], chaps[i+1][0]), chap[1]) )
  chaps_.append( ((chaps[-1][0], total_length_ms), chaps[-1][1]) )
  index = 0
  child_ids = []
  for chap in chaps_:
    element_id = 'ch{:02}'.format(index).encode()
    times, title = chap
    new_chap = tag.chapters.set(element_id, times)
    new_chap.sub_frames.setTextFrame(b'TIT2', u'{}'.format(title))
    child_ids.append(element_id)
    index += 1
    #print(element_id, times)
  tag.table_of_contents.set(b"toc", child_ids=child_ids)
  list_chaps(tag)
  print('-> Done adding chapters')
  tag.save()

### tests
#print(to_millisecs('00:10:00.001'))
#print(to_hms('3000'))

def main():
  'Main'
  args = docopt(__doc__, version="mp3chaps 0.5")
  fname = args["<filename>"]
  tag = Tag()
  tag.parse(fname)
  audioFile = core.load(fname)
  total_length = audioFile.info.time_secs
  print('Name of file:', fname)
  print('Total length:', total_length)
  print('Num of chaps:', len(tag.chapters))
  if args["-l"]:
    list_chaps(tag)
  elif args["-i"]:
    add_chapters(tag, fname, total_length)
  elif args["-r"]:
    remove_chaps(tag)

if __name__ == '__main__':
  main()
