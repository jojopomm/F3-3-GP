import sys, datetime, random, math, os, time, shutil
import inp, flappyBird, txtEdit, gd

#Constants
MOVE_CURSOR_UP = '\x1b[1A' 
DEL_LINE = '\x1b[2K' 
deltaTime = 0.1

ACCEPTABLES = ['txt']

def col(n):
    return '\x1b['+str(n)+'m'

DEFAULT = col(0)
BLACK_F = col(30)
RED_F = col(31)
GREEN_F = col(32)
YELLOW_F = col(33)
BLUE_F = col(34)
PURPLE_F = col(35)
CYAN_F = col(36)
WHITE_F = col(37)
BLACK_B = col(40)
RED_B = col(41)
GREEN_B = col(42)
YELLOW_B = col(43)
BLUE_B = col(44)
PURPLE_B = col(45)
CYAN_B = col(46)
WHITE_B = col(47)
UNDERLINE = col(4)
FLASH = col(5)
BRIGHT = col(1)


colDict = {
    '0':DEFAULT,
    '1':BRIGHT,
    '2':UNDERLINE,
    '3':FLASH,
    'a':BLACK_F,
    'b':RED_F,
    'c':GREEN_F,
    'd':YELLOW_F,
    'e':BLUE_F,
    'f':PURPLE_F,
    'g':CYAN_F,
    'h':WHITE_F,
    'A':BLACK_B,
    'B':RED_B,
    'C':GREEN_B,
    'D':YELLOW_B,
    'E':BLUE_B,
    'F':PURPLE_B,
    'G':CYAN_B,
    'H':WHITE_B
}

