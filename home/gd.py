import random, math, time
import inp

AVATAR = ['▣','▩','❒','▦','⊡']
HP_BAR = ['-cmH-0m','-cmP-0m','-cm:-0m','-cm -0m'],'-bm▮-0m','-bm▯-0m'
Inventory = [['◈',' ','-emx-0m','-em'],['❤',' ','-dmx-0m','-dm'],['⌾',' ','-dmx-0m','-dm'],['◯',' ','-hmx-0m','-hm'],['⍟' ' ','-fmx-0m','-fm'],['♛',' ','-hmx-0m','-hm']]
SwingSwordA = ['|','/','-','\\','|','/','-','\\']
SwingSwordP = lambda x,y:[(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y),(x-1,y-1)]
ArrowsLook = ['↑','↗','→','↘','↓','↙','←','↖']
EnemyVisual = ['ఠ','▴','〠','ಠ']
EnemyHps = [100, 75, 200, 1000]
EnemyVisDis = [6, None, 10, 8]
EnemySpeed = [0.1,0,0.12,0.05]
EnemyAbilities = [None, None, 0, 1]
EnemyDamage = [50, 2, 30, 200]
Enemydrops = [[' ','⌾'],[' ','◯','⍟','↑'],[' ','◈'],['♛']]
EnemydropsChances = [[80,20],[40,45,5,10],[95,5],[100]]
Weapons = ['Sword','Axe']
WeaponDamge = [[10, 20],[15,26],[30,40],[50,65]]
WeaponUp = [[3,0,0],[10,2,0],[20,15,1]],[[4,0,0],[10,3,1],[18,13,2]]

stepDict = lambda x,y,p:random.choices([(x-1,y),(x+1,y),(x,y-1),(x,y+1)],weights=[p/3,1-p,p/3,p/3])[0]
shoot = lambda enemy:Arrows(enemy.x,enemy.y,enemy.direction)
spawn = lambda enemy,cave,t:Enemies(t,cave, x=enemy.x+random.randrange(1,enemy.VisDis),y=enemy.y+random.randrange(1,enemy.VisDis))

class Arrows():
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 0.5
        self.damage = 10
        self.look = ArrowsLook[direction]
    
    def move(self, cave):
        tmpX, tmpY = self.x, self.y
        if self.direction in [0,1,7]:
            self.y -= self.speed
        if self.direction in [3,4,5]:
            self.y += self.speed
        if self.direction in [1,2,3]:
            self.x += self.speed
        if self.direction in [5,6,7]:
            self.x -= self.speed
        if self.x>cave.size*2-1 or self.x<0 or self.y>cave.size-1 or self.y<0:
            self.x, self.y = tmpX, tmpY
        elif cave.cave[round(self.y)][round(self.x)] == '-Cm -0m':
            self.x, self.y = tmpX, tmpY
        cave.cave[round(tmpY)][round(tmpX)] = ' '
        if round(self.x) == cave.x and round(self.y) == cave.y:
            cave.hp -= self.damage
        if cave.scr[round(self.y)][round(self.x)] in SwingSwordA:
            return True

    def draw(self, cave):
        cave.cave[round(self.y)][round(self.x)] = self.look

