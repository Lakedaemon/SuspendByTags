# -*- coding: utf-8 -*-
# Copyright: Olivier Binda <olivier.binda@wanadoo.fr>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# ---------------------------------------------------------------------------
# This file is a plugin for the "anki" flashcard application http://ichi2.net/anki/
# ---------------------------------------------------------------------------
from PyQt4 import QtGui, QtCore
import os 
from ankiqt import mw
from anki.utils import addTags,deleteTags


def onEnglish():
    swith('English')
def onFrench():
    swith('French')
def onSI():
    swith('SI')
def onMaths():
    swith('Maths')
def onPhysics():
    swith('Physics')
    
myDict = {
'French':'french',
'Maths':'math maths',
'English':'english anglais',
'Physics':'physique',
'SI':u'si'
}

myFunctions={
'English':onEnglish,
'French':onFrench,
'SI':onSI,
'Maths':onMaths,
'Physics':onPhysics
}

myPictures = {
('Maths',''):'Maths.png',
('Maths','un'):'UnMaths.png',
('Physics',''):'Physics.png',
('Physics','un'):'UnPhysics.png',
('SI',''):'SI.png',
('SI','un'):'UnSI.png',
('French',''):'French.png',
('French','un'):'UnFrench.png',
('English',''):'English.png',
('English','un'):'UnEnglish.png'
}

def swith(string):
    mw.config['SBT_'+ string] = not(mw.config.setdefault('SBT_'+ string,False))
    if mw.config['SBT_'+ string]:
            mw.deck.suspended = addTags(mw.deck.suspended,myDict[string])
            mw.mainWin.myActions[string].setIcon(myPictures[(string,'','icon')])
    else:
            mw.deck.suspended = deleteTags(mw.deck.suspended,myDict[string])
            mw.mainWin.myActions[string].setIcon(myPictures[(string,'un','icon')])
    mw.deck.updateAllPriorities()        
    mw.help.showText(str(mw.deck.suspended))



mw.mainWin.myActions = {}
for string in myDict.iterkeys():
    for prefix in ['','un']:
        myPictures[(string,prefix,'icon')] = QtGui.QIcon()
        myPictures[(string,prefix,'icon')].addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__ ),myPictures[(string,prefix)])), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    mw.mainWin.myActions[string] = QtGui.QAction(string + ' / no ' + string, mw)
    mw.mainWin.myActions[string] .setStatusTip('Suspend/Unsuspend')
    mw.mainWin.myActions[string] .setEnabled(not not mw.deck)
    mw.connect(mw.mainWin.myActions[string] , QtCore.SIGNAL('triggered()'), myFunctions[string])    

    # creates Suspend/Unsuspend Action
    if mw.config['SBT_'+ string]:
        mw.mainWin.myActions[string].setIcon(myPictures[(string,'','icon')])
    else:
        mw.mainWin.myActions[string].setIcon(myPictures[(string,'un','icon')])        
    mw.mainWin.myActions[string].setObjectName(string)



    # adds the Suspend/Unsuspend icon in the Anki Toolbar
	
    mw.mainWin.toolBar.addAction(mw.mainWin.myActions[string])
  

mw.mainWin.actionMaths = mw.mainWin.myActions['Maths']
mw.mainWin.actionPhysics = mw.mainWin.myActions['Physics']
mw.mainWin.actionSI = mw.mainWin.myActions['SI']
mw.mainWin.actionFrench = mw.mainWin.myActions['French']
mw.mainWin.actionEnglish = mw.mainWin.myActions['English']  

mw.deckRelatedMenuItems = mw.deckRelatedMenuItems + tuple(myDict.iterkeys())
# to enable or disable Jstats whenever a deck is opened/closed

