import inp
import os

class txtEditor():
    def __init__(self, screen):
        self.cursorPosX = 0
        self.cursorPosY = 0
        self.txt = ['']
        with open(screen.curPath+'/'+screen.fileName, 'r') as f:
            for l in f:
                self.txt += [l]
        self.lastTxt = self.txt
    
    def inputting(self, key, screen):
        if key == inp.ENTER:
            if self.cursorPosY < len(self.txt):
                self.txt = self.txt[:self.cursorPosY] + [self.txt[self.cursorPosY][:self.cursorPosX]] + [self.txt[self.cursorPosY][self.cursorPosX:]] + self.txt[self.cursorPosY+1:]
            else:
                self.txt = self.txt[:self.cursorPosY] + [self.txt[self.cursorPosY][:self.cursorPosX]] + [self.txt[self.cursorPosY][self.cursorPosX:]]
        elif key == inp.UP:
            self.cursorPosY = max(self.cursorPosY-1,0)
        elif key == inp.DOWN:
            self.cursorPosY = min(self.cursorPosY+1,len(self.txt))
        elif key == inp.LEFT:
            if self.cursorPosX > 0:
                self.cursorPosX-=1
            else:
                self.cursorPosY = max(self.cursorPosY-1,0)
                self.cursorPosX = len(self.txt[self.cursorPosY])-1
        elif key == inp.RIGHT:
            if self.cursorPosX < len(self.txt[self.cursorPosY])-1:
                self.cursorPosX-=1
            else:
                self.cursorPosY = max(self.cursorPosY-1,0)
                self.cursorPosX = len(self.txt[self.cursorPosY])-1
    
    def save(self, key, directory):
        if key == 'CS' or self.lastTxt == self.txt:
            if os.path.exists(directory):
                with open(directory, 'w') as f:
                    f.write(self.txtRaw)
                self.lastTxt = self.txt
                return 1
            else:
                raise FileNotFoundError('wtf bro')
        return 0
    
    def draw(self, screen, size):
        txtP1 = self.txt.split('\n')
        txttmp = []
        txtP2 = []
        c = 1
        for i in txtP1:
            while True:
                if len(i) > 2*size-4:
                    txttmp.append(i[:2*size-5])
                    i = i[2*size-5:]
                    continue
                txttmp.append(i)
                break
            txtP2.append(str(c)+'|'+txttmp[0])
            for i in txttmp[1:]:
                txtP2.append(' |'+i)
            c += 1
        maxi = max([len(i) for i in txtP2]+[screen.size-2])
        for i in range(len(txtP2)):
            txtP2[i] += ' '*(maxi-len(txtP2[i]))
        if self.cursorPosX < len(txtP2[self.cursorPosY]):
            txtP2[self.cursorPosY]=txtP2[self.cursorPosY][:self.cursorPosX]+'\x1b[7m'+txtP2[self.cursorPosY][self.cursorPosX]+'\x1b[27m'+txtP2[self.cursorPosY][self.cursorPosX+1:]
        else:
            txtP2[self.cursorPosY]=txtP2[self.cursorPosY][:self.cursorPosX]+'\x1b[7m'+txtP2[self.cursorPosY][self.cursorPosX]+'\x1b[27m'
        screen.load(txtP2,align=(0,1))
