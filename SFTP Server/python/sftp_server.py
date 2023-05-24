#
# IPWorks SSH 2022 Python Edition - Demo Application
#
# Copyright (c) 2023 /n software inc. - All rights reserved. - www.nsoftware.com
#

import sys
import string
from ipworksssh import *

input = sys.hexversion<0x03000000 and raw_input or input


def fireError(e):
  print("Error %i: %s\n" %(e.error_code, e.description))

def fireSSHServerAuthentication(e):
  if e.user == "test" and e.auth_method != "none" and e.auth_param == "test":
    print("USER AUTHENTICATED")
    e.accept = True
  else:
    sftpserver.available_methods = "password"

def fireDirList(e):
  print("Listing directory for client")

def ensureArg(argument, prompt, index):
  if len(argument) <= index:
    while len(argument) <= index:
      argument.append(None)
    argument[index] = input(prompt)

def fireConnected(e):
    print(str(e.connection_id) + " Connected")

def fireConnectionRequest(e):
    print(e.address + ':' + str(e.port) + ' is attempting to connect.')

def fireDirCreated(e):
    print(e.user + ' created the directory ' + e.path)

def fireDirRemoved(e):
    print(e.user + ' deleted the directory ' + e.path)

def fireDisconnected(e):
    print('[' + str(e.connection_id) + '] Now Disconnected')

global transtime
global transbytes

print('**********************************************************')
print('* This demo shows how to use the SFTPServer component to *')
print('* create a simple SFTP Server on localhost.              *')
print('* Use the following credentials to connect.              *')
print('* Host: localhost                                        *')
print('* User: test                                             *')
print('* Password: test                                         *')
print('**********************************************************')

sftpserver = SFTPServer()

# For the purposes of this demo we are using the included certificate.
# You may change these options to specify your own certificate.
# See the documentation for additional information.
sftpserver.ssh_cert_store_type = 2
sftpserver.ssh_cert_store = "sftpserver.pfx"
sftpserver.ssh_cert_store_password = "demo"
sftpserver.ssh_cert_subject = "*"

sftpserver.on_connected = fireConnected
sftpserver.on_connection_request = fireConnectionRequest
sftpserver.on_dir_create = fireDirCreated
sftpserver.on_dir_remove = fireDirRemoved
sftpserver.on_dir_list = fireDirList
sftpserver.on_error = fireError
sftpserver.on_disconnected = fireDisconnected
sftpserver.on_ssh_user_auth_request = fireSSHServerAuthentication

root = input("Set root directory to whatever you want or press enter for default ./ ")
sftpserver.root_directory = root
localport = input("Set local port (default 22): ")
if localport == "":
  localport = 22
sftpserver.local_port = int(localport)
sftpserver.listening = True
print("Server listening on port " + str(sftpserver.local_port) + '...')
print("Press Ctrl+C to quit...")
try:
  while True:
    sftpserver.do_events()
except KeyboardInterrupt:
  print("Server shutting down. Goodbye!")
  sftpserver.shutdown()

