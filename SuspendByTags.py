# -*- coding: utf-8 -*-
# Copyright: Olivier Binda <olivier.binda@wanadoo.fr>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# ---------------------------------------------------------------------------
# This file is a plugin for the "anki" flashcard application http://ichi2.net/anki/
# ---------------------------------------------------------------------------
from PyQt4 import QtGui, QtCore
import os 
from ankiqt import mw
from anki.utils import addTags,deleteTags,parseTags

myDict = {
'French':u'french français',
'Maths':'math maths',
'English':'english anglais',
'Physics':'physique',
'SI':'si'
}
# I'm using 2 different ways to suspend cards in this plugin... this brings 2 different colors in the fact browser...strange...which one is the best ? the red one looks faster (anki level suspend <> sqllite level suspend)

def block(string):
    query = """select cards.Id from cardTags, tags, cards
                 where cardTags.tagId = tags.id and cards.Id= cardTags.cardId and cards.type = 2 
                 and tags.tag in ('%(tags)s') group by cardTags.cardId
                 """ % {'tags':"','".join(parseTags(myDict[string]))}
    cards = list(mw.deck.s.column0(query))
    mw.deck.suspendCards(cards)
         
def unblock(string):
    query = """select cards.Id from cardTags, tags, cards
                 where cardTags.tagId = tags.id and cards.Id= cardTags.cardId and cards.type = 2 
                 and tags.tag in ('%(tags)s') group by cardTags.cardId
                 """ % {'tags':"','".join(parseTags(myDict[string]))}
    cards = list(mw.deck.s.column0(query))
    mw.deck.unsuspendCards(cards)

def switch(string): 
    myAction = mw.mainWin.__getattribute__('action'+ string)
    choice = mw.config.get('SBT_'+ string,0)
    if choice == 0:
            block(string)
            #mw.deck.lowPriority = addTags(myDict[string],mw.deck.lowPriority)
            myAction.setIcon(myPictures['NoNew'+string])
    elif choice == 1:
            #mw.deck.lowPriority = deleteTags(myDict[string],mw.deck.lowPriority)
            mw.deck.suspended  = addTags(myDict[string],mw.deck.suspended)
            myAction.setIcon(myPictures['No'+string])
    else:
            unblock(string)
            mw.deck.suspended = deleteTags(myDict[string],mw.deck.suspended)
            myAction.setIcon(myPictures[string])
    mw.config['SBT_'+ string] = (choice + 1) % 3        
    mw.deck.updateAllPriorities()        


myPictures = {}
mw.mainWin.myActions = {}
for string in myDict.iterkeys():
    exec """def on%s():switch('%s')""" % (string,string)
    for prefix in ['','NoNew','No']:
        myPictures[prefix+string] = QtGui.QIcon()
        myPictures[prefix+string].addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__ ),"Icons",prefix+string+'.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    mw.mainWin.__setattr__('action'+ string, QtGui.QAction(string, mw))
    myAction = mw.mainWin.__getattribute__('action'+ string)
    myAction.setEnabled(not not mw.deck)
    mw.connect(myAction , QtCore.SIGNAL('triggered()'), eval ('on' +string))    
    # creates Suspend/Unsuspend Action
    choice = mw.config.get('SBT_'+ string,0)
    if choice == 0:
        myAction.setIcon(myPictures[string])      
    elif choice == 1:
        myAction.setIcon(myPictures['NoNew'+string])    
    else:
        myAction.setIcon(myPictures['No'+string])     
    myAction.setObjectName(string)
    # adds the Suspend/Unsuspend icon in the Anki Toolbar
    mw.mainWin.toolBar.addAction(myAction)
  
mw.deckRelatedMenuItems = mw.deckRelatedMenuItems + tuple(myDict.iterkeys())

oldLoadDeck = mw.loadDeck

def newLoadDeck(deckPath, sync=True, interactive=True, uprecent=True,media=None):
    code = oldLoadDeck(deckPath, sync, interactive, uprecent,media)
    if code and mw.deck:
        for string in myDict.iterkeys():
            myAction = mw.mainWin.__getattribute__('action'+ string)
            choice = mw.config.get('SBT_'+ string,0)
            if choice == 0:
                myAction.setStatusTip(string)
                pass  
            elif choice == 1:
                block(string)
                #mw.deck.lowPriority  = addTags(myDict[string],mw.deck.lowPriority)  
                myAction.setStatusTip('No new '+string)
            else:
                mw.deck.suspended  = addTags(myDict[string],mw.deck.suspended)  
                myAction.setStatusTip('No '+string)
        mw.deck.updateAllPriorities()     
    return code

mw.loadDeck = newLoadDeck
