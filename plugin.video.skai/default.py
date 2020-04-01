# -*- coding: utf-8 -*-
# Version 1.2.7 (01/04/2020)
# SKAI TV
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
__settings__ = xbmcaddon.Addon(id='plugin.video.skai')
__language__ = __settings__.getLocalizedString
fanart = os.path.join(__settings__.getAddonInfo('path'),'fanart.jpg')
BaseURL='http://www.skaitv.gr'

#Load user settings
timeout = int(__settings__.getSetting("socket_timeout"))
socket.setdefaulttimeout(timeout)


#Index Menu
def INDEX(url):
	req=urllib2.Request(BaseURL)
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=normalize_link(link)
	menu_block=re.compile('"menulist"(.+?)</div>').findall(link)
	cat_list=re.compile('<a href="(.+?)">(.+?)</a>').findall(menu_block[0])
	for urlext, name1 in cat_list:
	  # Filter out root page
	  if urlext.count('live') >0:
	    addDir(name1.strip(),BaseURL+urlext.strip(),1,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))
	  elif urlext.count('enimerosi') >0:
	    addDir(name1.strip(),BaseURL+urlext.strip(),2,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))
	  elif urlext.count('seires') >0:
	    addDir(name1.strip(),BaseURL+urlext.strip(),3,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))
	  elif urlext.count('psuchagogia') >0:
	    addDir(name1.strip(),BaseURL+urlext.strip(),3,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))
	  else:
	    if urlext.strip() not in ['/', '/programma']:
	      print 'ERROR :: SKAITV - Could not process URL:'+BaseURL+urlext.strip()
	addSetting(__language__(50001),'plugin://plugin.video.skai',10,os.path.join(__settings__.getAddonInfo('path'),'resources','images','settings.png'))


#LIVE
def INDEX1(url):
	req=urllib2.Request(url)
	req.add_header('Accept', '*/*')
	req.add_header('Connection', 'keep-alive')
	req.add_header('Referer', url)
	req.add_header('Origin', 'https://www.skaitv.gr')
	req.add_header('Connection', 'keep-alive')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	response = urllib2.urlopen(req)
	link=response.read()
	link=normalize_link(link)
	response.close()
	match=re.compile('var data = {(.+?)};').findall(link)
	main_json = json.loads('{'+match[0]+'}')
	if link.count('"livestream":"') > 0:
	  ep_name=main_json['now']['title'].encode('utf-8')
	  if str(main_json['now']['livestream'].encode('utf-8')).replace('\\','').count('watch?v=') > 0: 
	    sYTid=link.split('watch?v=')[1].split('"')[0]
	    addYTLink(ep_name,url,sYTid,30,os.path.join(__settings__.getAddonInfo('path'),'resources','images','latest.png'))
	  else:
	    addLink(ep_name,str(main_json['now']['livestream'].encode('utf-8')).replace('\\',''),os.path.join(__settings__.getAddonInfo('path'),'resources','images','latest.png'))
	else:
	  print 'ERROR :: SKAI TV - Could not process LIVE stream URL:'+url
	if xbmcplugin.getSetting(int( sys.argv[ 1 ] ),"goback") == "true":
	  addSetting('<< [ Back ]','plugin://plugin.video.skai/',11,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))


#CATEGORY LISTINGS
def INDEX2(url):
	req=urllib2.Request(url)
	req.add_header('Accept', '*/*')
	req.add_header('Connection', 'keep-alive')
	req.add_header('Referer', url)
	req.add_header('Origin', 'https://www.skaitv.gr')
	req.add_header('Connection', 'keep-alive')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=normalize_link(link)
	menu_block=re.compile('<h1 class=(.+?)<div class="catel">').findall(link)
	cat_list=re.compile('<img src="(.+?)" alt="(.+?)">(.+?)<a href="/episode(.+?)"><span').findall(menu_block[0])
	for epimage, name1, buffer1, urlpath in cat_list:
	  addDirSwitch(name1.strip(),BaseURL+'/episode'+urlpath.strip(),'main',20,epimage)
	  #print 'SKAI TV - addDir Name='+name1.strip()+' URL='+BaseURL+'/episode'+urlpath.strip()+' IMG='+epimage
	if xbmcplugin.getSetting(int( sys.argv[ 1 ] ),"goback") == "true":
	  addSetting('<< [ Back ]','plugin://plugin.video.skai/',11,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))


#SKAI Seires
def INDEX3(url):
	req=urllib2.Request(url)
	req.add_header('Accept', '*/*')
	req.add_header('Connection', 'keep-alive')
	req.add_header('Referer', url)
	req.add_header('Origin', 'https://www.skaitv.gr')
	req.add_header('Connection', 'keep-alive')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=normalize_link(link)
	menu_block=re.compile('<h1 class=(.+?)<div class="catel">').findall(link)
	cat_list=re.compile('<img src="(.+?)" alt="(.+?)">(.+?)<a href="/show(.+?)"(.+?)class="col-3 last-epi"').findall(menu_block[0])
	for epimage, name1, buffer1, urlpath, buffer2 in cat_list:
	  # For each url run another query and parse the URL to the latest episode
	  req=urllib2.Request(BaseURL+'/show'+urlpath.strip())
	  req.add_header('Accept', '*/*')
	  req.add_header('Referer', url)
	  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	  req.add_header('X-Requested-With', 'XMLHttpRequest')
	  response = urllib2.urlopen(req)
	  link=response.read()
	  response.close()
	  link=normalize_link(link)
	  match=re.compile('pro all active(.+?)<a href="(.+?)"(.+?)title_r">(.+?)</h3>(.+?)src="(.+?)"').findall(link)
	  if match:
	    ep_title=match[0][3].strip().replace('<br/>',' ').replace('\n','').replace('\r','')
	    ep_url=match[0][1]
	    ep_image=match[0][5]
	    #print 'SKAI TV - INDEX3 match = '+ep_url+' '+ep_title+' '+ep_image
	    addDirSwitch(ep_title,BaseURL+ep_url,'main',20,ep_image)
	if xbmcplugin.getSetting(int( sys.argv[ 1 ] ),"goback") == "true":
	  addSetting('<< [ Back ]','plugin://plugin.video.skai/',11,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))


