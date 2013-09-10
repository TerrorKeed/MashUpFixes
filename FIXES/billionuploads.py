'''
Billionuploads urlresolver plugin
Copyright (C) 2013 jas0npc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import urllib,urllib2,time
import os
from urlresolver import common
from t0mm0.common.net import Net 
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
net = Net()

captcha_img = os.path.join(common.addon_path, 'resources', 'billionuploads_captcha.png')
logo = os.path.join(common.addon_path, 'resources', 'images', 'redx.png')

class billionuploads(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "billionuploads"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        # UPDATED BY THE-ONE @ XBMCHUB - 08-27-2013
        try:
            url = self.get_url(host, media_id)
                
                #########
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving BillionUploads Link...')       
            dialog.update(0)
            
            common.addon.log( self.name + ' - Requesting GET URL: %s' % url )
            cj = cookielib.CookieJar()
            normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            normal.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
            
            ########################################################
            ######## CLOUD FLARE STUFF
            #######################################################
            class NoRedirection(urllib2.HTTPErrorProcessor):
                # Stop Urllib2 from bypassing the 503 page.    
                def http_response(self, request, response):
                    code, msg, hdrs = response.code, response.msg, response.info()

                    return response
                https_response = http_response            
            
            opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
            response = opener.open(url).read()
                
            html = None
            jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
            if jschl:
                jschl = jschl[0]    
            
                maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')

                domain_url = re.compile('(https?://.+?/)').findall(url)[0]
                domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
                                
                final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
                
                html = normal.open(url).read()
            else:
                html = response
            ################################################################################
            #Check page for any error msgs
            if re.search('This server is in maintenance mode', html, re.I):
                print '***** BillionUploads - Site reported maintenance mode'
                xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,BillionUploads in maintenance,2000)")                                
                return False
                
            #Check for File Not Found
            if re.search('File Not Found', html, re.I):
                print '***** BillionUploads - File Not Found'
                xbmc.executebuiltin("XBMC.Notification(File Not Found,BillionUploads,2000)")
                return False                                
            
            #NEW BILLIONUPLOADS
            #postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            #video_src_url = 'http://new.billionuploads.com/embed-' + postid + '.html'
            #print video_src_url
            #html = normal.open(video_src_url).read()
            
            #dialog.close()
            
            # SOLVEMEDIA CAPTCHA
            #try:
            #    captcha_dir = os.path.join( datapath, 'resources')
            #    captcha_img = os.path.join(captcha_dir, 'billion_uploads_resolver.png')
            #    if not os.path.exists(captcha_dir):
            #        os.makedirs(captcha_dir)
            #    os.remove(captcha_img)
            #except: 
            #    pass
                
            #net1 = net()
            #noscript=re.compile('<iframe src="(.+?)"').findall(html)[0]
            #check = net1.http_GET(noscript).content
            #hugekey=re.compile('id="adcopy_challenge" value="(.+?)">').findall(check)[0]           
            #captcha_headers= {'User-Agent':'Mozilla/6.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4',
            #     'Host':'api.solvemedia.com','Referer':video_src_url,'Accept':'image/png,image/*;q=0.8,*/*;q=0.5'}
            #open(captcha_img, 'wb').write( net1.http_GET("http://api.solvemedia.com%s"%re.compile('<img src="(.+?)"').findall(check)[0]).content)
            
            #img = xbmcgui.ControlImage(550,15,240,100,captcha_img)
            #wdlg = xbmcgui.WindowDialog()
            #wdlg.addControl(img)
            #wdlg.show()
        
            #Prompt keyboard for user input
            #kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            #kb.doModal()
            #capcode = kb.getText()
        
            #Check input                             
            #if (kb.isConfirmed()):
            #    userInput = kb.getText()
            #    if userInput != '':
            #        capcode = kb.getText()
            #    elif userInput == '':
            #        Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
            #        return False
            #else:
            #    return False 
            #wdlg.close()
                
            #print 'Mash Up BillionUploads - Requesting POST URL: %s' % video_src_url
            #data={'op':'video_embed','file_code':postid, 'adcopy_response':capcode,'adcopy_challenge':hugekey}
            #html = normal.open(video_src_url, urllib.urlencode(data)).read()
            
            ####
            #OLD BILLION UPLOADS
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
            for name, value in r:
                data[name] = value
                
            captchaimg = re.search('<img src="((?:http://|www\.)?BillionUploads.com/captchas/.+?)"', html)
    
            if captchaimg:
                dialog.close()
                img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()
        
                kb = xbmc.Keyboard('', 'Type the letters in the image', False)
                kb.doModal()
                capcode = kb.getText()
        
                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '':
                        capcode = kb.getText()
                    elif userInput == '':
                        common.addon.show_error_dialog("You must enter the text from the image to access video")
                        return False
                else:
                    return False
                wdlg.close()
                dialog.close() 
                dialog.create('Resolving', 'Resolving Mash Up BillionUploads Link...')
                dialog.update(50)
                data.update({'code':capcode})

            else:  
                dialog.update(50)
            
            data.update({'submit_btn':''})
            data.update({'geekref':'yeahman'})
            
            print 'Mash Up BillionUploads - Requesting POST URL: %s' % url
            html = normal.open(url, urllib.urlencode(data)).read()
            
            dialog.update(100)
            
            def custom_range(start, end, step):
                while start <= end:
                    yield start
                    start += step

            def checkwmv(e):
                s = ""
                
                # Create an array containing A-Z,a-z,0-9,+,/
                i=[]
                u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
                for z in range(0, len(u)):
                    for n in range(u[z][0],u[z][1]):
                        i.append(chr(n))
                #print i

                # Create a dict with A=0, B=1, ...
                t = {}
                for n in range(0, 64):
                    t[i[n]]=n
                #print t

                for n in custom_range(0, len(e), 72):

                    a=0
                    h=e[n:n+72]
                    c=0

                    #print h
                    for l in range(0, len(h)):            
                        
                        f = t.get(h[l], 'undefined')
                        if f == 'undefined':
                            continue
                            
                        a= (a<<6) + f
                        c = c + 6

                        while c >= 8:
                            c = c - 8
                            s = s + chr( (a >> c) % 256 )

                return s

        
            dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)[0]
            dl = dll.split('GvaZu')[1]
            dl = checkwmv(dl);
            dl = checkwmv(dl);
            print 'Mash Up BillionUploads Link Found: %s' % dl

            return dl

        except Exception, e:
            common.addon.log_error(self.name + ' - Exception: %s' % e)
            return self.unresolvable(code=0, msg='Exception: %s' % e)
        finally:
            dialog.close()

        

    def get_url(self, host, media_id):
        return 'http://www.BillionUploads.com/%s' % media_id

    def get_host_and_id(self, url):
        r = re.search('//(.+?)/([0-9a-zA-Z]+)',url)
        if r:
            return r.groups()
        else:
            return False
        return ('host', 'media_id')

    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false': return False
        return (re.match('http://(www.)?[bB]illion[uU]ploads.com/' +
                         '[0-9A-Za-z]+', url) or
                         '[bB]illion[uU]ploads' in host)
