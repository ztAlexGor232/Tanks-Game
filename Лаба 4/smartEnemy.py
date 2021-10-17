import random
from tank import Tank
from algorithms import SA
from usefulStuffs import*
#from map import Map

class SmartEnemy(Tank):

    def __init__(self, x, y):
        Tank.__init__(self, x, y, player = 2)

        self.goal = None
        self.path = []


    def setGoal(self, enemies, map, player):
        self.goal = (player.x // 100, player.y // 100)
        self.path = SA.search(enemies, map, self, Tank(self.goal[0], self.goal[1]), 1)
        

    def processShot(self, bullets, player, map):
        dir = checkShotPossibility(self, player, map)

        if dir != Direction.NONE:
            self.isMove = False

            if self.direction != dir:
                self.direction = dir
                

            if self.standTime > random.randint(5, 50):
                t = self.shoot()
                if not t == None:
                    bullets.append(t)
            
            return

        self.isMove = True



    def processTankByAI(self, bullets, win, map, enemies, player):
        self.recalcKd()

        if self.goal is not None and (self.goal[0] * 100 == self.x and self.goal[1] * 100 == self.y):
            self.goal = None
            return
        
        self.setGoal(enemies, map, player)

        self.processShot(bullets, player, map)

        if self.isMove:
            if len(self.path) > 0:
                self.standTime = 0

                if self.path[-1] != self.goal:
                    self.path.pop()
                
                if self.y % 100 == 0 and self.x > self.path[-1][0] * 100:
                    self.moveLeft(map, enemies, player)
                elif self.y % 100 == 0 and self.x < self.path[-1][0] * 100:
                    self.moveRight(win, map, enemies, player) 
                elif self.x % 100 == 0 and self.y > self.path[-1][1] * 100:
                    self.moveUp(map, enemies, player) 
                elif self.x % 100 == 0 and self.y < self.path[-1][1] * 100:
                    self.moveDown(win, map, enemies, player)
        else:
            self.standTime += 1

        
    def processTank(self, bullets, win, map, enemies, player):
        self.processTankByAI(bullets, win, map, enemies, player)


    def processTankForMinimax(self, bullets, win, map, enemies, player):
        self.recalcKd()
        self.processShot(bullets, player, map)

        if self.isMove:
            if len(self.path) > 0:
                self.standTime = 0

                if self.path[-1] != self.goal:
                    self.path.pop()
                
                if self.y % 100 == 0 and self.x > self.path[-1][0] * 100:
                    self.moveLeft(map, enemies, player)
                elif self.y % 100 == 0 and self.x < self.path[-1][0] * 100:
                    self.moveRight(win, map, enemies, player) 
                elif self.x % 100 == 0 and self.y > self.path[-1][1] * 100:
                    self.moveUp(map, enemies, player) 
                elif self.x % 100 == 0 and self.y < self.path[-1][1] * 100:
                    self.moveDown(win, map, enemies, player)
        else:
            self.standTime += 1