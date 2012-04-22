#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import *
from grid import Grid
from ship import Ship
from send import Send
from player import Player
import os
import sys
import fnmatch
import shelve

'''
Seperate Script checks googleVoice and sends battleship requests to this file with the arguments being: phoneNumber = , message =

Commands:
RESET = clear data and starts new game (if in the middle of a game then requests confirmation from other player, sleeps one hour and then purges records
HELP = Send help messages
NUM_PLAY = return number of players online
STATS = return player win/loss statistics (i.e.: Games Played, Times Won, Percentage Won, Times Lost, Percentage Lost, National Rank)
'''

def twitShipMain(phoneNumberA, message):

    message=message.strip()
    
    def status():
        db = shelve.open("twitShipDB")
        if(db.has_key(str(phoneNumberA))):
            playerA = db[str(phoneNumberA)]
            if(playerA.getShipsPlaced() != 5):
                Send("You have placed " + str(playerA.getShipsPlaced()) + " ships and you are currently placing your " + playerA.getNextShipToPlace()[0], phoneNumberA)
            else:
                Send("It is " + ("" if playerA.isTurn() else "not ") + "your turn\n", phoneNumberA)

            return 0
        else:
            Send("You don't exist in our database :( ... initiating game now :D", phoneNumberA)
            return 1

    def myGrid():
        db = shelve.open("twitShipDB")
        if(db.has_key(str(phoneNumberA))):
            playerA = db[str(phoneNumberA)]
            Send(playerA.getGrid().printOwnGrid(), phoneNumberA)
            return 0
        else:
            Send("You don't exist in our database :( ... initiating game now :D", phoneNumberA)
            return 1

    def enemyGrid():
        db = shelve.open("twitShipDB")
        if(db.has_key(str(phoneNumberA))):
            playerA = db[str(phoneNumberA)]
            if(playerA.getOtherID() != 0 and db.has_key(str(playerA.getOtherID()))):
                Send(db[str(playerA.getOtherID())].getGrid().printOpponentGrid(), phoneNumberA)
            else:
               Send("What are you trying to pull?  You don't have an opponent yet!! >:(", phoneNumberA)
            return 0
        else:
            Send("You don't exist in our database :( ... initiating game now :D", phoneNumberA)
            return 1

    def newGame():
        db = shelve.open("twitShipDB")
        if(db.has_key(str(phoneNumberA))):
            del db[str(phoneNumberA)]
        return 1

    def myHelp():
        Send("Commands are: STATUS, MYGRID, ENEMYGRID, NEWGAME, HELP, ONLINE and MSG 'message'", phoneNumberA)
        return 0

    def online():
        db = shelve.open("twitShipDB")
        Send(len(db) - 1, phoneNumberA)
        return 0

    def msg(message):
        db = shelve.open("twitShipDB")
        if(db.has_key(str(phoneNumberA))):
            playerA = db[str(phoneNumberA)]
            if(playerA.getOtherID() != 0 and db.has_key(str(playerA.getOtherID()))):
                Send("Msg from opponent: " + message, playerA.getOtherID())
            else:
               Send("What are you trying to pull?  You don't have an opponent yet!! >:(", phoneNumberA)
            return 0
        else:
            Send("You don't exist in our database :( ... initiating game now :D", phoneNumberA)
            return 1

    def easter():
        Send("You caught me!  Find the area of the solid formed by rotating y=2x around y=x from x=0 to x=5 and send the result to this number (accurate to 0 decimal places) and you will win a prize", phoneNumberA)

    def clue():
        Send(" You just won a free text message!! Congratulations! :) ", phoneNumberA)

    commands = ['STATUS', 'MYGRID', 'ENEMYGRID', 'NEWGAME', 'HELP', 'ONLINE', 'MSG', 'EASTER', '185']
    commandFunc =[status, myGrid, enemyGrid, newGame, myHelp, online, msg, easter, clue]

    strings = message.split(' ', 1)
    if strings[0].upper() in commands:
        if(len(strings) > 1):
            if(not commandFunc[commands.index(strings[0].upper())](strings[1])):
                return 0
        elif(not commandFunc[commands.index(message.upper())]()):
            return 0
    else:
        print message
        
    def strToCoord(userInput):
        x = y = -1
        horiz = -1
        y = ord(userInput[0].upper()) - ord('A')
        x = ord(userInput[1]) - ord('1')
        if(len(userInput) >= 3):
            if(userInput[2].upper() == 'H'):
                horiz = 1;
            elif(userInput[2].upper() == 'V'):
                horiz = 0;
            else:
                Send("Bad coord combination", phoneNumberA);
                return [-1, -1], -1
        if(x not in range(10) or y not in range(10)):
            Send("Bad coord combination: " + "[" + str(x) + ", " + str(y) + "]", phoneNumberA);
            if(horiz == -1):
                return [-1, -1]
            else:
                return [-1, -1], -1
        if(horiz != -1):
            return horiz, [x, y]
        return [x,y]

    phoneNumberB = -1

    db = shelve.open("twitShipDB", flag='c')
    if(db.has_key(str(phoneNumberA))):
        playerA = db[str(phoneNumberA)];
        if(db.has_key(str(playerA.getOtherID()))):
            phoneNumberB = playerA.getOtherID()
            playerB = db[str(phoneNumberB)];
            if(playerA.isTurn()):
                coord = strToCoord(message);
                if(coord != [-1, -1]):
                    ''' good shot '''
                    resultString = playerB.shoot(coord);
                    if(resultString != -1):
                        Send(resultString, phoneNumberA);
                        Send("Enemy shot:\n" + resultString + " at (" + chr(coord[1] + ord('A')) + ", " + str(coord[0]+1) + ")", phoneNumberB);

                        playerA.setTurn(0)
                        playerB.setTurn(1)

                        db[str(phoneNumberA)] = playerA
                        db[str(phoneNumberB)] = playerB
                        
                        if(not playerB.checkShipStatus()):
                            Send("You have sunk all of your opponent's ships!!! :D WINNER!!!  Text back to initate new game :D", phoneNumberA);
                            Send("Your opponent sunk all of your ships :( ... Reply to start a new game", phoneNumberB);
                            del db[str(phoneNumberA)]
                            del db[str(phoneNumberB)]
                        else:
                            Send(playerB.getGrid().printOpponentGrid(), phoneNumberA);
                            Send(playerA.getGrid().printOwnGrid(), phoneNumberA);

                            Send(playerA.getGrid().printOpponentGrid(), phoneNumberB);
                            Send(playerB.getGrid().printOwnGrid(), phoneNumberB);
                    else:
                        Send("You've already shot that location, try again", phoneNumberA)

                else:
                    Send("Bad coordinate, try again", phoneNumberA)
        else:
            ''' Player A exists but isn't paired '''
            if(playerA.getShipsPlaced() < 5):
                ''' not all ships are placed therefore we can check this message as a SHIP PLACE message '''
                horiz, coord = strToCoord(message);
                if(horiz != -1 and not isinstance(coord, int)):
                    ''' our coords are good... going on to stage 2 - FIRING!!! '''
                    if(playerA.placeShip(coord, horiz) == -1):
                        Send("Bad Ship Placement, try again", phoneNumberA)
                    else:
                        db[str(phoneNumberA)] = playerA
                       
                    if(playerA.getShipsPlaced() < 5):
                        nextName, nextSize = playerA.getNextShipToPlace();
                        Send(playerA.getGrid().printOwnGrid(), phoneNumberA);
                        Send("Respond with: XYH (x = letter, y = number, h = horizontal) to place: " + nextName + " which has a width of: " + str(nextSize) + ".", phoneNumberA)
                    else:
                        ''' check to see if there are any other unpaired players '''
                        if(db.has_key("unpairedList")):
                            unpairedList = db["unpairedList"];
                        else:
                            db["unpairedList"] = []
                            unpairedList = db["unpairedList"]
                            
                        if(len(unpairedList) > 0):
                            seed();
                            rand = randint(0, len(unpairedList) - 1);
                            print "Rand = " + str(rand)
                            print unpairedList
                            phoneNumberB = unpairedList[rand];
                            playerB = db[str(phoneNumberB)]
                            del unpairedList[rand]
                            Send("Twitship -- You've been paired!  You have been randomly selected to go first :D ... reply with a coordinate in this format to fire: XY (x = letter, y = number) i.e.: B4 or C2 or F8 :D", phoneNumberA)
                            Send("Twitship: You've been paired!!  You've been randomly selected to go second :( ... it is the other player's turn.", phoneNumberB)
                            playerA.setTurn(1);
                            playerB.setTurn(0);
                            playerA.setOtherID(phoneNumberB);
                            playerB.setOtherID(phoneNumberA);
                            db[str(phoneNumberA)] = playerA
                            db[str(phoneNumberB)] = playerB
                            db["unpairedList"] = unpairedList;
                        else:
                            unpairedList.append(phoneNumberA);
                            Send("Twitship -- Waiting for other players to join :) ... You will be notified when you get paired with another player :D", phoneNumberA)
                            db["unpairedList"] = unpairedList
    else:
        ''' player doesn't exist... time to create!!! :D '''
        playerA = Player(phoneNumberA);
        db[str(phoneNumberA)] = playerA
        Send(playerA.getGrid().printOwnGrid(), phoneNumberA);
        Send("Reply with the coordinate for your Minesweeper (length = 2) followed by whether you want it horizonatal or vertical: ie:D5H for horizontally with the first location being D5 or E7V for a vertical ship with first location being E7", phoneNumberA)

    db.close()

if __name__ == '__main__':
    sys.exit(twitShipMain(phoneNumber = sys.argv[1], message = sys.argv[2]))

