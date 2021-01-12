# enable import from ./api/ folder
import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),os.path.expanduser(__file__)))),"..")))



from api.server import *



s=WS(("192.168.178.56","8080"))
s.start()
def f(m):
	print("PACKET: "+m)
	return "null"
s.add_packet("join",f)