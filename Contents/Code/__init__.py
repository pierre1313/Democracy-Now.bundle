from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

DN_PREFIX    = '/video/democracynow'
DN_RSS_FEED  = 'http://www.democracynow.org/podcast-video.xml'
DN_NAMESPACE = {'i':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
CACHE_INTERVAL = 3600

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(DN_PREFIX, Videos, 'Democracy Now!', 'icon-default.png', 'art-default.jpg')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'Democracy Now!'
  MediaContainer.content = 'Items'
  MediaContainer.art = R('art-default.jpg')
  
####################################################################################################
def UpdateCache():
  HTTP.Request(DN_RSS_FEED)

####################################################################################################
def Videos():
  dir = MediaContainer()
  for v in XML.ElementFromURL(DN_RSS_FEED, cacheTime=CACHE_INTERVAL).xpath("//item"):
    title = v.find('title').text
    description = v.find('description').text
    date = Datetime.ParseDate(v.find('pubDate').text).strftime('%a %b %d, %Y')
    url = v.find('enclosure').get('url')
    duration = v.xpath('i:duration', namespaces=DN_NAMESPACE)[0].text.split(':')
    duration = (int(duration[0])*60 + int(duration[1])) * 1000
    dir.Append(VideoItem(url, date, subtitle='Democracy Now!', duration=duration, summary=description, thumb=R('icon-default.png')))
  return dir
