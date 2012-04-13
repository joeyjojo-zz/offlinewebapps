# -*- encoding: utf-8 -*-
__author__ = 'jond'

import re
import urlparse
import urllib
import framework.handlers.qnetworkhandler as qnetworkhandler

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
    Our network access manager that is used instead of the default
    This allows us to jump in and interrupt the calls to usually external
    services
    """
    def createRequest(self, operation, request, data):
        """
        Deal with the request when it comes in
        TODO: Only deals with keyworded get requests in urls not ordered
        """
        reply = None
        requrl = request.url()
        requrlstr = requrl.toString()
        for urltuple in urls.REDIRECTS:
            m = re.search(urltuple[0], requrlstr)
            if m:
                argd = {}
                if data is not None:
                    # parse the post data
                    postargs = unicode(data.readAll())
                    argd = urlparse.parse_qs(urllib.unquote_plus(postargs.encode('ascii')).decode('utf-8'),
                                             keep_blank_values=True)
                # add get data keyword arguments
                argd.update(m.groupdict())

                reply = qnetworkhandler.FakeReply(self, request, operation, urltuple[1], argd)
                # set up the reply with the correct status
                reply.setAttribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute, 200)
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return reply



