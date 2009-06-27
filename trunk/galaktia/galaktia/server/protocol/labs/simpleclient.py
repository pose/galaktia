#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, logging

from twisted.internet import reactor
from twisted.python import log

# should be using pyglet, but for this example it's ok
import pygame
from pygame.locals import *

from galaktia.server.protocol.model import Datagram, Command
from galaktia.server.protocol.base import BaseServer, BaseClient
from galaktia.server.protocol.codec import ProtocolCodec
from galaktia.server.protocol.controller import Controller

from galaktia.server.protocol.operations.talk import SayThis
from galaktia.server.protocol.operations.join import RequestUserJoin

logger = logging.getLogger(__name__)

CLIENT_VERSION = 0.1
SCREEN_SIZE = (800, 600)
pygame.init()
font = pygame.font.SysFont("arial", 16)
font_height = font.get_linesize()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
username = "Matias"
playerinLOS = []

class PygameClientController(Controller):
    def greet(self):

        pygame.display.set_caption("Simple Pygame Galaktia Client")
        self.event_text = ["Type Your Username Please..."]
        entered_username = self.prompt()

        return [RequestUserJoin(username=entered_username)]

    def process(self, input_message):
        """ Writes server response and prompts for a new message to send """
        command = input_message['name']
	
	""" Talk commands """
	
	if command == "SomoneSaid":	    
	    string = input_message['message']
	    self.event_text.append(input_message['username'] + ": " + string)
	    self.prompt()
	    return []
	elif command == "SayThisAck":
	    return []
	elif command == "UserAccepted":
	    if input_message['accepted']:
		return [UserAcceptedAck(ack = input_message['id'])]
	    else:
		return [UserAcceptedAck(ack = input_message['id'])]
	elif command == "CheckProtocolVersion":
	    version = input_message['version']
	    if version != CLIENT_VERSION:
		self.event_text.append("Bajate la ultima version de:" + input_message['url'])
	    else:
		self.event_text.append("Version "+ version)
	    self.prompt()
	    return [RequestUserJoin(username = username)]
	elif command == "UserJoined":
	    self.event_text.append("El usuario "+ input_message['username'] + "se ha conectado." )
	    self.prompt()
	    return []
	else:
	    self.event_text[-1] = string
	    self.event_text.append("Type to send chat")
	    self.event_text = self.event_text[-SCREEN_SIZE[1]/font_height:]
	    output_message = self.prompt()
	    if output_message is None:
	   	reactor.stop() # the reactor singleton is not a good idea...
		return []
	    return [SayThis(text=output_message)]
	   # raise ValueError, "Invalid command: %s" % command

    def prompt(self):
        """ Prompts to read a new message to be sent to the server """

        clock = pygame.time.Clock()
        input_string = ""
        keepGoing = True

        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    reactor.stop()
                    return input_string
                elif event.type == KEYDOWN:
                    key = event.key
                    if key == K_RETURN:
                        keepGoing = False
                    elif key == K_BACKSPACE:
                        input_string = input_string[:-1]
                    else:
                        try:
                            input_string += chr(event.key)
                        except:
                            pass
                    self.user_is_typing(input_string)
            screen.fill((255, 255, 255))
            pygame.draw.line(screen, (0,0,0),(0,SCREEN_SIZE[1]-font_height-1),\
                       (SCREEN_SIZE[0],SCREEN_SIZE[1]-font_height-1),1)
            y = SCREEN_SIZE[1]-font_height
            for text in reversed(self.event_text):
                screen.blit( font.render(text, True, (0, 0, 0)), (0, y) )
                y-=font_height
            pygame.display.flip()

        output_message = input_string
        if output_message == 'quit' or output_message == '':
            return None # exits on empty message or by entering 'quit'
        return output_message
        
    def user_is_typing(self, string):
        self.event_text[-1] = string

def main(program, endpoint='client', host='127.0.0.1', port=6414):
    """ Main program: Starts a chat client or server on given host:port """
    class MockSession(object):
        def __init__(self, id):
            self.password = id
    class MockSessionDAO(object):
        def get(self, id):
            return MockSession(id)
    codec = ProtocolCodec(MockSessionDAO())

    log_level = logging.DEBUG
    controller = PygameClientController()
    protocol = BaseClient(codec, controller, host, port)
    port = 0 # dinamically assign client port
    logging.basicConfig(stream=sys.stderr, level=log_level)
    logger.info('Starting %s', endpoint)
    reactor.listenUDP(port, protocol)
    reactor.run()

if __name__ == '__main__': # This is how to run a main program
    reload(sys); sys.setdefaultencoding('utf-8')
    # log.startLogging(sys.stderr) # enables Twisted logging
    main(*sys.argv)

