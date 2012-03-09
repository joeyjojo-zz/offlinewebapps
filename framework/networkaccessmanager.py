# -*- encoding: utf-8 -*-
__author__ = 'jond'

import re
import json
import urlparse
import urllib

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
                argd = {}
                if data is not None:
                    # parse the post data
                    postargs = unicode(data.readAll())
                    argd = urlparse.parse_qs(urllib.unquote_plus(postargs.encode('ascii')).decode('utf-8'),
                                             keep_blank_values=True)

                reply = FakeReply(self, request, operation, urltuple[1], argd)
                # set up the reply with the correct status
                reply.setAttribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute, 200)
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return reply

class FakeReply(QtNetwork.QNetworkReply):
    """
    The reply class that is used when a url is to be dealt with by the application
    and is not to be dealt with by the usual method
    """
    def __init__(self, parent, request, operation, f, args={}):
        """
        @type args: dict
        """
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.setRequest(request)
        self.setUrl(request.url())
        self.setOperation(operation)
        self.open(self.ReadOnly | self.Unbuffered)
        # if any are lists of 1 item then just send the item through
        for k, v in args.items():
            if type(v) is type([]):
                if len(v) is 1:
                    args[k] = v[0]
        self.content = f(**args)
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

