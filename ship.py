from random import *

class Ship:
    def __init__(self, width, height, char, grid):
        
        self._width = width
        self._height = height
        self._char = char
        self._grid = grid;

    def placeShip(self, coord):
        ''' check for placement conflicts '''
        if (coord[1] + self._height <= 9 and
            coord[0] + self._width <= 9):
            for j in range(coord[1], coord[1] + self._height):
                for i in range(coord[0], coord[0] + self._width):
                    if (not self._grid.getData(i, j)):
                        ''' do nothing '''
                    else:
                        ''' ship conflict exists '''
                        return -1
        else:
            ''' ship outside of grid '''
            return -1
        self._x = coord[0];
        self._y = coord[1];
        myArray = [];
        for y in range(0, self._height):
            myArray.append([]);
            for x in range(0, self._width):
                myArray[y].append(self._char);
        self._grid.insertData(myArray, self._x, self._y, self._width, self._height);
        return 0;

    def placeRandom(self):
        kill = 1
        while kill:
            seed();
            randX = randint(0,1000000) % 9
            randY = randint(0,1000000) % 9
            kill = 0;
            temp2dList = [[]];

            if (randY + self._height <= 8 and
                randX + self._width <= 8):
                for j in range(randY, randY + self._height):
                    for i in range(randX, randX + self._width):
                        if (not self._grid.getData(i, j)):
                            ''' do nothing '''
                        else:
                            kill = 1
            else:
                kill = 1
        self._x = randX;
        self._y = randY;
        myArray = [];
        for y in range(0, self._height):
            myArray.append([]);
            for x in range(0, self._width):
                myArray[y].append(self._char);
        self._grid.insertData(myArray, self._x, self._y, self._width, self._height);
