import pygame
import sys
from tkinter import messagebox, Tk



columns = int(input("Input length of grid: "))
rows = int(input("Input height of grid: "))

squareW = 20
squareH = 20

winH = rows * squareH
winW = columns * squareW
window = pygame.display.set_mode((winW, winH))


class Square:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.start = False
        self.target = False
        self.wall = False
        self.queued = False
        self.visited = False
        self.neighbors = []
        self.edgeTo = None

    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x * squareW, self.y * squareH, squareW - 3, squareH - 3))

    def set_neighbors(self):
        if self.x>0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.x <columns - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.y>0:
            self.neighbors.append(grid[self.x][self.y-1])
        if self.y <rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])

#Setup Square Grid and neighbors
grid = []
queue = []
path = []
for x in range(columns):
    arr = []
    for y in range(rows):
        arr.append(Square(x,y))
    grid.append(arr)
for x in range(columns):
    for y in range(rows):
        grid[x][y].set_neighbors()


def main():
    target_set = False
    start_search = False
    searching = True
    target_square = None
    start_set = False

    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                print("Pygame has been quit")
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if(event.buttons[1] and not start_set):
                    start = grid[x//squareW][y//squareH]
                    start.start = True
                    start.visited = True
                    queue.append(start)
                    start_set = True
                if event.buttons[0] and not grid[x//squareW][y//squareH].start and not grid[x//squareW][y//squareH].target:
                    grid[x//squareW][y//squareH].wall = True
                if (event.buttons[2] and not target_set):
                    target = grid[x//squareW][y//squareH]
                    target.target = True
                    target_set = True
            if (event.type == pygame.KEYDOWN and target_set):
                start_search = True

        if start_search:
            if(len(queue)>0 and searching):
                current = queue.pop(0)
                current.visited = True
                if current == target:
                    searching = False
                    while current.edgeTo != start:
                        path.append(current.edgeTo)
                        current = current.edgeTo
                else:
                    for neighbor in current.neighbors:
                        if not neighbor.queued and not neighbor.wall:
                            neighbor.queued = True
                            neighbor.edgeTo = current
                            queue.append(neighbor)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution since it cannot make it to the target")
                    searching = False

        window.fill((0,0,0))
        for x in range(columns):
            for y in range(rows):
                square = grid[x][y]
                square.draw(window, (50, 50, 50))

                if square.queued:
                    square.draw(window, (0, 230, 250))
                if square.visited:
                    square.draw(window, (0, 20, 255))
                if square in path:
                    square.draw(window, (100, 100, 0))
                if square.start:
                    square.draw(window, (255, 0, 0))
                if square.wall:
                    square.draw(window, (255, 255, 255))
                if square.target:
                    square.draw(window, (0, 255, 0))
        pygame.display.flip()
main()