def VIDEOLINKS(url,name,switch):
	req=urllib2.Request(url)
	req.add_header('Accept', '*/*')
	req.add_header('Referer', url)
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	req.add_header('X-Requested-With', 'XMLHttpRequest')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('var data = {(.+?)};').findall(link)
	main_json = json.loads('{'+match[0]+'}')
	for x in range(len(main_json['episode'])):
	  if 'media_item_title' in main_json['episode'][x]:
	    #If the title contains the air date then display it as is
	    ep_title=main_json['episode'][x]['media_item_title'].encode('utf-8')
	    ep_date=main_json['episode'][x]['start'].encode('utf-8').split(' ')[0].replace('"','')
	    ep_date1=ep_date.replace('-','/')
	    ep_date2=ep_date.split('-')[2]+'/'+ep_date.split('-')[1]+'/'+ep_date.split('-')[0]
	    if ep_title.count(ep_date1) > 0 or ep_title.count(ep_date2) > 0:
	      ep_name=ep_title
	    else:
	      ep_name=main_json['episode'][x]['media_item_title'].encode('utf-8')+' - '+ep_date2
	    addLink(ep_name,str('http://videostream.skai.gr/'+main_json['episode'][x]['media_item_file'].encode('utf-8')).replace('\\','')+'.m3u8','http:'+main_json['episode'][x]['img'].encode('utf-8'))
	if switch == 'main':
	  matchrest=re.compile('btncustom(.+?)">(.+?)</a>').findall(link)
	  if matchrest[0][1]:
	    addDir(matchrest[0][1],url,21,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))
	if xbmcplugin.getSetting(int( sys.argv[ 1 ] ),"goback") == "true":
	  addSetting('<< [ Back ]','plugin://plugin.video.skai/',11,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))


def VIDEOINDEX(url,name):
	req=urllib2.Request(url)
	req.add_header('Accept', '*/*')
	req.add_header('Referer', url)
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) XBMC Multimedia System')
	req.add_header('X-Requested-With', 'XMLHttpRequest')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('var data = {(.+?)};').findall(link)
	main_json = json.loads('{'+match[0]+'}')
	for x in range(len(main_json['episodes'])):
	  if 'link' in main_json['episodes'][x]:
	    ep_title=main_json['episodes'][x]['title'].encode('utf-8')
	    ep_date=main_json['episodes'][x]['start'].encode('utf-8').split(' ')[0].replace('"','')
	    ep_date1=ep_date.replace('-','/')
	    ep_date2=ep_date.split('-')[2]+'/'+ep_date.split('-')[1]+'/'+ep_date.split('-')[0]
	    if ep_title.count(ep_date1) > 0 or ep_title.count(ep_date2) > 0:
	      addDirSwitch(ep_title,str(BaseURL+main_json['episodes'][x]['link'].encode('utf-8')).replace('\\',''),'rest',20,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))
	    else:
	      addDirSwitch(ep_title+' - '+ep_date2,str(BaseURL+main_json['episodes'][x]['link'].encode('utf-8')).replace('\\',''),'rest',20,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))
	if xbmcplugin.getSetting(int( sys.argv[ 1 ] ),"goback") == "true":
	  addSetting('<< [ Back ]','plugin://plugin.video.skai/',11,os.path.join(__settings__.getAddonInfo('path'),'resources','images','defFolder.png'))


def VIDEOLINKSYT(ytid):
        xbmc_url = 'plugin://plugin.video.youtube/play/?video_id='+str(ytid)
        li = xbmcgui.ListItem("testing",path=xbmc_url)
        li.setProperty("IsPlayable","true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)

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
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addYTLink(name,url,ytid,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&ytid="+str(ytid)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        icoimg = os.path.join(__settings__.getAddonInfo('path'),iconimage)
        if icoimg.count('http:') > 0:
                icoimg=iconimage
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable","true")
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        icoimg = os.path.join(__settings__.getAddonInfo('path'),iconimage)
        if icoimg.count('http:') > 0:
                icoimg=iconimage
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=icoimg)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirSwitch(name,url,switch,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&switch="+urllib.quote_plus(switch)
        ok=True
        icoimg = os.path.join(__settings__.getAddonInfo('path'),iconimage)
        if icoimg.count('http:') > 0:
                icoimg=iconimage
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=icoimg)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
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
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
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
switch=None

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
try:
        switch=urllib.unquote_plus(params["switch"])
except:
        pass

#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "YTid: "+str(ytid)
#print "Switch: "+str(switch)

if mode==None or url==None or len(url)<1:
        INDEX(url)
elif mode==1:
	INDEX1(url)
elif mode==2:
	INDEX2(url)
elif mode==3:
	INDEX3(url)
elif mode==10:
	LoadSettings()
elif mode==11:
	PageBack()
elif mode==20:
        VIDEOLINKS(url,name,switch)
elif mode==21:
        VIDEOINDEX(url,name)
elif mode==30:
        VIDEOLINKSYT(ytid)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
