__author__ = 'jond'

import re

try:
    from PyQt4 import QtCore, QtNetwork
except ImportError:
    from PySide import QtCore, QtNetwork

try:
    import urls
except ImportError:
    print "Application is not properly configured. please provide urls.py"
    raise

class NetworkAccessManager(QtNetwork.QNetworkAccessManager):
    """
    Our network asccess manager that is used instead of the default
    This allows us to jump in and interupt the calls to usually external
    services
    """
    def createRequest(self, operation, request, data):
        """
        Deal with the request when it comes in
        """
        reply = None
        requrl = request.url()
        requrlstr = requrl.toString()
        for urltuple in urls.REDIRECTS:
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

