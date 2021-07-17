import urllib
import urllib2
from bs4 import BeautifulSoup
import youtube_dl
import os
import re
import subprocess
from Name import Namer

MAX_LEN = 60 * 10

class YTDownloader:

	# Returns the first 64 or so links from a query, depending on how youtube feels that day.
	@staticmethod
	def fetch(textToSearch):
		# All of this is stack overflow magic, lel
		query = urllib.quote(textToSearch)
		url = "https://www.youtube.com/results?search_query=" + query
		response = urllib2.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html, "html.parser")
		vids = []
		for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		    vids.append('https://www.youtube.com' + vid['href'])
		return vids

	# Given a link, downloads the video as the video name without punctuation. Returns true if it was downloaded.
	@staticmethod
	def download(link):
		# Sometimes a youtube query will return links or user pages. Bad youtube! Don't download this.
		if('user' in link or 'list' in link ):
			return False
		try:
			# Get the video info, and retitle it to only include alphanumeric.
			r = youtube_dl.YoutubeDL().extract_info(link,download = False)
			title = re.sub(r'([^\s\w]|_)+', '', r['title'])
			savename = ("download/" + title +".%(ext)s")
			
			# If the video is super long, don't download it.
			if (r['duration'] > MAX_LEN):	
				return False	
			# This will download the video for us.
			subprocess.call(["youtube-dl", "--extract-audio", "--audio-format", "wav" ,"-o", savename,link])
			return True
		except youtube_dl.utils.DownloadError:
			return False
		except ExtractorError:
			return False

	# Downloads 'count' videos from a list of links.
	@staticmethod
	def dl_some(count,links):
		for link in links:
			if(count == 0):
				return
			if(YTDownloader.download(link)):
				count -= 1

	# Vaporwaveises all of the names in the "downloads" folder.
	@staticmethod
	def convert_names(query):
		for f in os.listdir("download/"):
			new_name = f.split(".")[0].lower()
			for s in query.split():
				new_name = new_name.replace(s,'')
			new_name = Namer.vaporname(new_name).replace('(','').replace(')','')
			os.rename("download/"+f,"download/"+new_name)

	# Given a query, downloads the top youtube audio for that query
	@staticmethod
	def download_wav_to_samp2(query):
		# Downloads a single youtube video from the query.
		YTDownloader.dl_some(1,YTDownloader.fetch(query))
		# Vaporizes the names.
		YTDownloader.convert_names(query)
