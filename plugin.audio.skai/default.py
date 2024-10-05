# -*- coding: utf-8 -*-
# Version 1.1.1 (05/10/2024)
# SKAI RADIO
# Greek News Channel XBMC addon
# By GODoal
# https://github.com/GODoal/omega-addons
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################
import os
import sys
import xbmc
import urllib.request
import re
import xbmcplugin
import xbmcgui
import xbmcaddon
import socket
from html.parser import HTMLParser
import json
__settings__ = xbmcaddon.Addon(id='plugin.audio.skai')
fanart = os.path.join(__settings__.getAddonInfo('path'),'fanart.jpg')
BaseURL='http://www.skairadio.gr'

#Load user settings
socket.setdefaulttimeout(15)

#Index Menu
def INDEX(url):
	addLink("Live Stream","http://skai.live24.gr/skai1003",os.path.join(__settings__.getAddonInfo('path'),'resources','images','latest.png'))
	for i in range(1,3):
	  req=urllib.request.Request('http://www.skairadio.gr/shows?page='+str(i-1))
	  req.add_header('Accept', '*/*')
	  req.add_header('Connection', 'keep-alive')
	  req.add_header('Referer', 'http://www.skairadio.gr/shows?page='+str(i-1))
	  req.add_header('Origin', BaseURL)
	  req.add_header('Connection', 'keep-alive')
	  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	  response = urllib.request.urlopen(req)
	  link=response.read()
	  link=normalize_link(link)
	  response.close()
	  block=re.compile('<section class="mb-5">(.+?)pagination').findall(link)
	  match=re.compile('<a href="(.+?)">(.+?)src="(.+?)" alt="(.+?)" typeof="(.+?)</h3>(.+?)<span class\="d-block">(.+?)</span>').findall(block[0])
	  for ep_url, buffer1, ep_image, ep_title, buffer2, buffer3, buffer4 in match:
	    addDir(ep_title.replace(' &#039;','\''),BaseURL+ep_url,1,ep_image.split('?')[0])

# Show List
def INDEX1(url,name):
	req=urllib.request.Request(url)
	req.add_header('Accept', '*/*')
	req.add_header('Connection', 'keep-alive')
	req.add_header('Referer', url)
	req.add_header('Connection', 'keep-alive')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	response = urllib.request.urlopen(req)
	link=response.read()
	response.close()
	link=normalize_link(link)
	block=re.compile('="selected">(.+?)</select>').findall(link)
	episodes=re.compile('data-url = "(.+?)">(.+?)</option>').findall(block[0])
	for ep_url, ep_date in episodes:
	  addDir(name+' - '+ep_date.strip(),BaseURL+ep_url,2,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))
	addSetting('<< [ Back ]','plugin://plugin.audio.skai/',11,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))

# Non-Lazy Show List
def INDEX2(url,name):
	req=urllib.request.Request(url)
	req.add_header('Accept', '*/*')
	req.add_header('Connection', 'keep-alive')
	req.add_header('Referer', url)
	req.add_header('Connection', 'keep-alive')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	response = urllib.request.urlopen(req)
	link=response.read()
	response.close()
	link=normalize_link(link)
	block=re.compile('configuration(.+?)}],').findall(link)
	ep_image=block[0].split('\'')[1]
	ep_audio=block[0].split('\'')[5].strip()
	addLink(name,ep_audio,ep_image.split('?')[0])
	addSetting('<< [ Back ]','plugin://plugin.audio.skai/',11,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
        return param

def addLink(name,url,iconimage):
        ok=True
        icoimg = os.path.join(__settings__.getAddonInfo('path'),iconimage)
        if icoimg.count('http:') > 0:
                icoimg=iconimage
        liz = xbmcgui.ListItem(name)
        liz.setArt({'icon':icoimg, 'fanart': fanart})
        vinfo = liz.getVideoInfoTag()
        vinfo.setTitle(name)
        vinfo.setMediaType('video')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)
        ok=True
        icoimg = os.path.join(__settings__.getAddonInfo('path'),iconimage)
        if icoimg.count('http:') > 0:
                icoimg=iconimage
        liz = xbmcgui.ListItem(name)
        liz.setArt({'icon':icoimg, 'fanart': fanart})
        vinfo = liz.getVideoInfoTag()
        vinfo.setTitle(name)
        vinfo.setPath(u)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addSetting(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)
        ok=True
        icoimg = os.path.join(__settings__.getAddonInfo('path'),iconimage)
        if icoimg.count('http:') > 0:
                icoimg=iconimage
        liz = xbmcgui.ListItem(name)
        liz.setArt({'icon':icoimg, 'fanart': fanart})
        vinfo = liz.getVideoInfoTag()
        vinfo.setTitle(name)
        vinfo.setMediaType('video')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def normalize_link(link):
        decoded = link.decode('utf-8')
        match=re.compile('charset=(.+?)"').findall(decoded)
        if not match:
                link=link.replace('\t','').replace('\r\n','').replace('\n','')
                return link
        elif match[0].upper() == "UTF-8":
                link=decoded.replace('\t','').replace('\r\n','').replace('\n','')
                return link
        else:
                link=decoded.replace('\t','').replace('\r\n','').replace('\n','').encode('utf-8')
                return link.decode('UTF-8')

def PageBack():
        xbmc.executebuiltin( "Action(Back)" )

params=get_params()
url=None
name=None
mode=None
ytid=None

try:
        url=urllib.parse.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.parse.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        ytid=urllib.parse.unquote_plus(params["ytid"])
except:
        pass


#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "YTid: "+str(ytid)

if mode==None or url==None or len(url)<1:
    INDEX(url)
elif mode==1:
	INDEX1(url,name)
elif mode==2:
	INDEX2(url,name)
elif mode==10:
	LoadSettings()
elif mode==11:
	PageBack()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
