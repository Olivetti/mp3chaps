# mp3chaps v0.5
**mp3chaps** is a commandline utility for adding chapter marks to mp3 files similar to `mp4chaps` utility
many podcast apps on Android and iOS support chapter markers in both mp4 (aac) and mp3 files
this utilizes the excellent `eyeD3 <https://github.com/nicfit/eyeD3>` tagging module to read
and write chapter frames and title subframes

forked from [David Karimeddini's](https://github.com/dskrad/mp3chaps)

### Requirements
- [Python](https://python.org)

### Installation
1. [Download & unpack](https://github.com/Olivetti/mp3chaps/releases/latest/download/mp3chaps.tar.gz)
2. Execute           `python setup.py`

-3. Original version `pip install mp3chaps`

### Usage
- mp3chaps[.py] -h

Assuming you have a file named `file.mp3`, mp3chaps looks for a chapter marks file called
`file.chp` in the same directory:

    00:00:00 Introduction
    00:02:00 Chapter Title
    00:42:24 Chapter Title

    or with milliseconds

    00:00:00.000 Introduction
    00:02:00.000 Chapter Title
    00:42:24.123 Chapter Title

### Add chapter marks
Add (import) chapter marks from text file

`mp3chaps -i file.mp3`

Unexpected results may occur if chapters already exist. For best results remove chapters first with -r.
If you run into errors, try using ASCII. There have been some issues with Unicode.

### List chapters
`mp3chaps -l file.mp3`

### Remove chapters
`mp3chaps -r file.mp3`

### Under the hood
first we will set chapters with element_id and times tuple (start, end)
times are in milliseconds
```bash
tag.chapters.set("ch1", (0,10000))
tag.chapters.set("ch2", (10000, 360000))
tag.chapters.set("ch3", (360000, 1800000))
```

now we will set titles for each chapter
```bash
chap1 = tag.chapters.get("ch1")
chap1.sub_frames.setTextFrame("TIT2", u"Here is my first chapter title")
chap2 = tag.chapters.get("ch2")
chap2.sub_frames.setTextFrame("TIT2", u"Here is my second chapter title")
chap3 = tag.chapters.get("ch3")
chap3.sub_frames.setTextFrame("TIT2", u"Here is my third chapter title")
```

don't forget to add chapters to the toc
```bash
tag.table_of_contents.set("toc", child_ids=["ch1", "ch2", "ch3"])
```

last but not least, save our tag
```bash
tag.save()
```

## Contributing
Issues can be made in [**GitHub** project](https://github.com/Olivetti/mp3chaps)

## Contact
[Mastodon](https://mastodon.social/@Olivetti)
