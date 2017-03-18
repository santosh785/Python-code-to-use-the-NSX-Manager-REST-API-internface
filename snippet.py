#!/usr/bin/python3
#
# This Python script shows how to make basic REST API calls to an NSX
# Manager Server.
#
# More information on the NSX Manager REST API is here:
# http://pubs.vmware.com/nsx-63/topic/com.vmware.ICbase/PDF/nsx_63_api.pdf
# https://pubs.vmware.com/NSX-6/topic/com.vmware.ICbase/PDF/nsx_604_api.pdf

import base64
import ssl
import urllib.request

authorizationField = ''

def nsxSetup(username, password):
   '''Setups up Python's urllib library to communicate with the
      NSX Manager.  Uses TLS 1.2 and no cert, for demo purposes.
      Sets the authorization field you need to put in the
      request header into the global variable: authorizationField.
   '''
   global authorizationField

   context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
   context.verify_mode = ssl.CERT_NONE
   httpsHandler = urllib.request.HTTPSHandler(context = context)

   manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
   authHandler = urllib.request.HTTPBasicAuthHandler(manager)

   # The opener will be used for for all urllib calls, from now on.
   opener = urllib.request.build_opener(httpsHandler, authHandler)
   urllib.request.install_opener(opener)

   basicAuthString = '%s:%s' % (username, password)
   field = base64.b64encode(basicAuthString.encode('ascii'))
   #Debugging: print('Basic %s' % str(field,'utf-8'))
   authorizationField = 'Basic %s' % str(field,'utf-8')

def nsxGet(url, fileName=None):
   '''Does a HTTP GET on the NSX Manager REST Server.
      If a second argument is given, the result is stored in a file
      with that name.  Otherwise, it is written to standard output.
   '''
   global authorizationField

   request = urllib.request.Request(url,
             headers={'Authorization': authorizationField})
   response = urllib.request.urlopen(request)
   if fileName == None:
      print('REST %s:' % url)
      print(response.read().decode())
   else:
      print('REST %s is in file %s.' % (url, fileName))
      with open(fileName, 'w') as newFile:
         print(response.read().decode(),file=newFile)
   print('')

def nsxGetJson(url, fileName=None):
   '''Just like nsxGet, except that it asks for a JSON answer, rather than
      getting the default format (usually XML, but not always).
      Does a HTTP GET on the NSX Manager REST Server.
      If a second argument is given, the result is stored in a file
      with that name.  Otherwise, it is written to standard output.
   '''
   global authorizationField

   request = urllib.request.Request(url,
             headers={'Authorization': authorizationField,
                      'Accept': 'application/json'})
   response = urllib.request.urlopen(request)
   if fileName == None:
      print('REST JSON %s:' % url)
      print(response.read().decode())
   else:
      print('REST JSON %s is in file %s.' % (url, fileName))
      with open(fileName, 'w') as newFile:
         print(response.read().decode(),file=newFile)
   print('')

nsxSetup('admin','default')
nsxGet('https://10.161.2.73/api/1.0/appliance-management/global/info')
nsxGet('https://10.161.2.73/api/1.0/appliance-management/global/info','v.txt')

print('Can also get JSON data back from the server:')
nsxGetJson('https://10.161.2.73/api/1.0/appliance-management/system/meminfo')
print('Or that same information in XML format:')
nsxGet('https://10.161.2.73/api/1.0/appliance-management/system/meminfo')

print('Example of a REST call that does not return XML or JSON:')
nsxGet('https://10.161.2.73/api/1.0/appliance-management/system/uptime')
