__author__ = 'jond'

import sys
import os
import json
import re

try:
    from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
except ImportError:
    from PySide import QtCore, QtGui, QtWebKit, QtNetwork

def getcontacts():

    contacts = [{'guid':1,
                 'firstName':'Jon',
                 'lastName':'Dunleavy',
                 'phoneNumbers':['(415) 555-2380']},
                ]

    return json.dumps({"contacts":contacts})


REDIRECTS = ((re.compile('contacts.json'), getcontacts),)

class NetworkAccessManager(QtNetwork.QNetworkAccessManager):

    def createRequest(self, operation, request, data):
        reply = None
        requrl = request.url()
        requrlstr = requrl.toString()
        if operation == QtNetwork.QNetworkAccessManager.GetOperation:
            for urltuple in REDIRECTS:
                if re.search(urltuple[0], requrlstr):
                    reply = FakeReply(self, request, operation, urltuple[1])
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return reply

class FakeReply(QtNetwork.QNetworkReply):
    """
    The reply class that is used when a url is to be dealt with by the application
    and is not to be dealt with by the usual method
    """
    def __init__(self, parent, request, operation, f):
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.setRequest(request)
        self.setUrl(request.url())
        self.setOperation(operation)
        #self.setFinished(True)
        self.open(self.ReadOnly | self.Unbuffered)

        self.content = f()
        self.offset = 0

        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json; charset=UTF-8")
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, len(self.content))

        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("readyRead()"))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("finished()"))


    def abort(self):
        pass

    def bytesAvailable(self):
        return len(self.content) - self.offset

    def isSequential(self):
        return True

    def readData(self, maxSize):
        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            return data

class MainWindow(QtGui.QMainWindow):
    """
    The main, and only, window of the application
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi()

    def setupUi(self):
        """
        Setup the ui of the window that the webapp will operate in
        """
        centralwidget = QtGui.QWidget()
        centralwidget.setObjectName("centralwidget")
        horizontalLayout = QtGui.QHBoxLayout(centralwidget)
        horizontalLayout.setObjectName("horizontalLayout")
        webView = QtWebKit.QWebView(centralwidget)
        webView.setObjectName("webView")
        webpage = QtWebKit.QWebPage()
        self.setupNetworkManager(webpage)
        webView.setPage(webpage)
        horizontalLayout.addWidget(webView)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(centralwidget)

        gs = QtWebKit.QWebSettings.globalSettings()
        gs.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        gs.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        gs.setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        gs.setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, True)
        gs.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        # Added by PF - allows the inspector to persist your settings in a platform-specific way
        # On Windows this uses the registry, so we don't want this to happen in production builds.
        QtGui.QApplication.setApplicationName("EXAMPLEAPP")
        QtGui.QApplication.setOrganizationName("DEFMYFUNC")

    def setUrl(self, urlstr):
        """
        Set the url of the webview, should only be used on startup
        """
        webView = self.findChild(QtWebKit.QWebView, "webView")
        if webView:
            webView.setUrl(QtCore.QUrl(urlstr))

    def setupNetworkManager(self, page):
        """
        Set up our custom network manager that can interrupt requests
        """
        # set up the network request intercepter
        page.setNetworkAccessManager(NetworkAccessManager())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    u = QtCore.QUrl().fromLocalFile(os.path.join(os.getcwd(), 'app', 'index.html'))
    win.setUrl(u)
    sys.exit(app.exec_())