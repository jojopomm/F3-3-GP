import random
import inp

g = 0.7

def readPic(directory):
    '''
    ani: Animation list (this is what will be returned)
    pic: Temporary storage for each frame
    reads from any file (txt recommended)
    / means end of frame -> ani.append(pic)
    // means end of file
    '''
    ani=[]
    pic=[]
    line=''
    with open(directory, 'rb') as f:
        while '//' not in line:
            line=f.readline().decode('utf-8')
            if '/' not in line:
                pic.append(line.strip('\n'))
            else:
                ani.append(pic)
                pic=[]
    return ani[:-1]

upPicT = readPic("system/flappyBirdGraphics/pipe.txt")[0]
downPicT = readPic("system/flappyBirdGraphics/pipe.txt")[1]

class Bird():
    def __init__(self):
        self.char = readPic("system/flappyBirdGraphics/bird.txt")[0]
        self.size = (len(self.char[0]),len(self.char))
        self.x = 8-self.size[0]//2
        self.y = 16-self.size[1]//2
        self.Press = 0.8
        self.Yspeed = 0

    def draw(self, screen):
        self.pos = (int(self.x),int(self.y))
        screen.load(self.char, align=self.pos)
    
    def move(self, key, deltaTime, screen):
        if key == inp.SPACE and self.y > 1 and self.Yspeed < 4:
            self.Yspeed = self.Press
        if self.y < 1:
            self.y = 1
            self.Yspeed = 0
        self.Yspeed -= g*deltaTime
        self.y -= self.Yspeed
        if self.y > screen.size-2:
            return True
        return False

class Pipe():
    def __init__(self, x=0):
        self.Xspeed = 4
        self.gap = 8
        self.x = 64 - x
        self.y = 0
        self.rand = random.randrange(6,17-self.gap//2)
        self.pic = upPicT[self.rand + 1:] + [' '*len(upPicT[0]) for i in range(self.gap)] + downPicT[:30-self.gap-len(upPicT[self.rand + 1:])]
        #print(len(self.pic),self.rand)
        #print('\n'.join(self.pic),end='\n\n')
        self.pipeSizeT = (len(self.pic[0]),len(self.pic))
        self.pos = (int(self.x-self.pipeSizeT[0]//2),self.y)
    
    def draw(self, screen):
        self.pos = (int(self.x-self.pipeSizeT[0]//2),self.y)
        if self.pos[0]< 1:
            return 1
        tmp = [i[0:64-self.pos[0]] for i in self.pic]
        screen.load(tmp, align=self.pos)
        return 0
    
    def move(self, deltaTime):
        self.x -= self.Xspeed*deltaTime

