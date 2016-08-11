# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '10-08.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

#import yapılan kütüphaneler
from PyQt4 import QtCore, QtGui
import re
import httplib
import MySQLdb
from datetime import datetime
from xml.dom.minidom import parse
import xml.dom.minidom
import urllib
import time
import sys
import threading

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# Host adresi
HOST = 'www.netdata.com'
# mesaj alma sayfasi
PAGE = '/AccPo.asmx'
# mesaj almak icin gerekli HEADERS
HEADERS = {'Host':'www.netdata.com','Content-Type':'text/xml; charset=utf-8','SOAPAction':'http://tempuri.org/InsertRecord'}
# mesaj almak icin kullanilacak XML
SOAP = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <InsertRecord xmlns="http://tempuri.org/">
      <APIKey>#AccPoApikodu#</APIKey>
      <InsertList>
        <AccPoKeyValuePair>
          <Key>dc_UserName</Key>
          <Value>#kullaniciAdi#</Value>
        </AccPoKeyValuePair>
        <AccPoKeyValuePair>
          <Key>dc_Message</Key>
          <Value>#mesaj#</Value>
        </AccPoKeyValuePair>
        <AccPoKeyValuePair>
          <Key>dc_MessageTo</Key>
          <Value>string</Value>
        </AccPoKeyValuePair>
     </InsertList>
  </InsertRecord>
</soap:Body>
</soap:Envelope>"""
DEBUG = 1
#gui class
class Ui_MainWindow(object):
    
    #global değişkenler
    AccPoApikodu = ""
    kullaniciAdi = ""
    okumaApi = 'https://www.netdata.com/XML/'
    id2 = int()
    sayac = int()
    
    #constructor
    def __init__(self):
        self.setupUi(MainWindow)
        MainWindow.show()
        self.textBrowser.append("acpoo api gir")
        
    #daha önce yapılan sohbet mesajlarını getirir
    def getir(self):
        document = ('https://www.netdata.com/XML/72dcca41')
        web = urllib.urlopen(document)
        DomTree = xml.dom.minidom.parse(web)
        dataSet = DomTree.documentElement
        dataRow = dataSet.getElementsByTagName("DataRow")
        
        for veri in dataRow:
            userName = veri.getElementsByTagName("dc_UserName")[0]
            message = veri.getElementsByTagName("dc_Message")[0]
            self.textBrowser.append("%s" % userName.childNodes[0].data + " " + ">>>: %s" % message.childNodes[0].data)
            self.textBrowser.update()
            self.textBrowser.moveCursor(QtGui.QTextCursor.End)
            
    #3 saniyede bir mesaj kontrolü yapar
    def tazele(self):
        document = ('https://www.netdata.com/XML/72dcca41?$orderby=ID[desc]&$top=1')
        web = urllib.urlopen(document)
        DomTree = xml.dom.minidom.parse(web)
        dataSet = DomTree.documentElement
        dataRow = dataSet.getElementsByTagName("DataRow")
        desc1 = dataRow[0].getElementsByTagName("ID")[0].firstChild.data
        id1 = int(desc1[0] + desc1[1] + desc1[2])
        
        if id1 != Ui_MainWindow.id2:
            print "geldim"
            desc2 = dataRow[0].getElementsByTagName("ID")[0].firstChild.data
            Ui_MainWindow.id2 = int(desc2[0] + desc2[1] + desc2[2])
            print Ui_MainWindow.id2
            userName = dataRow[0].getElementsByTagName("dc_UserName")[0]
            message = dataRow[0].getElementsByTagName("dc_Message")[0]
            self.textBrowser.append("%s" % userName.childNodes[0].data + " " + ">>>: %s" % message.childNodes[0].data)
            self.textBrowser.update()
            self.textBrowser.moveCursor(QtGui.QTextCursor.End)
        
        threading.Timer(3, self.tazele).start()
        
    #mesajları gönderir
    def text_isle(self):
        if Ui_MainWindow.sayac == 0:
            Ui_MainWindow.AccPoApikodu = str(self.txtMesaj.text())
            self.textBrowser.append("Okumak icin Api Key gir")
            self.txtMesaj.setText(" ")
            
        if Ui_MainWindow.sayac == 1:
            okumakIcinApi = Ui_MainWindow.okumaApi + str(self.txtMesaj.text())
            self.textBrowser.append("Kullanici Adi gir")
            self.txtMesaj.setText("")
            
        if Ui_MainWindow.sayac == 2:
            Ui_MainWindow.kullaniciAdi = str(self.txtMesaj.text())
            self.txtMesaj.setText(" ")
            
        Ui_MainWindow.sayac = Ui_MainWindow.sayac + 1
        
        if Ui_MainWindow.kullaniciAdi != "":
            
            if Ui_MainWindow.sayac == 3:
                self.getir()
                Ui_MainWindow.sayac = Ui_MainWindow.sayac + 1
            mesaj = str(self.txtMesaj.text())
            req = SOAP.replace('#kullaniciAdi#', Ui_MainWindow.kullaniciAdi).replace('#mesaj#', mesaj).replace('#AccPoApikodu#',
                                                                                                                Ui_MainWindow.AccPoApikodu)
            cnn = httplib.HTTPConnection(HOST)
            cnn.request('POST', PAGE, req, HEADERS)
            res = cnn.getresponse().read()
            self.txtMesaj.setText(" ")
            self.tazele()
            
    #gui nesneleri
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(561, 505)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.txtMesaj = QtGui.QLineEdit(self.centralwidget)
        self.txtMesaj.setGeometry(QtCore.QRect(90, 440, 341, 20))
        self.txtMesaj.setObjectName(_fromUtf8("txtMesaj"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 440, 91, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnGnder = QtGui.QPushButton(self.centralwidget)
        self.btnGnder.setGeometry(QtCore.QRect(440, 440, 81, 23))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 212, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 113, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 212, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 212, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 113, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 212, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 212, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 113, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.btnGnder.setPalette(palette)
        self.btnGnder.setObjectName(_fromUtf8("btnGnder"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 10, 501, 421))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 561, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.connect(self.btnGnder, QtCore.SIGNAL("pressed()"), self.text_isle)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "mesaj...", None))
        self.btnGnder.setText(_translate("MainWindow", "gönder", None))

#main function
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    sys.exit(app.exec_())

