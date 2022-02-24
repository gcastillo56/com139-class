"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""


import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import os

totalFigures = 0
Generations = 0
ON = 255
OFF = 0
vals = [ON, OFF]
class Entities:
    def __init__(self):
        # Still Lifes
        self.Block = np.array([
            [255,    255],
            [255,  255]
        ])
        self.Beehive = np.array([
            [0,    255, 255, 0],
            [255,  0, 0, 255],
            [0,  255, 255, 0]
        ])
        self.Loaf = np.array([
            [0,    255, 255, 0],
            [255,  0, 0, 255],
            [0,  255, 0, 255],
            [0,  0, 255, 0]
        ])
        self.Boat = np.array([
            [255,    255, 0],
            [255,  0, 255],
            [0,  255, 0]
        ])
        self.Tub = np.array([
            [0,    255, 0],
            [255,  0, 255],
            [0,  255, 0]
        ])
        # Oscilators
        self.BlinkerV1 = np.array([
            [255, 255, 255]
        ])
        self.BlinkerV2 = np.array([
            [255],
            [255],
            [255]
        ])
        self.ToadV1 = np.array([
            [0,    0, 255, 0],
            [255,  0, 0, 255],
            [255,  0, 0, 255],
            [0,  255, 0, 0]
        ])
        self.ToadV2 = np.array([
            [0,  0, 0, 0],
            [0,  255, 255, 255],
            [0,  255, 255, 0],
            [255,  0, 0, 0]
        ])
        self.BeaconV1 = np.array([
            [255, 255, 0, 0],
            [255, 255, 0, 0],
            [0,  0, 255, 255],
            [0,  0, 255, 255]
        ])
        self.BeaconV2 = np.array([
            [255, 255, 0, 0],
            [255, 0, 0, 0],
            [0,  0, 0, 255],
            [0,  0, 255, 255]
        ])
        # SpaceShips
        self.GliderV1 = np.array([
            [0,    0, 255],
            [255,  0, 255],
            [0,  255, 255]
        ])
        self.GliderV2 = np.array([
            [255,  0, 255],
            [0,  255, 255],
            [0,  255, 0]
        ])
        self.GliderV3 = np.array([
            [0,  0, 255],
            [255,  0, 255],
            [0,  255, 255]
        ])
        self.GliderV4 = np.array([
            [255,  0, 0],
            [0,  255, 255],
            [255,  255, 0]
        ])
        self.LightWeightSpaceshipV1 = np.array([
            [255, 0, 0, 255, 0],
            [0, 0,  0,  0, 255],
            [255, 0, 0, 0, 255],
            [0,  255, 255, 255, 255]
        ])
        self.LightWeightSpaceshipV2 = np.array([
            [0, 0, 255, 255, 0],
            [255, 255, 0, 255, 255],
            [255, 255, 255, 255, 0],
            [0, 255, 255, 0, 0]
        ])
        self.LightWeightSpaceshipV3 = np.array([
            [0, 255, 255, 255, 255],
            [255, 0, 0, 0, 255],
            [0, 0, 0, 0, 255],
            [255, 0, 0, 255, 0]
        ])
        self.LightWeightSpaceshipV4 = np.array([
            [0, 255, 255, 0, 0],
            [255, 255, 255, 255, 0],
            [255, 255, 0, 255, 255],
            [0, 0, 255, 255, 0]
        ])
        return

    def GetEntities(self) -> list:
        ent = []

        ent.append(("LightWeightSpaceshipV1",
                    self.LightWeightSpaceshipV1, True))
        ent.append(("LightWeightSpaceshipV2",
                    self.LightWeightSpaceshipV2, True))
        ent.append(("LightWeightSpaceshipV3",
                    self.LightWeightSpaceshipV3, True))
        ent.append(("LightWeightSpaceshipV4",
                    self.LightWeightSpaceshipV4, True))

        ent.append(("GliderV1", self.GliderV1, True))
        ent.append(("GliderV2", self.GliderV2, True))
        ent.append(("GliderV3", self.GliderV3, True))
        ent.append(("GliderV4", self.GliderV4, True))

        ent.append(("BeaconV1", self.BeaconV1, True))
        ent.append(("BeaconV2", self.BeaconV2, True))

        ent.append(("ToadV1", self.ToadV1, True))
        ent.append(("ToadV2", self.ToadV2, True))

        ent.append(("BlinkerV1", self.BlinkerV1, False))
        ent.append(("BlinkerV2", self.BlinkerV2, False))

        ent.append(("Block", self.Block, False))
        ent.append(("Beehive", self.Beehive, True))
        ent.append(("Loaf", self.Loaf, True))
        ent.append(("Boat", self.Boat, True))
        ent.append(("Tub", self.Tub, True))

        return ent




            

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum,img, grid, N ,LogFile,ite):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    # TODO: Implement the rules of Conway's Game of Life
    global Generations 
    if Generations < ite:
        Generations = Generations + 1
        for x in range(1, N-1):
            for y in range(1, N-1):
                accum_cel = grid[x-1,y-1] + grid[x-1,y] + grid[x-1,y+1] + grid[x,y-1] + grid[x,y+1] + grid[x+1,y-1] + grid[x+1,y] + grid[x+1,y+1]
                accum_cel /= 255
                if grid[x,y] == 255:
                    if accum_cel == 2 or accum_cel == 3:
                        pass
                    else:
                        newGrid[x,y] = 0
                else:
                    if accum_cel == 3:
                        newGrid[x,y] = 255
        
    else:
        LogFile.close()
        sys.exit()
    # update data
    validateFigures(newGrid,LogFile)
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def CheckObject(index: int, pattern: np.array, patternName: str,  tempCheckerGrid: np.array,LogFile):
        global totalFigures
        tmpCheck = _FindIfPatternExists(
            tempCheckerGrid, pattern)
        if tmpCheck[0]:
            counter = 0

            def CheckAndRemovePattern(grid: np.array, counter: int, pattern: np.array, upper_left: list) -> (np.array, int):
                global totalFigures
                for ul_item in upper_left:
                    ul_row = ul_item[0]
                    ul_col = ul_item[1]
                    b_rows, b_cols = pattern.shape
                    a_slice = grid[ul_row: ul_row + b_rows,
                                       :][:, ul_col: ul_col + b_cols]
                    if a_slice.shape != pattern.shape:
                        continue

                    if (a_slice == pattern).all():
                        counter += 1
                        grid[ul_row: ul_row + b_rows,
                                :][:, ul_col: ul_col + b_cols] = 0

                return grid, counter

            res = CheckAndRemovePattern(
                tempCheckerGrid, counter, pattern, tmpCheck[1])
            tempCheckerGrid, counter = res
            totalFigures = totalFigures + counter
           
            if counter != 0:   
                LogFile.write(
                    f"|\t> {patternName}(s) \t| {counter} |  |\n")
    