class Screen():
    def __init__(self, size=32):
        '''
        size: int, default size: 32
        self.screen: nested lists (size: 2*self.size x self.size), where each nested list represents a row in the output
        '''
        self.size = size
        self.screen = ['┏'+'━'*2*self.size+'┓']+['┃'+' '*2*self.size+'┃' for i in range(self.size)]+['┗'+'━'*2*self.size+'┛']
        self.screenPix = [[j for j in i] for i in self.screen]
        self.key = ''
        self.enterCount = 0
        self.tabCount = 0
        self.loadAnimation = [[' '*20]+['      '+('┏━━━━━━┓' if i//4 else ['  ━━━━━┓','┏━  ━━━┓','┏━━━  ━┓','┏━━━━━  '][i])+'      ']+['      '+('┃' if i != 11 else ' ')+'      '+('┃' if i != 4 else ' ') +'      ']+['      '+('┃' if i != 10 else ' ')+'      '+('┃' if i != 5 else ' ')+'      ']+['      '+('┗━━━━━━┛' if (i-7)//4 else ['  ━━━━━┛','┗━  ━━━┛','┗━━━  ━┛','┗━━━━━  '][::-1][i-7])+'      ']+[' '*5 + 'Loading' + '   '.replace(' ','.',i//3) + ' '*5] for i in range(12)]
        self.logAnimation = [[' '*20]+['      '+('┏━━━━━━┓' if i//4 else ['  ━━━━━┓','┏━  ━━━┓','┏━━━  ━┓','┏━━━━━  '][i])+'      ']+['      '+('┃' if i != 11 else ' ')+'      '+('┃' if i != 4 else ' ') +'      ']+['      '+('┃' if i != 10 else ' ')+'      '+('┃' if i != 5 else ' ')+'      ']+['      '+('┗━━━━━━┛' if (i-7)//4 else ['  ━━━━━┛','┗━  ━━━┛','┗━━━  ━┛','┗━━━━━  '][::-1][i-7])+'      ']+[' '*5 + 'Logging' + '   '.replace(' ','.',i//3) + ' '*5] for i in range(12)]
        self.trunOffAnimation = [[' '*20]+['      '+('┏━━━━━━┓' if i//4 else ['  ━━━━━┓','┏━  ━━━┓','┏━━━  ━┓','┏━━━━━  '][i])+'      ']+['      '+('┃' if i != 11 else ' ')+'      '+('┃' if i != 4 else ' ') +'      ']+['      '+('┃' if i != 10 else ' ')+'      '+('┃' if i != 5 else ' ')+'      ']+['      '+('┗━━━━━━┛' if (i-7)//4 else ['  ━━━━━┛','┗━  ━━━┛','┗━━━  ━┛','┗━━━━━  '][::-1][i-7])+'      ']+[' '*3 + 'Turning off' + '   '.replace(' ','.',i//3) + ' '*3] for i in range(12)]

    def moveCursor(self, n=None): 
        '''
        Moves cursor to the top of frame
        '''
        if n == None:
            n=self.size+2
        sys.stdout.write('\x1b['+str(n)+'A')
    
    def load(self, data, align='cc'):
        '''
        data: lists, where each item represents a row
        align: str or tuple<int>, 
        if str: 
            first character represents the alignment of x, the second for y
            'c': center
            'l': left
            'r': right
            't': top
            'b': bottom
        if tuple:
            first item is the x-coordinate of the top left corner
            second item is the y-coodinate of the top left corner
        '''
        dataNoColor = []
        dataFull = []
        tmp = ''
        tmpc = ''
        mCount = 0
        for i in range(len(data)):
            if '-' in data[i]:
                mCount=0
                for j in range(len(data[i])-1):
                    if data[i][j] == '-' and data[i][j+1] in colDict.keys():
                        mCount = 1
                        tmpc += colDict[data[i][j+1]]
                    if not mCount:
                        tmp += data[i][j]
                        tmpc += data[i][j]
                    if data[i][j] == 'm' and mCount:
                        mCount = 0
                if not mCount:
                    tmpc += data[i][-1]
                    tmp += data[i][-1]
                dataNoColor += [tmp]
                dataFull += [tmpc]
                tmp = ''
                tmpc = ''
            else:
                dataNoColor += [data[i]]
                dataFull += [data[i]]
        dataLen = (len(dataNoColor[0]), len(dataNoColor))
        if type(align[0]) == type(align[1]) and type(align[0]) == type('c') and align[0] in 'clr' and align[1] in 'ctb':
            delX = {'c':(2*self.size - dataLen[0])//2, 'l':0, 'r':2*self.size - dataLen[0] - 1}[align[0]] + 1
            delY = {'c':(self.size - dataLen[1])//2, 't':0, 'b':self.size - dataLen[1]}[align[1]] + 1
        elif type(align) == type((0,1)) and type(align[0]) == type(1) and type(align[1]) == type(1):
            delX = align[0] + 1
            delY = align[1] + 1
        else:
            raise ValueError('align has to be str or tuple<int>','align:', type(align), 'first element:',type(align[0]),'second element:',type(align[1]))
        #print(type(dataFull),(dataFull[0]))
        for y in range(dataLen[1]):
            self.screen[delY+y] = self.screen[delY+y][:delX+1] + dataFull[y] + self.screen[delY+y][delX+dataLen[0]+1:]
    
    def readPic(self, directory):
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

    def quit(self):
        '''
        checks if \q is pressed, yes -> returns 0
        '''
        if self.key == inp.QUIT:
            return 0
        return 1

    def output(self):
        '''
        prints the screen and moves cursor up
        '''
        print('\n'.join(self.screen))
        self.screen = ['┏'+'━'*2*self.size+'┓']+['┃'+' '*2*self.size+'┃' for i in range(self.size)]+['┗'+'━'*2*self.size+'┛']
        self.key = inp.getKey(deltaTime)
        self.moveCursor()
        return self.quit()
    
    def loadingScr(self, timeStep):
        self.load(self.loadAnimation[(timeStep//2)%12])
    
    def loggingScr(self, timeStep):
        self.load(self.logAnimation[(timeStep//2)%12])
    
    def turningOffScr(self, timeStep):
        self.load(self.trunOffAnimation[(timeStep//2)%12]) 
    
    def loadTime(self, align='rb'):
        self.dt = datetime.datetime.now()
        dt_str = self.dt.strftime("%A, %d %B %Y %I:%M:%S%p ")
        self.load([dt_str], align=align)

    def endscr(self, timeStep, n=34):
        '''
        loads turning off screen and shuts down
        '''
        randTime = random.randint(12, 120)
        for i in range(randTime):
            self.turningOffScr(timeStep+i)
            self.output()
        print('\n'.join(self.screen))
        for i in range(n):
            sys.stdout.write(MOVE_CURSOR_UP)
            sys.stdout.write(DEL_LINE)

    def userInit(self):
        '''
        initializes users related
        '''
        self.userScr = self.readPic("system/login.txt")[0]
        self.users={}
        self.logged = False
        self.logged1 = False
        self.user = ''
        self.userPw = ''
        with open("system/users.txt", 'rb') as f:
            while True:
                tmpu=f.readline().decode('utf-8').strip('\n')
                tmpp=f.readline().decode('utf-8').strip('\n')
                self.users[tmpu]=tmpp
                nl = f.readline().decode('utf-8').strip('\n')
                if nl == '//':
                    break

    def UserLogin(self):
        '''
        input & checking when logging in
        '''
        self.load(self.userScr)
        if self.key != '':
            if self.key == inp.ENTER:
                self.tabCount=0
                if self.user not in self.users.keys():
                    self.userScr = self.readPic("system/login.txt")[1]
                    self.user = ''
                    self.userPw = ''
                    return 0
                if self.userPw == self.users[self.user]:
                    return 1
                else:
                    self.user = ''
                    self.userPw = ''
                    self.userScr = self.readPic("system/login.txt")[1]
                    return 0
            if self.key == inp.TAB:
                self.tabCount+=1
                self.tabCount%=2
            tmp=self.userScr[2*self.tabCount+1]
            if '_' in tmp:
                if self.key not in [inp.ENTER, inp.BACKSPACE, inp.TAB]+inp.CTRL:
                    if not self.tabCount:
                        tmp = tmp[:tmp.index('_')] + self.key + tmp[tmp.index('_')+1:]
                        self.user += self.key
                    else:
                        tmp = tmp[:tmp.index('_')] + '●' + tmp[tmp.index('_')+1:]

                        self.userPw += self.key
                elif self.key == inp.BACKSPACE:
                    if tmp[tmp.index('_')-1] != ' ':
                        tmp = tmp[:tmp.index('_')-1] + '_' + tmp[tmp.index('_'):]
                        self.user = self.user[:len(self.user)-int(not self.tabCount)]
                        self.userPw = self.userPw[:len(self.userPw)-int(self.tabCount)]
            elif self.key == inp.BACKSPACE:
                tmp = tmp[:-2]+'_'+tmp[-1:]
                self.user = self.user[:len(self.user)-int(not self.tabCount)]
                self.userPw = self.userPw[:len(self.userPw)-int(self.tabCount)]
            self.userScr[2*self.tabCount+1] = tmp
        return 0
        
    def login(self, timeStep, randt=None):
        '''
        checking if user is logged or not
        returns randt 
        for the timestep for the logging screen animation
        '''
        if not self.logged1:
            self.logged1 = self.UserLogin()
            return None
        else:
            randt = random.randint(12,120) if randt == None else randt
            if randt>0:
                self.loggingScr(randt)
            else:
                self.logged = True
            return randt-1

    def fileInit(self):
        '''
        filemodes: 
        r: read
        n: new (waits until done)
        e: error (waits until presses enter)
        '''
        self.filemode = 'r'
        self.fileerror = ''
        self.curPath = self.user
        if not os.path.exists(self.curPath):
            os.mkdir(self.user)
            with open(self.user + "/info.txt", "w") as f:
                f.write(self.user + "\n")
            os.makedirs(self.user+'/data')
            with open(self.user+'/data/exists.txt', 'w') as f:
                f.write('True\n')
        else:
            with open(self.user + '/info.txt', 'rb') as f:
                y=f.readline().decode('utf-8')
                if y.strip() != self.user:
                    raise ValueError('No: '+y)
        self.curPath = self.user+'/data'
        self.files = os.listdir(self.curPath)
        self.fileCreateScr = self.readPic("system/newfile.txt")[0]
        self.fileName = ''
        self.pressB = False
        self.pressC = False
        self.pressD = False
        self.lastkey = ''
    
    def mainInit(self):
        self.mainScr = ['Files','Don\' Press!','Cave Game','Flappy bird','Flappy Bird Leaderboard', 'Cave Game Leaderboard']
    
    def fileScrLoad(self,files=None):
        if files == None:
            files = self.files
        #n = round(math.sqrt(len(files)))
        tmpn = ['|'+self.fileIndex[i]+'. '+files[i] for i in range(len(files))]
        mainScrMaxLen = max([len(i) for i in tmpn])
        for i in range(len(tmpn)):
            tmpn[i] +=  ' '*(mainScrMaxLen - len(tmpn[i])) + '|'
        '''
        tmp = ['' for i in range(n+1)]
        for i in range(len(files)):
            tmp[i//n] += tmpn[i] +' '*(mainScrMaxLen - len(tmpn[i]))+'|   ' 
        for i in range(len(tmp)):
            tmp[i] = tmp[i].strip(' ')'''
        while '' in tmpn:
            tmpn.remove('')
        tmpn[-1] = tmpn[-1] + ' '*(len(tmpn[0]) - len(tmpn[-1]))
        self.load(tmpn)

    def MainScrLoad(self):
        self.fileScrLoad(files=self.mainScr)
    
    def mainIn(self):
        if self.key != '' and self.key in self.fileIndex and self.fileIndex.find(self.key) < len(self.mainScr):
            #print(self.fileIndex.find(self.key))
            return self.fileIndex.find(self.key) + 1
            #print('oh no')
        return 0

    def createFileCheck(self):
      '''
      input & checking when logging in
      '''
      if self.key != '':
            if self.key == inp.ENTER:
                if os.path.exists(self.curPath+'/'+self.fileName):
                    self.fileCreateScr = self.readPic("system/newfile.txt")[2]
                    self.fileName = ''
                    return 0
                if (len(self.fileName.split('.')) != 2 or self.fileName.split('.')[-1] not in ACCEPTABLES) and (self.fileName[-1] != '/' or len(self.fileName.split('.')) != 1):
                    #print(len(self.fileName.split('.')) != 2, self.fileName.split('.')[-1], self.fileName[-1] != '/', len(self.fileName.split('.')) != 0, self.fileName.split('.'))
                    self.fileName = ''
                    self.fileCreateScr = self.readPic("system/newfile.txt")[1]
                    return 0
                else:
                    return 1
            tmp=self.fileCreateScr[1]
            if '_' in tmp:
                if self.key not in [inp.ENTER, inp.BACKSPACE, inp.TAB]+inp.CTRL:
                    tmp = tmp[:tmp.index('_')] + self.key + tmp[tmp.index('_')+1:]
                    self.fileName += self.key
                elif self.key == inp.BACKSPACE:
                    if tmp[tmp.index('_')-1] != ' ':
                        tmp = tmp[:tmp.index('_')-1] + '_' + tmp[tmp.index('_'):]
                        self.fileName = self.fileName[:-1]
            elif self.key == inp.BACKSPACE:
                tmp = tmp[:-2]+'_'+tmp[-1:]
                self.fileName = self.fileName[:-1]
            self.fileCreateScr[1] = tmp
            return 0

    def filesRefresh(self):
        tmp = os.listdir(self.curPath)
        tmpp =[[] for i in range(len(''.join(ACCEPTABLES)))]
        self.files = []
        for i in tmp:
            if len(i.split('.')) == 1:
                self.files += [i]
            else:
                tmpp[(''.join(ACCEPTABLES)).find(i.split('.')[-1])] += [i]
        for i in tmpp:
            self.files += sorted(i) 

    def dirIn(self):
        if self.key != '' and self.key in self.fileIndex and self.fileIndex.find(self.key) < len(self.files):
            self.fileName = self.files[self.fileIndex.find(self.key)]
            if len(self.fileName.split('.')) == 2:
                if self.fileName.split('.')[-1] == 'txt':
                    return 11
            else:
                self.curPath += '/'+self.fileName
                self.fileName = ''
                return 1
    
    def dirOut(self):
        if self.curPath != self.user+'/data':
            self.curPath = '/'.join(self.curPath.split('/')[:-1])
        else:
            return 0
    
    def dirNew(self):
        if self.key.lower() == 'q':
            self.filemode = 'r'
            self.fileName = ''
            self.fileerror = ''
            self.fileCreateScr = self.readPic("system/newfile.txt")[0]
        else:
            if len(self.files) < len(self.fileIndex):
                if self.fileerror == '':
                    self.filemode = 'n'
                    if self.createFileCheck():
                        if self.fileName.split('.')[-1] in ACCEPTABLES:
                            with open(self.curPath+'/'+self.fileName, 'w') as f:
                                pass
                        else:
                            #print(self.fileName)
                            os.mkdir(self.curPath+'/'+self.fileName)
                            with open(self.curPath+'/'+self.fileName+'exists.txt', 'w') as f:
                                f.write("True")
                        self.fileName = ''
                        self.fileCreateScr = self.readPic("system/newfile.txt")[0]
                        self.filemode = 'r'
                        self.fileerror = ''
                else:
                    self.fileCreateScr = self.readPic("system/newfile.txt")[3]
                    self.fileerror = 'n'
                    if self.key == inp.ENTER:
                        self.fileerror = ''
        
    def dirDel(self):
        self.filemode = 'd'
        if self.key.lower() == 'q':
            self.filemode = 'r'
            self.fileerror = ''
            self.fileName = ''
        elif self.key!='' and self.key!='d':
            if (self.key in self.fileIndex and self.fileIndex.find(self.key) < len(self.files) and self.files[self.fileIndex.find(self.key)] != 'exists.txt') or (self.fileerror == 'd1' and self.key in [inp.ENTER, inp.TAB]):
                if self.fileerror == '':
                    self.fileCreateScr = self.readPic("system/newfile.txt")[5]
                    self.fileerror = 'd1'
                if self.key == inp.ENTER:
                    self.filemode = 'r'
                    self.fileerror = ''
                    print(self.fileIndex.find(self.key))
                    self.fileName = self.files[self.fileIndex.find(self.lastkey)]
                    if self.fileName.split('.')[-1] not in ACCEPTABLES:
                        shutil.rmtree(self.curPath + '/' + self.fileName)
                    else:
                        os.remove(self.curPath + '/' + self.fileName)
                    self.fileCreateScr = self.readPic("system/newfile.txt")[0]
                    self.fileName = ''
                elif self.key == inp.TAB:
                    self.filemode = 'r'
                    self.fileerror = ''
                    self.fileName = ''
                    self.fileCreateScr = self.readPic("system/newfile.txt")[0]
                self.lastkey = self.key
            elif self.key in self.fileIndex and self.fileIndex.find(self.key) < len(self.files) and self.files[self.fileIndex.find(self.key)] == 'exists.txt':
                if self.fileerror == '':
                    self.fileCreateScr = self.readPic("system/newfile.txt")[6]
                    self.fileerror = 'd'
                if self.key == inp.ENTER:
                    self.filemode = 'r'
                    self.fileerror = ''
                    self.fileCreateScr = self.readPic("system/newfile.txt")[0]
            else:
                if self.fileerror == '':
                    self.fileCreateScr = self.readPic("system/newfile.txt")[4]
                    self.fileerror = 'd'
                if self.key == inp.ENTER:
                    self.filemode = 'r'
                    self.fileerror = ''
                    self.fileCreateScr = self.readPic("system/newfile.txt")[0]
    
    def fileControlSys(self):
        s2=1
        self.fileIndex = '0123456789acefghijklmopqrstuvwxyzACEFGHIJKLMOPQRSTUVWXYZ'[:29-len(self.tmpPath)]
        self.fileScrLoad()
        if self.filemode == 'r' and self.fileerror == '':
            s2=self.dirIn()
            if self.pressB:
                s=self.dirOut()
                if s==0:return 0
        if self.pressC or self.filemode == 'n' or self.fileerror == 'n':
            self.dirNew()
        if self.pressD or self.filemode == 'd' or self.fileerror == 'd':
            self.dirDel()
        if self.filemode == 'n' or (self.key!='d' and self.fileerror in ['d','d1']):
            self.load(self.fileCreateScr)
        self.filesRefresh()
        #print(self.filemode)
        tmp = self.curPath.split('/')[1:]
        tmpp = [len(i)+1 for i in tmp]
        tmpPath = []
        while len(tmpp) > 0:
            i = 0
            while sum(tmpp[:i+1]) < 24 and i+1!=len(tmpp):
                i+=1
            tmpPath += ['/'.join(tmp[:i+1])]
            if i+1 != len(tmpp):
                tmpp = tmpp[i+1:]
                tmp = tmp[i+1:]
            else:
                break
        maxi = max([len(i) for i in tmpPath])
        for i in range(len(tmpPath)):
            tmpPath[i] += ' '*(maxi - len(tmpPath[i]))
        tmpPath = [' '*maxi,' '*maxi] + tmpPath
        self.tmpPath = tmpPath
        self.load(tmpPath, align='ct') 
        self.load(['Path:'],align=(0,2))
        self.load(['-'*62],align=(0,1))
        self.load(['-'*62],align=(0,len(tmpPath)))
        self.load(['Delete file: D ','Add file: C    ','Move back up: B'],align='lb')
        tmp = [''.join(['Press the index to delete file (Press Q to cancel)' if self.filemode == 'd' else '','Press the index to open the file' if self.filemode == 'r' else ''])]
        self.load(tmp, align='ct')
        self.pressB = self.key.lower() == 'b'
        self.pressC = self.key.lower() == 'c' and (self.filemode != 'd' and 'd' not in self.fileerror)
        self.pressD = self.key.lower() == 'd' and (self.filemode != 'n' and self.fileerror != 'n')
        return s2

    def mainControlSys(self):
        self.fileIndex = '0123456789acefghijklmopqrstuvwxyzACEFGHIJKLMOPQRSTUVWXYZ'[:29-len(self.tmpPath)]
        self.MainScrLoad()
        return self.mainIn()

    def flappyBirdInit(self):
        self.flappy = flappyBird.Bird()
        self.score = 0
        self.ggScr = self.readPic("system/flappyBirdGraphics/ggScr.txt")[0]
        self.quitScr = self.readPic("system/flappyBirdGraphics/quitScr.txt")[0]
        self.flappyMode = 'n'
        self.pipe = [flappyBird.Pipe(32), flappyBird.Pipe()]
        self.once = True
    
    def flappyRun(self):
        if self.flappyMode == 'n':
            for j in self.pipe:
                j.move(deltaTime)
            if self.flappy.move(self.key, deltaTime, self):
                self.flappyMode = 'g'
            if self.key.lower() == 'q':
                self.flappyMode = 's'
        if self.flappyMode in 'sg':
            if self.flappyMode == 's':
                self.bg = self.quitScr
            else:
                if self.once:
                    score = 'Your Score: ' + str(self.score)
                    self.ggScr[3] = self.ggScr[3][0]+score+self.ggScr[3][len(score)+1:]
                    self.once = False
                self.bg = self.ggScr
            if self.key == inp.ENTER:
                with open("system/flappyBirdGraphics/Highest.txt", "a") as f:
                    f.write(self.user + '-' + self.dt.strftime("%d %B %Y %I:%M:%S%p ") + '-' + str(self.score)+'\n')
                return 0
            if self.key == inp.TAB:
                with open("system/flappyBirdGraphics/Highest.txt", "a") as f:
                    f.write(self.user + '-' + self.dt.strftime("%d %B %Y %I:%M:%S%p ") + '-' + str(self.score)+'\n')
                if self.flappyMode == 'g':
                    self.flappyBirdInit()
                self.flappyMode = 'n'
        if self.flappyMode == 'n':
            for i in self.pipe:
                if i.draw(self):
                    self.pipe.pop(0)
                    self.pipe.append(flappyBird.Pipe())
                    self.score += 1
            self.flappy.draw(self)
            self.load(['Flappy bird|Press Q to quit|Your score: '+str(self.score)],align='ct')
            if self.collide():
                self.flappyMode = 'g'
        else:
            self.load(self.bg)
        return 4

    def collide(self):
        flappySurroundings = [(self.flappy.x, self.flappy.y) for x in range(self.flappy.size[0])] + [(self.flappy.x, self.flappy.y+2) for x in range(self.flappy.size[0])] + [(self.flappy.x,self.flappy.y+1)] + [(self.flappy.x+self.flappy.size[0]-1,self.flappy.y+1)]
        for x,y in flappySurroundings:
            #print(int(x),int(y),self.screen[int(y)][int(x)],self.screen[int(y)][int(x)] != ' ' and self.screen[int(y)][int(x)] in self.pipe[0].pic)
            if self.screen[int(y)][int(x)] != ' ' and self.screen[int(y)][int(x)] in '┌┴─┴┐|└┬─┬┘':
                return True
        return False

    def addSpace(self, lst):
        lst = [i.strip(' ') for i in lst]
        maxi = max([len(i) for i in lst])
        for i in range(len(lst)):
            lst[i] += ' '*(maxi-len(lst[i]))
        return lst

    def flappyHighest(self, n=20):
        if self.key.lower() == 'q':
            return 0
        tmpdict = {}
        with open("system/flappyBirdGraphics/Highest.txt",'rb') as f:
            for tmpp in f:
                tmp = tmpp.decode('utf-8')
                tmpdict['-'.join(tmp.split('-')[:2])] = int(tmp.split('-')[-1].strip('\n').strip(' '))+1
        tmpdict = dict(sorted(tmpdict.items(), key=lambda item: item[1])[::-1])
        user = []
        date = []
        score = []
        j = 0
        for i in tmpdict.keys():
            if j > n:
                break
            user.append(i.split('-')[0])
            date.append(i.split('-')[1].strip(' '))
            score.append(str(tmpdict[i]-1))
            j += 1
        user = self.addSpace(['User']+(user if len(user) < 9 else user[:6]+'...'))
        date = self.addSpace(['Date n time']+date)
        score = self.addSpace(['Score']+score)
        scr = []
        for i in range(len(user)):
            scr.append(user[i] + ' ' + date[i] + ' ' + score[i])
        tmp = 'Leaderboard (top ' + str(n) + ')'
        scr = [' '*(len(scr[0])//2 - len(tmp)//2) + tmp + ' '*(len(scr[0])-len(scr[0])//2 - len(tmp)//2)] + scr
        self.load(scr)
        return 5
    
    def txtInit(self):
        '''self.txtEditor = txtEdit.txtEditor(self)
        self.txtMode = "w"'''
        self.txtScr = self.readPic("system/flappyBirdGraphics/quitScr.txt")[2]
        '''self.save = 0'''
        self.time = time.time()

    def txtRun(self):
        '''
        Sorry, There wasn't enough time to finish this part

        if self.key == 'CQ' and self.txtMode == 'w':
            if self.save:
                self.txtMode = 'w'
                return 1
            else:
                self.txtMode = 's'
        if self.txtMode == 'w':
            self.txtEditor.inputting(self.key, self.screen)
            self.save = self.txtEditor.save(self.key, self.curPath+"/"+self.fileName)
        if self.txtMode == 's':
            if self.key == inp.TAB:
                self.txtMode = 'w'
            elif self.key == inp.ENTER:
                return 1
        if self.txtMode == 'w':
            self.txtEditor.draw(self,self.size)
        elif self.txtMode == 's':
            self.load(self.txtScr)'''
        if time.time() - self.time > 2:
            return 1
        else:
            self.load(self.txtScr)
            return 11

    def gdInit(self):
        self.cave = gd.Cave(30)
        self.ggScr = self.txtScr = self.readPic("system/flappyBirdGraphics/ggScr.txt")[0]
        self.quitScr = self.txtScr = self.readPic("system/flappyBirdGraphics/quitScr.txt")[0]
        self.caveMode ='r'

    def gdRun(self):
        if self.caveMode == 'g':
            self.caveMode = 'g'
            txt = 'Ur Pts: ' + str(self.cave.t//1000 + self.cave.stuff.count('♛')*5)
            self.ggScr = self.ggScr[:2] + [self.ggScr[2].replace(' '*len(txt),txt,len(txt))] + self.ggScr[3:]
        if self.key.lower() == 'q':
            self.caveMode = 'p'
        if self.cave.hp > 0 and self.caveMode == 'r':
            self.cave.move(self.key)
            self.cave.draw(self)
        elif self.caveMode == 'g':
            self.load(self.ggScr)
            if self.key == inp.TAB:
                with open("Cave/Highest.txt", "a") as f:
                    f.write(self.user + '-' + self.dt.strftime("%d %B %Y %I:%M:%S%p ") + '-' + str(self.cave.t//60 + self.cave.stuff.count('♛')*10)+'\n')
                self.caveMode = 'r'
                self.cave = gd.Cave(30)
                return 3
            elif self.key == inp.ENTER:
                with open("Cave/Highest.txt", "a") as f:
                    f.write(self.user + '-' + self.dt.strftime("%d %B %Y %I:%M:%S%p ") + '-' + str(self.cave.t//60 + self.cave.stuff.count('♛')*10)+'\n')
                return 0
        elif self.caveMode == 'p':
            self.load(self.quitScr)
            if self.key == inp.TAB:
                self.caveMode = 'r'
                return 3
            elif self.key == inp.ENTER:
                return 0
        return 3

    def caveHighest(self, n=20):
        if self.key.lower() == 'q':
            return 0
        tmpdict = {}
        with open("Cave/Highest.txt") as f:
            for tmp in f:
                tmpdict['-'.join(tmp.split('-')[:2])] = int(tmp.split('-')[-1].strip('\n').strip(' '))+1
        tmpdict = dict(sorted(tmpdict.items(), key=lambda item: item[1])[::-1])
        user = []
        date = []
        score = []
        j = 0
        for i in tmpdict.keys():
            if j > n:
                break
            user.append(i.split('-')[0])
            date.append(i.split('-')[1].strip(' '))
            score.append(str(tmpdict[i]-1))
            j += 1
        user = self.addSpace(['User']+(user if len(user) < 9 else user[:6]+'...'))
        date = self.addSpace(['Date n time']+date)
        score = self.addSpace(['Score']+score)
        scr = []
        for i in range(len(user)):
            scr.append(user[i] + ' ' + date[i] + ' ' + score[i])
        tmp = 'Leaderboard (top ' + str(n) + ')'
        scr = [' '*(len(scr[0])//2 - len(tmp)//2) + tmp + ' '*(len(scr[0])-len(scr[0])//2 - len(tmp)//2)] + scr
        self.load(scr)
        return 6