class Enemies():
    def __init__(self, Etype, cave, x=-1, y=-1):
        self.hp = EnemyHps[Etype]
        self.x, self.y = x, y
        self.VisDis = EnemyVisDis[Etype]
        self.Visual = EnemyVisual[Etype]
        self.speed = EnemySpeed[Etype]
        self.damage = EnemyDamage[Etype]
        self.direction = 0
        self.Etype = Etype
        self.time = time.time()
        while cave.cave[round(self.y)][round(self.x)] != ' ' and x<0  and y<0:
            self.x, self.y = random.randrange(0, cave.size), random.randrange(0, cave.size)
    
    def move(self, cave):
        tmpX = self.x
        tmpY = self.y
        if self.VisDis != None:
            m=1
            if (cave.x-self.x)**2 + (cave.y-self.y)**2 < self.VisDis:
                delX = cave.x-self.x
                delY = cave.y-self.y
                if delY < 0 and abs(delX) < delY/2:self.direction = 0
                elif delX > 0 and abs(delY) < delX/2:self.direction = 2
                elif delX < 0 and abs(delY) < delX/2:self.direction = 6
                elif delY > 0 and abs(delX) < delY/2:self.direction = 4
                elif delX > 0 and delY < 0:self.direction = 1
                elif delX > 0 and delY > 0:self.direction = 3
                elif delX < 0 and delY > 0:self.direction = 5
                elif delX < 0 and delY < 0:self.dirction = 7
                if self.Etype == 2 and time.time()-self.time > 1:
                    cave.arrows.append(shoot(self))
                    self.time = time.time()
                elif self.Etype == 3 and time.time()-self.time > 2:
                    cave.enemies.append(spawn(self, cave, random.choices([0,2,3],weights=[48,48,4])[0]))
                    cave.enemies.append(spawn(self, cave, random.choices([0,2,3],weights=[48,48,4])[0]))
                    self.time = time.time()
            else:
                possibi = [-1,0,1]
                self.direction += random.choice(possibi)
                self.direction %= 8
            self.x+=self.speed*[0,1,1,1,0,-1,-1,-1][self.direction]
            self.y+=self.speed*[-1,-1,0,1,1,1,0,-1][self.direction]
            if self.x>cave.size*2-1 or self.x<0 or self.y>cave.size-1 or self.y<0:
                self.x, self.y = tmpX, tmpY
            elif cave.cave[round(self.y)][round(self.x)] not in ' '+self.Visual+''.join(ArrowsLook):
                self.x, self.y = tmpX, tmpY
            cave.cave[round(tmpY)][round(tmpX)] = ' '
            if round(self.x) == cave.x and round(self.y) == cave.y and time.time()-self.time>1:
                cave.hp -= self.damage
                self.time = time.time()
        elif abs(self.x-cave.x)<2 and abs(self.y-cave.y)<2:
            cave.hp -= self.damage
        if cave.scr[round(self.y)][round(self.x)] in SwingSwordA:
            self.hp -= cave.damage
            self.x, self.y = tmpX, tmpY
        if self.hp < 1:
            return True

    def draw(self, cave):
        cave.cave[round(self.y)][round(self.x)] = self.Visual
    
    def delete(self, cave):
        cave.cave[round(self.y)][round(self.x)] = random.choices(Enemydrops[self.Etype],weights=EnemydropsChances[self.Etype])[0]

