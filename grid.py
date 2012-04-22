class Grid:

    def __init__(self):
        self.data = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
	    [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
	    [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

    def mergeData(self, otherData):
        for y in range(9):
            for x in range(9):
                if (otherData[y][x] != '\0'):
                    _data[y][x] = otherData[y][x];

    def insertData(self, otherData, otherDataX, otherDataY, otherDataWidth = 1, otherDataHeight = 1):
        for y in range(otherDataY, otherDataY + otherDataHeight):
            for x in range(otherDataX, otherDataX + otherDataWidth):
                self.data[y][x] = otherData[otherDataY - y][otherDataX - x];

    def getData(self, x, y):
        print "X:", x, "Y:", y
	return self.data[y][x];

    def stillAlive(self, data):
        for y in self.data:
            for x in y:
                if(x == data):
                    return 1;
        return 0

    def printOwnGrid(self):
        stringArray = ['You:\n '];
        for i in range(9):
            stringArray.append(str(i+1));
        stringArray.append("\n");
        j=ord('A')
        for y in self.data:
            stringArray.append(chr(j))
            j+=1
            for x in y:
                stringArray.append(str(x));
            stringArray.append("\n");
        myString = ''
        return myString.join(stringArray)

    def printOpponentGrid(self):
        stringArray = ['Them:\n '];
        for i in range(9):
            stringArray.append(str(i+1))
        stringArray.append("\n");
        j=ord('A')
        for y in self.data:
            stringArray.append(chr(j))
            j+=1
            for x in y:
                if(x == '0' or x == 0 or x == 'X' or x == '#'):
                    stringArray.append(str(x));
                else:
                    stringArray.append("0");
            stringArray.append("\n")
        myString = '';
        return myString.join(stringArray);
