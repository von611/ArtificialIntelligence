import random
import re
import time
from string import ascii_lowercase


class Mines:
    def __init__(self, gridsize, numberofmines):
        self.flags = []
        self.__currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]
        self.__fail = False;
        self.__currcell = (0,0)
        emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]
        self.__mines = self.__getmines(emptygrid, self.__currcell, numberofmines)        
        for i, j in self.__mines:
            emptygrid[i][j] = 'X'
        self.__grid = self.__getnumbers(emptygrid)                

        
    def __getrandomcell(self, grid):
        gridsize = len(grid)

        a = random.randint(0, gridsize - 1)
        b = random.randint(0, gridsize - 1)

        return (a, b)

    def __getneighbors(self, grid, rowno, colno):
        gridsize = len(grid)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                    neighbors.append((rowno + i, colno + j))
                    
        return neighbors
    

    def __getmines(self, grid, start, numberofmines):
        mines = []
        neighbors = self.__getneighbors(grid, *start)

        for i in range(numberofmines):
            cell = self.__getrandomcell(grid)
            while cell == start or cell in mines or cell in neighbors:
                cell = self.__getrandomcell(grid)
            mines.append(cell)
            
        return mines
    

    def __getnumbers(self, grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != 'X':
                    values = [grid[r][c] for r, c in self.__getneighbors(grid, rowno, colno)]
                    grid[rowno][colno] = str(values.count('X'))
                    
        return grid
    
    
    def __showcells(self, rowno, colno):        
        if self.__currgrid[rowno][colno] != ' ':
            return

        self.__currgrid[rowno][colno] = self.__grid[rowno][colno]

        if self.__grid[rowno][colno] == '0':
            for r, c in self.__getneighbors(self.__grid, rowno, colno):
                if self.__currgrid[r][c] != 'F':
                    self.__showcells(r, c)
                    

    def __showgrid(self, grid):
        gridsize = len(grid)
        horizontal = '   ' + (4 * gridsize * '-') + '-'
        toplabel = '     '

        for i in range(gridsize):
            if i < 10:
                toplabel = toplabel + str(i) + '   '
            else:
                toplabel = toplabel + str(i) + '  '

        print(toplabel + '\n' + horizontal)

        for idx, i in enumerate(grid):
            row = '{0:2} |'.format(idx)
            for j in i:
                row = row + ' ' + j + ' |'

            print(row + '\n' + horizontal)

        print('')  

    def checkcell(self, cell):
        if not self.__fail:            
            self.__currcell = cell
            if self.__grid[cell[0]][cell[1]] == 'X':
                self.__fail = True;
                
        return self.__currgrid

    def showcurrent(self):        
        self.__showcells(*self.__currcell)
        self.__showgrid(self.__currgrid)

    
    def isfail(self):
        return self.__fail


    def checkmines(self):
        if set(self.__mines) == set(self.flags):
            return True
        else:
            return False


def eqBuild(row,col):
    l = []
    l.append((row-1,col-1))
    l.append((row-1,col))
    l.append((row-1,col+1))
    l.append((row,col+1))
    l.append((row,col-1))
    l.append((row+1,col-1))
    l.append((row+1,col))
    l.append((row+1,col+1))
    return l
def findCell(tr):
    largest = 0
    cell = None
    for i in tr:
        if tr[i] > largest:
            largest = tr[i]
            cell = i
    return cell
        
class Cell:
    def __init__(self, coord, value):
        self.coord = coord
        self.value = value
        
if __name__ == '__main__':
    gridsize = 16
    n_mines = 40
    sweeper = Mines(gridsize, n_mines)
    sweeper.showcurrent()
    
    predictCell = None
    
    while sweeper.isfail() == False:
        diction = {}
        knowledge = {}
        eq = {}
        grid = sweeper.checkcell((0,0))
        for row in range(len(grid)):
            for col in range(len(grid)):

                diction[(row,col)] = grid[row][col]
                if grid[row][col] != '0' and grid[row][col] != ' ':
                    eq[(row,col)] = eqBuild(row,col)

        for i in eq: #elminating what cells cannot be mines such as cell that already has a numbers or out of bound
            temp = []
            for j in eq[i]:

                if j in diction and diction[j] == ' ':

                    temp.append(j)


            eq[i] = temp
        #print(diction)
        for i in eq:
            knowledge[Cell(i,int(diction[i]))] = eq[i]
            #print(i, eq[i])
        safeCell = []
        mineCell = []
        tr = {} #Use when there is no safe cell to move , use to predict possible mine spot 
        if predictCell != None:
            mineCell.append(predictCell)
        #print("before subtracting")
        for i in knowledge:
            
            #print(i.value, knowledge[i])
            
            if i.value == len(knowledge[i]): # this means they have to be mines
                for j in knowledge[i]:
                    if j not in sweeper.flags:
                        mineCell.append(j)
                        
        #print("temporary minecell",mineCell)
        for i in knowledge:
            temp = []
            for j in knowledge[i]:
                if j not in sweeper.flags:
                    if j not in tr: # filling in tr
                        tr[j] = 1
                    else:
                        tr[j] += 1
                if j in sweeper.flags: # determining cells that doesn't have mines
                    i.value -=1
                else:
                    temp.append(j)
            knowledge[i] = temp
        for i in mineCell:
            if i not in sweeper.flags:
                sweeper.flags.append(i) #add to mines
        for i in knowledge:
            #print(str(i.value) +":"+str(i.coord), knowledge[i])
            if i.value == 0: #this means all cell is safe if there are any
                for j in knowledge[i]:
                    if j not in safeCell:
                        safeCell.append(j)
                        #grid = sweeper.checkcell(j)
                        #sweeper.showcurrent()
        #print("safe cell",safeCell)
        for i in safeCell:
            grid = sweeper.checkcell(i)
            print("Checking cell",i)
            sweeper.showcurrent()
            if sweeper.isfail():
                break
            
            
        #print("tracker",tr)
        if len(safeCell) == 0: #cannot find a guarantee safe cell
            #print ("largest cell",findCell(tr))
            cell = findCell(tr)
            if cell != None and cell not in sweeper.flags:
                print("Predict mine cell",cell)
                sweeper.flags.append(cell)
                predictCell = cell
            #sweeper.showcurrent()
       
        #print("mine cell", mineCell)
        
        print("sweeper mines cell",sweeper.flags)
        print("number of mines in sweeper",len(sweeper.flags))
        if sweeper.checkmines():
            print("Solved")
            sweeper.showcurrent()
            break