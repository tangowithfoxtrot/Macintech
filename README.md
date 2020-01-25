# Macintech Plus
A ｖａｐｏｒｗａｖｅ generator hacked together at UncommonHacks 2016. Downloads audio from a video on youtube and turns it into vaporwave, and also gives it a vaporwave name. Uses python 2.7 with a bunch of dependencies. Now you too can slow some music down and call yourself an artist!

# Installation
This was tested on Ubuntu 19. You'll need these dependencies:

```
sudo apt install python-pip ffmpeg libavl1 sox
sudo pip install beautifulsoup4 youtube-dl
```

# Usage
From the root folder of this project:

```
python src/VaporMain.py youtube_query_to_vaporize
```
