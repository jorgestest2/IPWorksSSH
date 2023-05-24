#
# IPWorks SSH 2022 Python Edition - Demo Application
#
# Copyright (c) 2023 /n software inc. - All rights reserved. - www.nsoftware.com
#

import sys
import string
from ipworksssh import *

input = sys.hexversion<0x03000000 and raw_input or input

def fireStdErr(e):
  print("StdErr: " + bytes.decode(e.text))

def fireStdOut(e):
  print("StdOut: " + bytes.decode(e.text))

def fireSSHStatus(e):
  print("Status: " + e.message)

def fireSSHServerAuth(e):
  print("\nServer provided the following fingerprint:\n%s\n"%e.fingerprint)
  cntue = input("Would you like to continue [y/n]: ")
  if cntue == "Y" or cntue == "y":
      e.accept = True

def newHost():
  host = input("Host: ")
  sexec.ssh_host = host
  port = input("Port (22): ")
  if port == '':
    port = 22
  else:
    port = int(port)
  sexec.ssh_port = port
  user = input("User: ")
  sexec.ssh_user = user
  password = input("Password: ")
  sexec.ssh_password = password
  sexec.ssh_logon(host, port)

sexec = SExec()
sexec.on_ssh_server_authentication = fireSSHServerAuth
sexec.on_ssh_status = fireSSHStatus
sexec.on_stdout = fireStdOut
sexec.on_stderr = fireStdErr

try:
    newHost()
    command = input("Command: ")
    sexec.execute(command)

    while True:
      cntu = input("Would you like to run another command? [y/n]: ")
      if cntu == "n" or cntu == "N":
        print("Goodbye!")
        sexec.ssh_logoff()
        break
      else:
        diffHost = input("Would you like to use a different server? [y/n]: ")
        if diffHost == "n" or diffHost == "N":
          command = input("Command: ")
          sexec.execute(command)
        else:
          sexec.ssh_logoff()
          newHost()
          command = input("Command: ")
          sexec.execute(command)

except IPWorksSSHError as e:
    print( "Error %s"%e.message)
except KeyboardInterrupt:
    print( "Exiting..." )



