# -*- coding: utf-8 -*-
#
#  RealTek Weather Info
#
#  Coded by TBX for Kraven Skins (c) 2016
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative
#  Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.
#

from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Converter.Converter import Converter
from Components.Language import language
from Components.Element import cached
from Components.config import config
from xml.etree.cElementTree import fromstring
from enigma import eTimer
from datetime import datetime
import os, gettext, requests

lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SevenHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/SevenHD/locale/"))

def _(txt):
	t = gettext.dgettext("SevenHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

URL = 'http://realtek.accu-weather.com/widget/realtek/weather-data.asp?%s' % str(config.plugins.SevenHD.weather_lat_lon.value)
WEATHER_DATA = None

class SevenHDWeather_realtek(Converter, object):
	def __init__(self, type):
                Converter.__init__(self, type)
                type = type.split(',')                
                self.day_value = type[0]
                self.what = type[1]
                self.data = {}
                self.timer = eTimer()
                self.timer.callback.append(self.reset)
		self.timer.callback.append(self.get_Data)
		self.get_Data()

	@cached
	def getText(self):

	    day = self.day_value.split('_')[1]
            if self.what == 'DayTemp':
               self.info = self.getDayTemp()	
            elif self.what == 'FeelTemp':
               self.info = self.getFeelTemp()
            elif self.what == 'MinTemp':
               self.info = self.getMinTemp(int(day))
            elif self.what == 'MaxTemp':
               self.info = self.getMaxTemp(int(day))
            elif self.what == 'Description':
               self.info = self.getWeatherDes(int(day)) 
            elif self.what == 'MeteoIcon':
               self.info = self.getWeatherIcon(int(day))
            elif self.what == 'MeteoFont':
               self.info = self.getMeteoFont(int(day))
            elif self.what == 'WetterDate':
               self.info = self.getWeatherDate(int(day))
            elif self.what == 'Wind':
               self.info = self.getCompWind()	 
            elif self.what == 'Humidity':
               self.info = self.getHumidity()
            elif self.what == 'RainMM':
               self.info = self.getRainMM(int(day))
            elif self.what == 'City':
               self.info = str(config.plugins.SevenHD.weather_cityname.getValue())

            return str(self.info)
	text = property(getText)
        
        def reset(self):
	    global WEATHER_DATA
            WEATHER_DATA = None
        
        def get_Data(self):
            global WEATHER_DATA
            if WEATHER_DATA is None:
               
               self.data = {}
               index = 0

               res = requests.request('get', URL)
               root = fromstring(res.text.replace('xmlns="http://www.accuweather.com"',''))

               for child in root.findall('currentconditions'):
                   self.data['Day_%s' % str(index)] = {}
                   self.data['Day_%s' % str(index)]['temp'] = child.find('temperature').text
                   self.data['Day_%s' % str(index)]['skytextday'] = child.find('weathertext').text
                   self.data['Day_%s' % str(index)]['skycodeday'] = child.find('weathericon').text 
                   self.data['Day_%s' % str(index)]['humidity'] = child.find('humidity').text
                   self.data['Day_%s' % str(index)]['winddisplay'] = child.find('winddirection').text
                   self.data['Day_%s' % str(index)]['windspeed'] = child.find('windspeed').text
                   self.data['Day_%s' % str(index)]['feelslike'] = child.find('realfeel').text

               for child in root.findall('forecast'):
                   for item in child.findall('day'):                        
                       for entrie in item.findall('daytime'):        
                           index += 1
                           self.data['Day_%s' % str(index)] = {}
                           self.data['Day_%s' % str(index)]['day'] = item.find('obsdate').text
                           self.data['Day_%s' % str(index)]['low'] = entrie.find('hightemperature').text
                           self.data['Day_%s' % str(index)]['high'] = entrie.find('lowtemperature').text
                           self.data['Day_%s' % str(index)]['skycodeday'] = entrie.find('weathericon').text                                
                           self.data['Day_%s' % str(index)]['skytextday'] = entrie.find('txtshort').text  
                           self.data['Day_%s' % str(index)]['precip'] = entrie.find('rainamount').text
                           
               WEATHER_DATA = self.data
               timeout = int(config.plugins.SevenHD.refreshInterval.value) * 1000.0 * 60.0
               self.timer.start(int(timeout), True)
               
            else:
               self.data = WEATHER_DATA
               
        def getMinTemp(self, day):
            try:
               temp = self.data['Day_%s' % str(day)]['low']
               if temp == '':
                  temp = 'N/A'
               return str(temp) + '°C'
            except:
               return 'N/A'
            
        def getMaxTemp(self, day):
            try:
               temp = self.data['Day_%s' % str(day)]['high']
               if temp == '':
                  temp = 'N/A'
               return str(temp) + '°C'
            except:
               return 'N/A'
            
        def getFeelTemp(self):
            try:
               temp = self.data['Day_0']['temp']
               feels = self.data['Day_0']['feelslike']
               return str(temp) + '°C' + _(", feels ") + str(feels) + '°C'
            except:
               return 'N/A'
            
        def getDayTemp(self):
            try:
               temp = self.data['Day_0']['temp']
               return str(temp) + '°C'
            except:
               return 'N/A'
            
        def getWeatherDes(self, day):
            try:
               weather = self.data['Day_%s' % str(day)]['skytextday']
               return str(weather)
            except:
               return 'N/A'
            
        def getWeatherIcon(self, day):
            try:
               weathericon = self.data['Day_%s' % str(day)]['skycodeday']
               return str(weathericon)
            except:
               return 'N/A'
            
        def getCompWind(self):
            try:
               speed = self.data['Day_0']['windspeed']
               wind = self.getWind()
               return str(speed) + _(" km/h") + _(" from ") + str(wind)
            except:
               return 'N/A'
            
        def getWeatherDate(self, day):
            try:
               weather_date = self.data['Day_%s' % str(day)]['day']
               date_struc = datetime.strptime(weather_date,"%m/%d/%Y")
               weather_dayname = date_struc.strftime('%a')
               return str(weather_dayname)
            except:
               return 'N/A'
            
        def getHumidity(self):
            try:
               humi = self.data['Day_0']['humidity']
               return str(humi.replace('%','')) + _('% humidity')
            except:
               return 'N/A'
        
        def getRainMM(self, day):
            try:
               rainp = self.data['Day_%s' % str(day)]['precip']
               return str(float(rain)) + ' %'
            except:
               return 'N/A'    
        
        def getMeteoFont(self, day):
            try:
               font = self.data['Day_%s' % str(day)]['skycodeday']
               font_icon = '0x' + str(20 + int(font))
               weather_font_icon = unichr(int(font_icon, 16)).encode('utf-8')
               return str(weather_font_icon)
            except:
               return 'N/A'
            
        def getWind(self):
            direct = int(float(self.data['Day_0']['winddisplay']))
            if direct >= 0 and direct <= 20:
               wdirect = _('N')
            elif direct >= 21 and direct <= 35:
               wdirect = _('N-NE')
            elif direct >= 36 and direct <= 55:
               wdirect = _('NE')
            elif direct >= 56 and direct <= 70:
               wdirect = _('E-NE')
            elif direct >= 71 and direct <= 110:
               wdirect = _('E')
            elif direct >= 111 and direct <= 125:
               wdirect = _('E-SE')
            elif direct >= 126 and direct <= 145:
               wdirect = _('SE')
            elif direct >= 146 and direct <= 160:
               wdirect = _('S-SE')
            elif direct >= 161 and direct <= 200:
               wdirect = _('S')
            elif direct >= 201 and direct <= 215:
               wdirect = _('S-SW')
            elif direct >= 216 and direct <= 235:
               wdirect = _('SW')
            elif direct >= 236 and direct <= 250:
               wdirect = _('W-SW')
            elif direct >= 251 and direct <= 290:
               wdirect = _('W')
            elif direct >= 291 and direct <= 305:
               wdirect = _('W-NW')
            elif direct >= 306 and direct <= 325:
               wdirect = _('NW')
            elif direct >= 326 and direct <= 340:
               wdirect = _('N-NW')
            elif direct >= 341 and direct <= 360:
               wdirect = _('N')
            else:
               wdirect = "N/A"
            return wdirect