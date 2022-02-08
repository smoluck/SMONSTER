#python
#---------------------------------------
# Name:         SMO_HelpWebsiteCMD.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               open the Smoluck Help Website
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      03/03/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

lx.eval('layout.create width:1024 height:768 style:palette')
lx.eval('viewport.restore {} false webView')
lx.eval('select.viewport viewport:0 frame:4')
lx.eval('webview.homePageURL "http://smoluck.com/"')
lx.eval('webview.homePageAlways true')
lx.eval('webview.goHome')



# import PySide
# from PySide.QtWebKit import *

# # Subclassing from lxifc.CustomView
# class SmoluckWebsite(lxifc.CustomView):

    # def customview_Init(self, pane):

        # if pane is None:
            # return False

        # custPane = lx.object.CustomPane(pane)

        # if not custPane.test():
            # return False

        # # get the parent object
        # parent = custPane.GetParent()

        # # convert to PySide QWidget
        # p = lx.getQWidget(parent)

        # # Check that it suceeds
        # if p is not None:
            # layout = PySide.QtGui.QVBoxLayout()

            # # Creating a QWebView widget
            # web = QWebView()
            # web.load("http://smoluck.com/")
            # web.show()
            
            # layout.addWidget(web)
            # layout.setContentsMargins(2,2,2,2)
            # p.setLayout(layout)
            # return True

        # return False
        
# if( not lx.service.Platform().IsHeadless() ):
    # lx.bless(SmoluckWebsite, "SMO HelpWebsite ")