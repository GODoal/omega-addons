# -*- coding: utf-8 -*-
# Version 1.0.1 (25/02/2020)
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
import urllib
import urllib2
import re
import xbmcplugin
import xbmcgui
import xbmcaddon
import socket
import HTMLParser
import json
__settings__ = xbmcaddon.Addon(id='plugin.audio.skai')
__language__ = __settings__.getLocalizedString
fanart = os.path.join(__settings__.getAddonInfo('path'),'fanart.jpg')
BaseURL='http://www.skairadio.gr'

#Load user settings
timeout = int(__settings__.getSetting("socket_timeout"))
socket.setdefaulttimeout(timeout)


#Index Menu
def INDEX(url):
	addLink("Live Stream","http://liveradio.skai.gr/skaihd/skai/playlist.m3u8",os.path.join(__settings__.getAddonInfo('path'),'resources','images','latest.png'))
	for i in range(1,3):
	  req=urllib2.Request('http://www.skairadio.gr/shows?page='+str(i-1))
	  req.add_header('Accept', '*/*')
	  req.add_header('Connection', 'keep-alive')
	  req.add_header('Referer', 'http://www.skairadio.gr/shows?page='+str(i-1))
	  req.add_header('Origin', BaseURL)
	  req.add_header('Connection', 'keep-alive')
	  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	  response = urllib2.urlopen(req)
	  link=response.read()
	  response.close()
	  link=normalize_link(link)
	  block=re.compile('<section class="mb-5">(.+?)pagination').findall(link)
	  match=re.compile('<a href="(.+?)">(.+?)src="(.+?)" alt="(.+?)"(.+?)<span class="d-block">').findall(block[0])
	  for ep_url, buffer1, ep_image, ep_title, buffer2 in match:
	    addDir(ep_title,BaseURL+ep_url,1,ep_image.split('?')[0])
	addSetting(__language__(50001),'plugin://plugin.audio.skai',10,os.path.join(__settings__.getAddonInfo('path'),'resources','images','settings.png'))


# Specific Show List
def INDEX1(url,name):
	req=urllib2.Request(url)
	req.add_header('Accept', '*/*')
	req.add_header('Connection', 'keep-alive')
	req.add_header('Referer', url)
	req.add_header('Connection', 'keep-alive')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=normalize_link(link)
	bblock=re.compile('configuration(.+?)}],').findall(link)
	ep_image=bblock[0].split('\'')[1]
	ep_audio_url1=bblock[0].split('\'')[5][:-12]
	ep_audio_url2=bblock[0].split('\'')[5][-4:]
	#print 'SKAI RADIO ep_title='+name+' ep_image='+ep_image+' ep_audio_url1='+ep_audio_url1+' ep_audio_url2='+ep_audio_url2
	block=re.compile('episode_list_dropdown">(.+?)</select>').findall(link)
	armatch=block[0].split('</option>')
	for i in range(len(armatch)-1):
	  ep_date=armatch[i].split('>')
	  ep_date=ep_date[1].strip()
	  ep_url=ep_audio_url1+ep_date.split('/')[2]+ep_date.split('/')[1]+ep_date.split('/')[0]+ep_audio_url2
	  #print 'SKAI RADIO ep_title='+name.encode('utf-8')+' ep_date='+ep_date+' ep_url='+ep_url
	  addLink(name.encode('utf-8')+' - '+ep_date.split('/')[2]+'/'+ep_date.split('/')[1]+'/'+ep_date.split('/')[0],ep_url,ep_image.split('?')[0])
	if xbmcplugin.getSetting(int( sys.argv[ 1 ] ),"goback") == "true":
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
        liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "IsPlayable". "true" )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        icoimg = os.path.join(__settings__.getAddonInfo('path'),iconimage)
        if icoimg.count('http:') > 0:
                icoimg=iconimage
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=icoimg)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addSetting(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        icoimg = os.path.join(__settings__.getAddonInfo('path'),iconimage)
        if icoimg.count('http:') > 0:
                icoimg=iconimage
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=icoimg)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok 

def normalize_link(link):
        match=re.compile('charset=(.+?)"').findall(link)
        if not match:
                link=link.replace('\t','').replace('\r\n','').replace('\n','')
                return link
        elif match[0].upper() == "UTF-8":
                link=link.replace('\t','').replace('\r\n','').replace('\n','')
                return link
        else:
                link=link.replace('\t','').replace('\r\n','').replace('\n','').decode(match[0]).encode('utf-8')
                return link

def LoadSettings():
        __settings__.openSettings(sys.argv[ 0 ])
        timeout = int(__settings__.getSetting("socket_timeout"))
        socket.setdefaulttimeout(timeout)

def PageBack():
        xbmc.executebuiltin( "XBMC.Action(Back)" )

params=get_params()
url=None
name=None
mode=None
ytid=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        ytid=urllib.unquote_plus(params["ytid"])
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
elif mode==10:
	LoadSettings()
elif mode==11:
	PageBack()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