def validateFigures(newGrid,LogFile):
    tempCheckerGrid = newGrid.copy()
    LogFile.write(f"Iteration: {Generations}\n---------------------------------------------------\n")
    LogFile.write(f"|                               | Count | Percent |\n---------------------------------------------------\n")
    print(f"{Generations} ", end="")
    p = Entities()
    ents = p.GetEntities()
    global totalFigures
    i = 0
    for (name, pattern, rot) in ents:
        CheckObject(i, pattern, name, tempCheckerGrid,LogFile)
        if rot:
            right = np.rot90(pattern)
            down = np.rot90(right)
            left = np.rot90(down)
            CheckObject(rot, right, name
                            , tempCheckerGrid,LogFile)
            CheckObject(rot, down, name , tempCheckerGrid,LogFile)
            CheckObject(rot, left, name , tempCheckerGrid,LogFile)
            i += 1
            
    LogFile.write(
                f"---------------------------------------------------\n| Total                          |   {totalFigures}   |        |\n---------------------------------------------------\n")
    totalFigures = 0        

def _Check( a, b, upper_left):
        ul_row = upper_left[0]
        ul_col = upper_left[1]
        b_rows, b_cols = b.shape
        a_slice = a[ul_row: ul_row + b_rows, :][:, ul_col: ul_col + b_cols]
        if a_slice.shape != b.shape:
            return False
        return (a_slice == b).all()

def _FindIfPatternExists(big_array, small_array) -> (bool, np.array):
    upper_left = np.argwhere(big_array == small_array[0, 0])
    for ul in upper_left:
        if _Check(big_array, small_array, ul):
            return (True, upper_left)
    else:
        return (False, None)

def fillGrid(grid, file):
    with open("{0}\{1}".format(os.getcwd(),file),'r') as f:
        lines_after_2 = f.readlines()[2:]
    
    coords = [i.strip() for i in lines_after_2]
    for i in coords:
        coord = i.split(" ")
        grid[int(coord[1]),int(coord[0])] = 255
    return grid
# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments
    parser.add_argument("-n","--number" ,type=int, help="Size of universe")
    parser.add_argument("-i", "--interval", type=int)
    parser.add_argument("-f", "--file", type=str)
 
    args = parser.parse_args()
    # set grid size
      
    # set animation update interval
    updateInterval = 20

    # declare grid
    grid = np.array([])

    try:
        os.remove("analysis.txt")
    except:
        pass
    LogFile = open("analysis.txt", "a+")

    if args.file:
        print("Setting initial configuration with file {0}".format(args.file))
        with open("{0}\{1}".format(os.getcwd(),args.file),'r') as f:
                first_2_lines = f.readlines()[:2]
        coords = [i.strip() for i in first_2_lines]
        a = (int(coords[0].split(" ")[0]),int(coords[0].split(" ")[1]))
        print(a[0])
        ite = int(coords[1]) 
        print(ite) 
        grid = np.zeros(a, dtype=int)
        grid = fillGrid(grid, args.file)
        fig, ax = plt.subplots()
        img = ax.imshow(grid, interpolation='nearest')
        ani = animation.FuncAnimation(fig, update, fargs=(img, grid, a[0],LogFile,ite,),
                                      frames = ite,
                                      interval=100,
                                      save_count=5)
        
        plt.show()
    else:
        N = args.number
        ite = args.interval  
        print("Setting grid of {0} x {0}".format(N))
        print("Update interval = {0}".format(updateInterval))
        # populate grid with random on/off - more off than on
        grid = randomGrid(N)
        # Uncomment lines to see the "glider" demo
        #grid = np.zeros(N*N).reshape(N, N)
        #addGlider(1, 1, grid)

        # set up animation

        fig, ax = plt.subplots()
        img = ax.imshow(grid, interpolation='nearest')
        ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,LogFile,ite,),
                                      frames = ite,
                                      interval=updateInterval,
                                      save_count=5)
        plt.show()
    

# call main
if __name__ == '__main__':
    main()