class Cave():
    def __init__(self, size):
        self.avatar = random.choice(AVATAR)
        self.size = size
        self.cave = self.genMaze(size)
        self.x, self.y = 0,0
        self.stuff = []
        self.arrows = []
        self.treasure = []
        self.weapon = random.random() > 0.5
        self.level = 1
        self.enemies = [self.ScatterEnemies(1) for i in range(6)] + [self.ScatterEnemies(1) for i in range(10)] + [self.ScatterEnemies(2) for i in range(2)] + [self.ScatterEnemies(3)]
        self.hp = 1000
        self.damage = WeaponDamge[self.level-1][self.weapon]
        self.t = 0
        self.swordFrame = 0
        self.swingSword = False
        self.swingSwordPulse = False
        self.time = time.time()
        self.VisDis = 10
        self.ScatterTreasure(10)
        while self.cave[self.y][self.x] != ' ':
            self.x, self.y = random.randrange(0, size), random.randrange(0, size)
        self.scr = [[x for x in y] for y in self.cave]

    def genMaze(self, size):
        maze = [[' ']*(2*size) for i in range(size)] 
        solution = [(0,random.randrange(1,size-1))]
        while solution[-1][0] != size*2-1:
            prob = 1-len(solution)/(size*1000)
            nextSq = stepDict(*solution[-1],prob)
            while any([nextSq[0]<1,nextSq[1]>size-1,nextSq[1]<1]):
                nextSq = stepDict(*solution[-1],prob)
            solution.append(nextSq)
        mazeLst = []
        for i in maze:
            mazeLst+=i
        for y in range(size):
            for x in range(size*2):
                if (x,y) in solution:
                    maze[y][x] = ' '
                else:
                    c = 0.2*mazeLst.count('-Cm -0m')/len(mazeLst)
                    maze[y][x] = random.choices([' ','-Cm -0m'],weights=[c,1-c])[0]
        return maze
    
    def ScatterTreasure(self, num=1):
        x,y = 0,0
        for i in range(num):
            while self.cave[y][x] != ' ' or (x-self.x)**2 + (y-self.y)**2 < self.VisDis+1:
                x, y = random.randrange(0, self.size), random.randrange(0,self.size)
            t = random.choices(['❤','◈'],weights=[0.99,0.01])[0]
            self.treasure.append((x,y,t))
            self.cave[y][x] = t

    def ScatterEnemies(self, t):
        return Enemies(t, self)

    def move(self, key):
        if (key == inp.UP or key == 'w') and self.y > 1 and self.cave[self.y-1][self.x] in ' ❤◈⍟♛◯⌾↑↗→↘↓↙←↖':
            self.y -= 1
        if (key == inp.DOWN or key == 's') and self.y < self.size-2 and self.cave[self.y+1][self.x] in ' ❤◈⍟◯♛⌾↑↗→↘↓↙←↖':
            self.y += 1
        if (key == inp.LEFT or key == 'a') and self.x > 1 and self.cave[self.y][self.x-1] in ' ❤◈⍟◯♛⌾↑↗→↘↓↙←↖':
            self.x -= 1
        if (key == inp.RIGHT or key == 'd') and self.x < 2*self.size-2 and self.cave[self.y][self.x+1] in ' ❤◈⍟◯⌾♛↑↗→↘↓↙←↖':
            self.x += 1
        if key == inp.SPACE and time.time() - self.time > 2:
            self.swordPos = SwingSwordP(self.x, self.y)
            self.swingSword = True
            self.swingSwordPulse = True
            if not self.swingSword:
                self.time = time.time()
        if key == 'e' and '❤' in self.stuff:
            self.stuff.remove('❤')
            self.hp = min(1000, self.hp + 100)
        if key == 'u' and '⍟' in self.stuff:
            if '⌾' in self.stuff and self.stuff.count('⌾') >= WeaponUp[self.weapon][self.level-1][0]:
                if self.level > 1:
                    if '◯'in self.stuff and self.stuff.count('◯') >= WeaponUp[self.weapon][self.level-1][1]:
                        if self.level > 2:
                            if '◈'in self.stuff and self.stuff.count('◈') >= WeaponUp[self.weapon][self.level-1][2]:
                                if self.level == 3:
                                    self.stuff.remove('⍟')
                                    for _ in range(WeaponUp[self.weapon][self.level-1][0]):self.stuff.remove('⌾')
                                    for _ in range(WeaponUp[self.weapon][self.level-1][1]):self.stuff.remove('◯')
                                    for _ in range(WeaponUp[self.weapon][self.level-1][2]):self.stuff.remove('◈')
                                    self.level = 4
                                    self.damage = WeaponDamge[self.level-1][self.weapon]
                        else:
                            self.stuff.remove('⍟')
                            for _ in range(WeaponUp[self.weapon][self.level-1][0]):self.stuff.remove('⌾')
                            for _ in range(WeaponUp[self.weapon][self.level-1][1]):self.stuff.remove('◯')
                            self.level = 3
                            self.damage = WeaponDamge[self.level-1][self.weapon]
                else:
                    self.stuff.remove('⍟')
                    for _ in range(WeaponUp[self.weapon][self.level-1][0]):self.stuff.remove('⌾')
                    self.level = 2
                    self.damage = WeaponDamge[self.level-1][self.weapon]
        if self.cave[self.y][self.x] in '❤◈⍟◯⌾♛':
            if self.cave[self.y][self.x] in '❤◈':
                self.treasure.remove((self.x,self.y,self.cave[self.y][self.x]))
            self.stuff.append(self.cave[self.y][self.x])
            self.cave[self.y][self.x] = ' '
            self.ScatterTreasure()
        for e in self.enemies:
            if e.move(self):
                e.delete(self)
                self.enemies.remove(e)
                self.enemies.append(self.ScatterEnemies(random.choices([0,1,2,3],[30,30,25,5])[0]))
        for a in self.arrows:
            if a.move(self) or (round(a.x) == self.x and round(a.y) == self.y):
                self.arrows.remove(a)
        self.t += 1

    def draw(self, screen):
        for e in self.enemies:
            e.draw(self)
        for a in self.arrows:
            a.draw(self)
        if self.swingSwordPulse:
            self.swordFrame = self.t
            self.swingSwordPulse = False
        self.scr = [[x for x in y] for y in self.cave]
        self.scr[self.y][self.x] = self.avatar
        if self.swingSword:
            x,y = self.swordPos[self.t//(2-self.weapon) %8]
            self.scr[y][x] = SwingSwordA[self.t//(2-self.weapon) %8]
            self.swingSword = self.t - self.swordFrame < 16
        for y in range(self.size):
            for x in range(self.size*2):
                if ((x-self.x)/2)**2 + (y-self.y)**2 > self.VisDis:
                    self.scr[y][x] = "-Am -0m"
        hpTxt = HP_BAR[0] + [HP_BAR[1] for i in range(round(self.hp/100))] + [HP_BAR[2]]*int(self.hp%100 < 50 and self.hp%100 > 0)
        self.scr[0] = list(hpTxt) + self.scr[0][len(hpTxt):]
        weapTxt = 'Weapon: ' + Weapons[self.weapon] + ' Level: ' + str(self.level)
        self.scr[1] = list(weapTxt) + self.scr[1][len(weapTxt):]
        invTxt = [Inventory[i][:2]+[Inventory[i][2]+j+'-0m' for j in str(self.stuff.count(Inventory[i][0]))] for i in range(len(Inventory))]
        for i in range(len(Inventory)):self.scr[i+2] = invTxt[i] + self.scr[i+2][len(invTxt[i]):]
        screen.load([''.join(i) for i in self.scr])

