from grid import *
from ship import *

class Player:
    def __init__(self, phoneNumber):
        self._shipsPlaced = 0
        self._grid = Grid()
        self._shipStatus = [1, 1, 1, 1, 1]
        self._shipSize = [2, 3, 3, 4, 5]
        self._shipChar = ['M', 'S', 'F', 'B', 'A']
        self._shipName = ["Minesweeper", "Submarine", "Frigate", "Battleship", "Aircraft Carrier"]
        self._shipArray = [];
        self._id = phoneNumber;
        self._otherID = 0;
        self._isTurn = 0;

    def setTurn(self, isTurn):
        self._isTurn = isTurn;

    def getShipsPlaced(self):
        return self._shipsPlaced

    def getNextShipToPlace(self):
        return self._shipName[self._shipsPlaced], self._shipSize[self._shipsPlaced]

    def placeShip(self, coord, horizontal):
        if(horizontal):
            self._shipArray.append(Ship(self._shipSize[self._shipsPlaced], 1, self._shipChar[self._shipsPlaced], self._grid));
            if(not self._shipArray[self._shipsPlaced].placeShip(coord)):
                self._shipsPlaced += 1;
                return 0
            else:
                return -1
        else:
            self._shipArray.append(Ship(1, self._shipSize[self._shipsPlaced], self._shipChar[self._shipsPlaced], self._grid));
            if(not self._shipArray[self._shipsPlaced].placeShip(coord)):
                self._shipsPlaced += 1;
                return 0
            else:
                return -1

    def isTurn(self):
        return self._isTurn

    def getGrid(self):
        return self._grid;

    def setOtherID(self, id):
        self._otherID = id;

    def getOtherID(self):
        return self._otherID;

    def getShipArray(self):
        return self._shipArray;

    def getShipChar(self):
        return self._shipChar;

    def checkShipStatus(self):
        return (1 in self._shipStatus);

    def shoot(self, coord):
        stringArray = []
        data = self._grid.getData(coord[0], coord[1])
        if(data != 0 and data != 'X' and data != '#'):
            self._grid.insertData('X', coord[0], coord[1])
            stringArray.append("Hit");
            if(not self._grid.stillAlive(data)):
                stringArray.append("\nYou sunk my " + self._shipName[self._shipChar.index(data)] + "!!")
                self._shipStatus[self._shipChar.index(data)] = 0
        elif(data == 0):
            self._grid.insertData('#', coord[0], coord[1])
            stringArray.append("Miss");
        else:
            return -1
        myString = '\n';
        return myString.join(stringArray);
