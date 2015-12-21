# -*- coding: UTF-8 -*-
#######################################################################
#
# SevenHD by Team Kraven
# 
# Thankfully inspired by:
# MyMetrix
# Coded by iMaxxx (c) 2013
#
# This plugin is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#######################################################################
from GlobalImport import *
#######################################################################
lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SevenHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/SevenHD/locale/"))

def _(txt):
	t = gettext.dgettext("SevenHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block
#######################################################################
class ChannelSettings(ConfigListScreen, Screen):
    skin = """
                  <screen name="SevenHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <eLabel font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Defaults" transparent="1" />
                         <widget name="blue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <eLabel position="70,12" size="708,46" text="SevenHD" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                         <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
                         <widget name="description" position="891,490" size="372,200" font="Regular; 26" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
                         <widget backgroundColor="#00000000" font="Regular2; 34" foregroundColor="#00ffffff" position="70,12" render="Label" size="708,46" source="Title" transparent="1" halign="center" valign="center" noWrap="1" />
                         <eLabel backgroundColor="#00000000" position="6,6" size="842,708" transparent="0" zPosition="-9" foregroundColor="#00ffffff" />
                         <eLabel backgroundColor="#00ffffff" position="6,6" size="842,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="6,714" size="844,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="6,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="848,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="18,64" size="816,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="18,656" size="816,2" zPosition="2" />
                         <widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
                                 <convert type="ClockToText">Default</convert>
                         </widget>
                         <eLabel backgroundColor="#00000000" position="878,6" size="396,708" transparent="0" zPosition="-9" />
                         <eLabel backgroundColor="#00ffffff" position="878,6" size="396,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="878,714" size="398,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="878,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="1274,6" size="2,708" zPosition="2" />
                         <widget source="session.CurrentService" render="Label" position="891,88" size="372,46" font="Regular2;35" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
                                 <convert type="SevenHDUpdate">Version</convert>
                         </widget>
                         <widget source="session.CurrentService" render="Label" position="891,134" size="372,28" font="Regular;26" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00B27708">
                                 <convert type="SevenHDUpdate">Update</convert>
                         </widget>
                         <eLabel position="891,274" size="372,2" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="891,481" size="372,2" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="891,274" size="2,208" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="1261,274" size="2,208" backgroundColor="#00ffffff" zPosition="5" />
                  </screen>
               """

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        self.session = session
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self["helperimage"] = Pixmap()
        self["blue"] = Label()
        self["description"] = Label()
        
        if config.plugins.SevenHD.grabdebug.value:
           self["blue"].setText('Screenshot')
           
        ConfigListScreen.__init__(
            self,
            self.getMenuItemList(),
            session = session,
            on_change = self.__selectionChanged
        )

        self["actions"] = ActionMap(
        [
            "OkCancelActions",
            "DirectionActions",
            "InputActions",
            "ColorActions"
        ],
        {
            "left": self.keyLeft,
            "down": self.keyDown,
            "up": self.keyUp,
            "right": self.keyRight,
            "red": self.exit,
            "yellow": self.defaults,
            "green": self.save,
            "blue": self.grab_png,
            "cancel": self.exit
        }, -1)

        self.onLayoutFinish.append(self.UpdatePicture)

    def getMenuItemList(self):
        list = []
        list.append(getConfigListEntry(_('___________________________channelselection___________________________________'), ))
        list.append(getConfigListEntry(_("style"),                        config.plugins.SevenHD.ChannelSelectionStyle,      'W\xc3\xa4hle den Stil der Kanalliste',                                                              '1',        ''))
        ChannelSelectionStyle = config.plugins.SevenHD.ChannelSelectionStyle.value
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3'):
           pass
        else:
           list.append(getConfigListEntry(_("prime time"),                config.plugins.SevenHD.PrimeTimeTime,              'Zeigt dir in der Kanalliste die PrimeTime an.',                                                '4',       'primetimetime'))
        list.append(getConfigListEntry(_('_____________________________background________________________________________'), ))
        list.append(getConfigListEntry(_("color left"),                   config.plugins.SevenHD.ChannelBack1,               'Stellt den Hintergrund der linken Spalte ein.',                                                '4',       'colorleftcs'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("color middle"),              config.plugins.SevenHD.ChannelBack3,               'Stellt den Hinergrund der mittleren Spalte ein',                                               '4',       'colormiddlecs'))
        list.append(getConfigListEntry(_("color right"),                  config.plugins.SevenHD.ChannelBack2,               'Stellt den Hintergrund der rechten Spalte ein.',                                               '4',       'colorrightcs'))
        list.append(getConfigListEntry(_('_____________________________color lines_______________________________________'), ))
        list.append(getConfigListEntry(_("line"),                         config.plugins.SevenHD.ChannelLine,                'Stellt die Farbe der Linie ein.',                                                             '4',       'linecs'))
        list.append(getConfigListEntry(_("border"),                       config.plugins.SevenHD.ChannelBorder,              'Stellt die Farbe des Rahmen ein.',                                                             '4',       'bordercs'))
        if ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3'):
           pass
        else:
           list.append(getConfigListEntry(_("progressbar"),               config.plugins.SevenHD.ProgressCS,                 'Stellt die Farbe des Fortschrittsbalken ein.',                                                 '4',       'progresscs'))
        if ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3'):
           pass
        else:
           list.append(getConfigListEntry(_("progressbar line"),          config.plugins.SevenHD.ProgressLineCS,             'Stellt die Farbe der Linie unter dem Fortschrittsbalken ein.',                                 '4',       'progresslinecs'))
        list.append(getConfigListEntry(_('_____________________________color description__________________________________'), ))
        list.append(getConfigListEntry(_("bouquet name"),                 config.plugins.SevenHD.ChannelColorBouquet,        'Stellt die Farbe des Bouquetnamen ein. ',                                                      '4',       'bouquetname'))
        if not ChannelSelectionStyle.startswith('channelselection-twocolumns4'):
           list.append(getConfigListEntry(_("program name"),              config.plugins.SevenHD.ChannelColorProgram,        'Stellt die Farbe des aktuellen Programmes ein.',                                                  '4',       'programname'))
        if not ChannelSelectionStyle.startswith('channelselection-twocolumns4'):
           list.append(getConfigListEntry(_("next events"),               config.plugins.SevenHD.ChannelColorNext,           'Stellt die Farbe der n\xc3\xa4chsten Sendungen ein.',                                                '4',       'nextevents'))
        list.append(getConfigListEntry(_("runtime"),                      config.plugins.SevenHD.ChannelColorRuntime,        'Stellt die Farbe der Laufzeit ein.',                                                           '4',       'runtime'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3'):
           list.append(getConfigListEntry(_("channel name"),              config.plugins.SevenHD.ChannelColorChannel,        'Stellt die Farbe des aktuellen Sender auf der linken Seite ein.',                              '4',       'channelnamecs'))
        if not ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("time"),                      config.plugins.SevenHD.ChannelColorTimeCS,         'Stellt die Farbe der Zeit oben rechts ein.',                                                   '4',       'time'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3'):
           pass
        else:
           list.append(getConfigListEntry(_("prime time"),                config.plugins.SevenHD.ChannelColorPrimeTime,      'Stellt die Farbe der PrimeTime ein.',                                                          '4',       'primetime'))
        list.append(getConfigListEntry(_("program description now"),      config.plugins.SevenHD.ChannelColorDesciption,     'Stellt die Farbe der aktuellen Sendung ein.',                                                  '4',       'descriptionnow'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.startswith('channelselection-twocolumns4'):
           list.append(getConfigListEntry(_("program description next"),  config.plugins.SevenHD.ChannelColorDesciptionNext, 'Stellt die Farbe der kommenden Sendung ein.',                                                  '4',       'descriptionnext'))
        if ChannelSelectionStyle.startswith('channelselection-twocolumns4'):
           list.append(getConfigListEntry(_("program description later"), config.plugins.SevenHD.ChannelColorDesciptionLater,'Stellt die Farbe der folgenden Sendungen ein.',                                        '4',       'descriptionlater'))
        list.append(getConfigListEntry(_("buttons"),                      config.plugins.SevenHD.ChannelColorButton,         'Stellt die Farbe der Farbtastenbeschreibung ein.',                                             '4',       'textbuttons'))
        list.append(getConfigListEntry(_('_____________________________color list_________________________________________'), ))
        list.append(getConfigListEntry(_("channel name and number"),      config.plugins.SevenHD.ChannelColorChannelName,    'Stellt die Farbe der Sender ein.',                                                             '4',       'channelnamelist'))
        list.append(getConfigListEntry(_("program"),                      config.plugins.SevenHD.ChannelColorEvent,          'Stellt die Farbe der Sendung ein.',                                                            '4',       'programlist'))
        list.append(getConfigListEntry(_("progressbar"),                  config.plugins.SevenHD.ProgressListCS,             'Stellt die Farbe des Fortschrittsbalken ein.',                                                 '4',       'progresslistcs'))
        list.append(getConfigListEntry(_("progressbar border"),           config.plugins.SevenHD.ProgressBorderCS,           'Stellt die Farbe des Fortschrittsbalkenrahmen ein.',                                          '4',       'progressbordercs'))
        return list

    def __selectionChanged(self):
        self["config"].setList(self.getMenuItemList())

    def GetPicturePath(self):
        returnValue = self["config"].getCurrent()[3]
        self.debug('\nRet_value[3]: ' + str(returnValue))		
           		
        if returnValue == '4':
           returnValue = self["config"].getCurrent()[int(returnValue)]
        else:
           returnValue = self["config"].getCurrent()[int(returnValue)].value
        
        self.debug('Ret_value[4]: ' + str(returnValue))   
        path = MAIN_IMAGE_PATH + str(returnValue) + str(".jpg")
        
        self["description"].setText(self["config"].getCurrent()[2])
        
        if fileExists(path):
           return path
        else:
           self.debug('Missing Picture: ' + str(path) + '\n')
           return MAIN_IMAGE_PATH + str("924938.jpg")

    def UpdatePicture(self):
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.PicLoad.startDecode(self.GetPicturePath())

    def DecodePicture(self, PicInfo = ""):
        ptr = self.PicLoad.getData()
        self["helperimage"].instance.setPixmap(ptr)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.ShowPicture()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.ShowPicture()

    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.ShowPicture()

    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.ShowPicture()
    
    def grab_png(self):
        if config.plugins.SevenHD.grabdebug.value:
           os.system('grab -p /tmp/kraven_debug.png')
           self.session.open(MessageBox, _('Debug Picture\n"kraven_debug.png" saved in /tmp\n'), MessageBox.TYPE_INFO)
           
    def defaults(self):
        self.setInputToDefault(config.plugins.SevenHD.ChannelSelectionStyle)
        self.setInputToDefault(config.plugins.SevenHD.PrimeTimeTime)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBack1)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBack2)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBack3)
        self.setInputToDefault(config.plugins.SevenHD.ChannelLine)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBorder)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorButton)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorBouquet)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorChannel)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorNext)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorDesciptionNext)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorDesciptionNext)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorRuntime)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorProgram)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorTimeCS)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorPrimeTime)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorDesciption)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorChannelName)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorChannelNumber)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorEvent)
        self.setInputToDefault(config.plugins.SevenHD.ProgressBorderCS)
        self.setInputToDefault(config.plugins.SevenHD.ProgressLineCS)
        self.setInputToDefault(config.plugins.SevenHD.ProgressCS)
        self.setInputToDefault(config.plugins.SevenHD.ProgressListCS)
        self.save()

    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)

    def save(self):
        
        if config.plugins.SevenHD.skin_mode.value > '3':
           if 'back' in config.plugins.SevenHD.ChannelBack1.value:
              self.setInputToDefault(config.plugins.SevenHD.ChannelBack1)
              self.session.open(MessageBox, _('Sorry, only Colors allowed.'), MessageBox.TYPE_INFO)
           if 'back' in config.plugins.SevenHD.ChannelBack2.value:
              self.setInputToDefault(config.plugins.SevenHD.ChannelBack2)
              self.session.open(MessageBox, _('Sorry, only Colors allowed.'), MessageBox.TYPE_INFO)
           if 'back' in config.plugins.SevenHD.ChannelBack3.value:
              if 'channelselection-threecolumns' in config.plugins.SevenHD.ChannelSelectionStyle.value:
                 self.setInputToDefault(config.plugins.SevenHD.ChannelBack3)
                 self.session.open(MessageBox, _('Sorry, only Colors allowed.'), MessageBox.TYPE_INFO)
              else:
                 self.setInputToDefault(config.plugins.SevenHD.ChannelBack3)
                 
        for x in self["config"].list:
            if len(x) > 1:
                x[1].save()
            else:
                pass

        configfile.save()
        self.exit()

    def exit(self):
        for x in self["config"].list:
            if len(x) > 1:
                    x[1].cancel()
            else:
                    pass
        self.close()
    
    def debug(self, what):
        if config.plugins.SevenHD.msgdebug.value:
           try:
              self.session.open(MessageBox, _('[ChannelSettings]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
              
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[ChannelSettings]' + str(what) + '\n')
           f.close() 