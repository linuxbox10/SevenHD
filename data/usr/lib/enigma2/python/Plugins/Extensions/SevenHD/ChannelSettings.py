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
                         <widget name="buttonRed" font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" transparent="1" />
                         <widget name="buttonGreen" font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" transparent="1" />
                         <widget name="buttonYellow" font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" transparent="1" />
                         <widget name="buttonBlue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <widget name="titel" position="70,12" size="708,46" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
                         <widget name="colorthump" position="891,220" size="372,30" zPosition="1" backgroundColor="#00000000" alphatest="blend" />
                         <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
                         <widget name="description" position="891,490" size="372,200" font="Regular; 22" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
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
        self.ColorLoad = ePicLoad()
        self["colorthump"] = Pixmap()
        self["helperimage"] = Pixmap()
        self["description"] = Label()
        self["buttonRed"] = Label()
        self["buttonGreen"] = Label()
        self["buttonYellow"] = Label()
        self["buttonBlue"] = Label()
        self["titel"] = Label()
        self["buttonRed"].setText(_("Cancel"))
        self["buttonGreen"].setText(_("Save"))
        self["buttonYellow"].setText(_("Defaults"))
        self["titel"].setText(_("Channel Settings"))
        
        if config.plugins.SevenHD.grabdebug.value:
           self["buttonBlue"].setText('Screenshot')
           
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
        list.append(getConfigListEntry(_("style"),                        config.plugins.SevenHD.ChannelSelectionStyle,      'W\xc3\xa4hle den Stil der Kanalliste',                            '1',        ''))
        ChannelSelectionStyle = config.plugins.SevenHD.ChannelSelectionStyle.value
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3') or ChannelSelectionStyle.startswith('channelselection-onecolumntwo'):
           pass
        else:
           list.append(getConfigListEntry(_("prime time"),                config.plugins.SevenHD.PrimeTimeTime,              'Zeigt dir in der Kanalliste die PrimeTime an.',                   '4',       'primetime'))
        list.append(getConfigListEntry(_('_____________________________background________________________________________'), ))
        list.append(getConfigListEntry(_("color left"),                   config.plugins.SevenHD.ChannelBack1,               'Stellt den Hintergrund der linken Spalte ein.',                   '4',       'colorleftcs'))
        if config.plugins.SevenHD.ChannelBack1.value=="back_gradient_csleft":
            list.append(getConfigListEntry(_("gradient top"),                 config.plugins.SevenHD.GradientCSLeftTop,          'Stellt die obere Farbe vom Farbverlauf der linken Spalte ein.',                   '4',       'colorleftcs'))
            list.append(getConfigListEntry(_("gradient bottom"),              config.plugins.SevenHD.GradientCSLeftBottom,       'Stellt die untere Farbe vom Farbverlauf der linken Spalte ein.',                   '4',       'colorleftcs'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("color middle"),              config.plugins.SevenHD.ChannelBack3,               'Stellt den Hinergrund der mittleren Spalte ein',                  '4',       'colormiddlecs'))
           if config.plugins.SevenHD.ChannelBack3.value=="back_gradient_csmiddle":
               list.append(getConfigListEntry(_("gradient top"),              config.plugins.SevenHD.GradientCSMiddleTop,        'Stellt die obere Farbe vom Farbverlauf der mittleren Spalte ein',                  '4',       'colormiddlecs'))
               list.append(getConfigListEntry(_("gradient bottom"),              config.plugins.SevenHD.GradientCSMiddleBottom,       'Stellt die untere Farbe vom Farbverlauf der mittleren Spalte ein',                  '4',       'colormiddlecs'))
        if not ChannelSelectionStyle.startswith('channelselection-onecolumn'):
           list.append(getConfigListEntry(_("color right"),                  config.plugins.SevenHD.ChannelBack2,               'Stellt den Hintergrund der rechten Spalte ein.',                  '4',       'colorrightcs'))
           if config.plugins.SevenHD.ChannelBack2.value=="back_gradient_csright":
               list.append(getConfigListEntry(_("gradient top"),                 config.plugins.SevenHD.GradientCSRightTop,               'Stellt die obere Farbe vom Farbverlauf der rechten Spalte ein.',                  '4',       'colorrightcs'))
               list.append(getConfigListEntry(_("gradient bottom"),              config.plugins.SevenHD.GradientCSRightBottom,               'Stellt die unteren Farbe vom Farbverlauf der rechten Spalte ein.',                  '4',       'colorrightcs'))
        list.append(getConfigListEntry(_('__________________________________transparency_____________________________________________'), ))
        list.append(getConfigListEntry(_("left window"),                  config.plugins.SevenHD.CSLeftColorTrans,           'Stellt die Transparenz des linken Fenster ein.',                  '4',       'csleft'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("middle window"),                config.plugins.SevenHD.CSMiddleColorTrans,         'Stellt die Transparenz des mittleren Fenster ein.',               '4',       'csmiddle'))
        if not ChannelSelectionStyle.startswith('channelselection-onecolumn'):
           list.append(getConfigListEntry(_("right window"),                 config.plugins.SevenHD.CSRightColorTrans,          'Stellt die Transparenz des rechten Fenster ein.',                 '4',       'csright'))
        list.append(getConfigListEntry(_('_____________________________color lines_______________________________________'), ))
        list.append(getConfigListEntry(_("line leftside"),                config.plugins.SevenHD.ChannelLine,                'Stellt die Farbe der Linie der linken Spalte ein.',               '4',       'linecs'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("line middle"),               config.plugins.SevenHD.ChannelLineMiddle,          'Stellt die Farbe der Linie der mittleren Spalte ein.',            '4',       'linecs'))
        if not ChannelSelectionStyle.startswith('channelselection-onecolumn'):
           list.append(getConfigListEntry(_("line rightside"),               config.plugins.SevenHD.ChannelLineRight,           'Stellt die Farbe der Linie der rechten Spalte ein.',              '4',       'linecs'))
        list.append(getConfigListEntry(_("border leftside"),              config.plugins.SevenHD.ChannelBorder,              'Stellt die Farbe des Rahmen der linken Spalte ein.',              '4',       'bordercs'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("border middle"),             config.plugins.SevenHD.ChannelBorderMiddle,        'Stellt die Farbe des Rahmen der mittleren Spalte ein.',           '4',       'bordercs'))
        if not ChannelSelectionStyle.startswith('channelselection-onecolumn'):
           list.append(getConfigListEntry(_("border rightside"),             config.plugins.SevenHD.ChannelBorderRight,         'Stellt die Farbe des Rahmen der rechten Spalte ein.',             '4',       'bordercs'))
        if ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3') or ChannelSelectionStyle.startswith('channelselection-onecolumntwo'):
           pass
        else:
           list.append(getConfigListEntry(_("progressbar"),               config.plugins.SevenHD.ProgressCS,                 'Stellt die Farbe des Fortschrittsbalken ein.',                    '4',       'progresscs'))
        if ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3') or ChannelSelectionStyle.startswith('channelselection-onecolumntwo'):
           pass
        else:
           list.append(getConfigListEntry(_("progressbar line"),          config.plugins.SevenHD.ProgressLineCS,             'Stellt die Farbe der Linie unter dem Fortschrittsbalken ein.',    '4',       'progresslinecs'))
        list.append(getConfigListEntry(_('_____________________________color description__________________________________'), ))
        list.append(getConfigListEntry(_("bouquet name"),                 config.plugins.SevenHD.ChannelColorBouquet,        'Stellt die Farbe des Bouquetnamen ein. ',                         '4',       'bouquetname'))
        if not config.plugins.SevenHD.ChannelSelectionStyle.value in ('channelselection-twocolumns4','channelselection-onecolumntwo'):
           list.append(getConfigListEntry(_("program name"),              config.plugins.SevenHD.ChannelColorProgram,        'Stellt die Farbe des aktuellen Programmes ein.',                  '4',       'programname'))
        if  ChannelSelectionStyle.startswith('channelselection-twocolumns4') or ChannelSelectionStyle.endswith('6') or ChannelSelectionStyle.startswith('channelselection-onecolumntwo'):
           pass
        else:
           list.append(getConfigListEntry(_("next events"),               config.plugins.SevenHD.ChannelColorNext,           'Stellt die Farbe der n\xc3\xa4chsten Sendungen ein.',             '4',       'nextevents'))
        if not ChannelSelectionStyle.startswith('channelselection-onecolumntwo'):
           list.append(getConfigListEntry(_("runtime"),                      config.plugins.SevenHD.ChannelColorRuntime,        'Stellt die Farbe der Laufzeit ein.',                              '4',       'runtime'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3') or ChannelSelectionStyle.startswith('channelselection-twocolumns6'):
           list.append(getConfigListEntry(_("channel name"),              config.plugins.SevenHD.ChannelColorChannel,        'Stellt die Farbe des aktuellen Sender auf der linken Seite ein.', '4',       'channelnamecs'))
        if not ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("time"),                      config.plugins.SevenHD.ChannelColorTimeCS,         'Stellt die Farbe der Zeit oben rechts ein.',                      '4',       'time'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3') or ChannelSelectionStyle.startswith('channelselection-onecolumntwo'):
           pass
        else:
           list.append(getConfigListEntry(_("prime time"),                config.plugins.SevenHD.ChannelColorPrimeTime,      'Stellt die Farbe der PrimeTime ein.',                             '4',       'primetime'))
        list.append(getConfigListEntry(_("program description now"),      config.plugins.SevenHD.ChannelColorDesciption,     'Stellt die Farbe der aktuellen Sendung ein.',                     '4',       'descriptionnow'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.startswith('channelselection-twocolumns4') or ChannelSelectionStyle.startswith('channelselection-twocolumns6'):
           list.append(getConfigListEntry(_("program description next"),  config.plugins.SevenHD.ChannelColorDesciptionNext, 'Stellt die Farbe der kommenden Sendung ein.',                     '4',       'descriptionnext'))
        if ChannelSelectionStyle.startswith('channelselection-twocolumns4'):
           list.append(getConfigListEntry(_("program description later"), config.plugins.SevenHD.ChannelColorDesciptionLater,'Stellt die Farbe der folgenden Sendungen ein.',                   '4',       'descriptionlater'))
        list.append(getConfigListEntry(_("buttons"),                      config.plugins.SevenHD.ChannelColorButton,         'Stellt die Farbe der Farbtastenbeschreibung ein.',                '4',       'textbuttons'))
        list.append(getConfigListEntry(_('_____________________________color list_________________________________________'), ))
        list.append(getConfigListEntry(_("channel name and number"),      config.plugins.SevenHD.ChannelColorChannelName,    'Stellt die Farbe der Sender ein.',                                '4',       'channelnamelist'))
        list.append(getConfigListEntry(_("program"),                      config.plugins.SevenHD.ChannelColorEvent,          'Stellt die Farbe der Sendung ein.',                               '4',       'programlist'))
        list.append(getConfigListEntry(_("progressbar"),                  config.plugins.SevenHD.ProgressListCS,             'Stellt die Farbe des Fortschrittsbalken ein.',                    '4',       'progresslistcs'))
        list.append(getConfigListEntry(_("progressbar border"),           config.plugins.SevenHD.ProgressBorderCS,           'Stellt die Farbe des Fortschrittsbalkenrahmen ein.',              '4',       'progressbordercs'))
        return list

    def __selectionChanged(self):
        self["config"].setList(self.getMenuItemList())

    def GetPicturePath(self):
        returnValue = self["config"].getCurrent()[3]
           		
        if returnValue == '4':
           returnValue = self["config"].getCurrent()[int(returnValue)]
        else:
           returnValue = self["config"].getCurrent()[int(returnValue)].value
        
        path = MAIN_IMAGE_PATH + str(returnValue) + str(".jpg")
        
        self["description"].setText(self["config"].getCurrent()[2])
        
        if fileExists(path):
           return path
        else:
           self.debug('Missing Picture: ' + str(path) + '\n')
           return MAIN_IMAGE_PATH + str("924938.jpg")

    def UpdatePicture(self):
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.UpdateColor()
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.PicLoad.startDecode(self.GetPicturePath())

    def DecodePicture(self, PicInfo = ""):
        ptr = self.PicLoad.getData()
        self["helperimage"].instance.setPixmap(ptr)

    def UpdateColor(self):
        self.ColorLoad.PictureData.get().append(self.DecodeColor)
        self.onLayoutFinish.append(self.ShowColor)

    def ShowColor(self):
        self.ColorLoad.setPara([self["colorthump"].instance.size().width(),self["colorthump"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.ColorLoad.startDecode(self.getFontColor())

    def DecodeColor(self, PicInfo = ""):
        ptr = self.ColorLoad.getData()
        self["colorthump"].instance.setPixmap(ptr)
    
    def getFontColor(self):   
        returnValue = self["config"].getCurrent()[1]
        self.debug(returnValue)
        self["colorthump"].instance.show()
        preview = ''
        if returnValue == config.plugins.SevenHD.ChannelSelectionStyle:
              self["colorthump"].instance.hide()
        elif returnValue == config.plugins.SevenHD.PrimeTimeTime:
              self["colorthump"].instance.hide()
        elif returnValue == config.plugins.SevenHD.ChannelBack1:
              preview = self.generate(config.plugins.SevenHD.ChannelBack1.value)
        elif returnValue == config.plugins.SevenHD.ChannelBack2:
              preview = self.generate(config.plugins.SevenHD.ChannelBack2.value)
        elif returnValue == config.plugins.SevenHD.ChannelBack3:
              preview = self.generate(config.plugins.SevenHD.ChannelBack3.value)  
        elif returnValue == config.plugins.SevenHD.ChannelLine:
              preview = self.generate(config.plugins.SevenHD.ChannelLine.value)
        elif returnValue == config.plugins.SevenHD.ChannelBorder:
              preview = self.generate(config.plugins.SevenHD.ChannelBorder.value)
        elif returnValue == config.plugins.SevenHD.ChannelLineRight:
              preview = self.generate(config.plugins.SevenHD.ChannelLineRight.value)
        elif returnValue == config.plugins.SevenHD.ChannelLineMiddle:
              preview = self.generate(config.plugins.SevenHD.ChannelLineMiddle.value)
        elif returnValue == config.plugins.SevenHD.ChannelBorderRight:
              preview = self.generate(config.plugins.SevenHD.ChannelBorderRight.value)
        elif returnValue == config.plugins.SevenHD.ChannelBorderMiddle:
              preview = self.generate(config.plugins.SevenHD.ChannelBorderMiddle.value) 
        elif returnValue == config.plugins.SevenHD.ProgressCS:
              preview = self.generate(config.plugins.SevenHD.ProgressCS.value)
        elif returnValue == config.plugins.SevenHD.ProgressLineCS:
              preview = self.generate(config.plugins.SevenHD.ProgressLineCS.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorBouquet:
              preview = self.generate(config.plugins.SevenHD.ChannelColorBouquet.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorProgram:
              preview = self.generate(config.plugins.SevenHD.ChannelColorProgram.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorNext:
              preview = self.generate(config.plugins.SevenHD.ChannelColorNext.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorRuntime:
              preview = self.generate(config.plugins.SevenHD.ChannelColorRuntime.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorChannel:
              preview = self.generate(config.plugins.SevenHD.ChannelColorChannel.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorTimeCS:
              preview = self.generate(config.plugins.SevenHD.ChannelColorTimeCS.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorPrimeTime:
              preview = self.generate(config.plugins.SevenHD.ChannelColorPrimeTime.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorDesciption:
              preview = self.generate(config.plugins.SevenHD.ChannelColorDesciption.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorDesciptionNext:
              preview = self.generate(config.plugins.SevenHD.ChannelColorDesciptionNext.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorDesciptionLater:
              preview = self.generate(config.plugins.SevenHD.ChannelColorDesciptionLater.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorButton:
              preview = self.generate(config.plugins.SevenHD.ChannelColorButton.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorChannelName:
              preview = self.generate(config.plugins.SevenHD.ChannelColorChannelName.value)
        elif returnValue == config.plugins.SevenHD.ChannelColorEvent:
              preview = self.generate(config.plugins.SevenHD.ChannelColorEvent.value)
        elif returnValue == config.plugins.SevenHD.ProgressListCS:
              preview = self.generate(config.plugins.SevenHD.ProgressListCS.value)
        elif returnValue == config.plugins.SevenHD.ProgressBorderCS:
              preview = self.generate(config.plugins.SevenHD.ProgressBorderCS.value)
        elif returnValue == config.plugins.SevenHD.GradientCSLeftTop:
              preview = self.generate(config.plugins.SevenHD.GradientCSLeftTop.value)
        elif returnValue == config.plugins.SevenHD.GradientCSLeftBottom:
              preview = self.generate(config.plugins.SevenHD.GradientCSLeftBottom.value)
        elif returnValue == config.plugins.SevenHD.GradientCSMiddleTop:
              preview = self.generate(config.plugins.SevenHD.GradientCSMiddleTop.value)
        elif returnValue == config.plugins.SevenHD.GradientCSMiddleBottom:
              preview = self.generate(config.plugins.SevenHD.GradientCSMiddleBottom.value)
        elif returnValue == config.plugins.SevenHD.GradientCSRightTop:
              preview = self.generate(config.plugins.SevenHD.GradientCSRightTop.value)
        elif returnValue == config.plugins.SevenHD.GradientCSRightBottom:
              preview = self.generate(config.plugins.SevenHD.GradientCSRightBottom.value)
        else:
              self["colorthump"].instance.hide()
        return str(preview)
        
    def generate(self,color):    
        
        if color.startswith('00'):
           r = int(color[2:4], 16)
           g = int(color[4:6], 16)
           b = int(color[6:], 16)

           img = Image.new("RGB",(372,30),(r,g,b))
           img.save(str(MAIN_IMAGE_PATH) + "color.png")
           return str(MAIN_IMAGE_PATH) + "color.png"
        
        elif 'progress' in color:
           return str(MAIN_IMAGE_PATH) + "progress.png"
        elif 'carbon' in color:
           return str(MAIN_IMAGE_PATH) + "carbon.png"
        elif 'lightwood' in color:
           return str(MAIN_IMAGE_PATH) + "lightwood.png"
        elif 'redwood' in color:
           return str(MAIN_IMAGE_PATH) + "redwood.png"
        elif 'slate' in color:
           return str(MAIN_IMAGE_PATH) + "slate.png"
        elif 'brownleather' in color:
           return str(MAIN_IMAGE_PATH) + "brownleather.png"
        elif 'gradient' in color:
           return str(MAIN_IMAGE_PATH) + "gradient.png"
        
    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.ShowPicture()
        self.ShowColor()
        
    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.ShowPicture()
        self.ShowColor()
        
    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.ShowPicture()
        self.ShowColor()
        
    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.ShowPicture()
        self.ShowColor()
        
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
        self.setInputToDefault(config.plugins.SevenHD.ChannelLineRight)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBorderRight)
        self.setInputToDefault(config.plugins.SevenHD.ChannelLineMiddle)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBorderMiddle)
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
        self.setInputToDefault(config.plugins.SevenHD.CSLeftColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.CSMiddleColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.CSRightColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.GradientCSLeftTop)
        self.setInputToDefault(config.plugins.SevenHD.GradientCSLeftBottom)
        self.setInputToDefault(config.plugins.SevenHD.GradientCSRightTop)
        self.setInputToDefault(config.plugins.SevenHD.GradientCSRightBottom)
        self.setInputToDefault(config.plugins.SevenHD.GradientCSMiddleTop)
        self.setInputToDefault(config.plugins.SevenHD.GradientCSMiddleBottom)
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
        
        
        ### changed by tomele for SevenHDPig
        if config.plugins.SevenHD.ChannelSelectionStyle.value == "channelselection-preview":
        	config.plugins.SevenHD.PigStyle.value = "Preview"
        elif config.plugins.SevenHD.ChannelSelectionStyle.value == "channelselection-pip":
        	config.plugins.SevenHD.PigStyle.value = "DualTV"
        elif config.plugins.SevenHD.ChannelSelectionStyle.value == "channelselection-ext":
        	config.plugins.SevenHD.PigStyle.value = "ExtPreview"
        config.plugins.SevenHD.PigStyle.save()
        ### end of change

                 
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