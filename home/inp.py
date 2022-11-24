import time
try:
    import msvcrt
except:
    import termios, sys, tty, select
'''
\q -> QUIT
'''

BACKSPACE = 'BACKSPACE'
ENTER = 'ENTER'
TAB = 'TAB'
QUIT = 'QUIT'
SPACE = 'SPACE'
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
ARROWS = {'\x1b[A':UP,'\x1b[B':DOWN,'\x1b[C':RIGHT,'\x1b[D':LEFT}
ARROWSWIN = {'H':UP,'K':DOWN,'M':LEFT,'P':RIGHT}
CTRL = ['C@','CA','CB','CC','CD','CE','CF','CG','CH','CI','CJ','CK','CL','CM','CN','CO','CP','CQ','CR','CS','CT','CU','CV','CW','CX','CY','CZ','C[','C\\','C]','C^','C_']

def getChar(delTime=0.1):
    filedes = sys.stdin.fileno()
    old = termios.tcgetattr(filedes)
    tty.setraw(filedes)
    inp=select.select([sys.stdin],[],[],delTime)
    ch = sys.stdin.read(1) if inp[0] else ''
    if ch == '\x1b':
        d = sys.stdin.read(2)
        #print(d)
        ch+=d
    '''elif ch != '':
        print(ord(ch))'''
    termios.tcsetattr(filedes, termios.TCSADRAIN, old)
    return ch

def getKey(deltaTime=0.16):
     try:
        #linux
        inp2 = ''
        inp1 = getChar(delTime=deltaTime/2)
        if inp1 == '\\':
             while inp2 == '':
                inp2 = getChar(delTime=deltaTime/2)
        if inp1 == '':
            return ''
        if inp1 in ARROWS:
            return ARROWS[inp1]
        if (inp1 == '\\' and inp2 == 'q'):
            return QUIT
        if ord(inp1[0]) == 13:
            return ENTER
        if inp1 == '\t':
            return TAB
        if ord(inp1[0]) == 127:
            return BACKSPACE
        if inp1 == ' ':
            return SPACE
        if ord(inp1[0]) < 32:
            return CTRL[ord(inp1[0])]
        return inp1
     except:
        #windows
        time.sleep(deltaTime/4)
        if msvcrt.kbhit():
            k2 = ''
            k1 = msvcrt.getch()
            if k1 == b'\xe0':
                k2 = msvcrt.getch().decode('ascii')
                if k2 in ARROWSWIN:
                    return ARROWSWIN[k2]
            else:
                k1 = k1.decode('ascii')
                if k1 == '\\':
                    while k2 == '':
                        k2 = msvcrt.getch().decode('ascii')
            if k1 == '\r':
                return ENTER
            if k1 == '\t':
                return TAB
            if k1 == '\\' and k2 == 'q':
                return QUIT
            if k1 == ' ':
                return SPACE
            if ord(k1) == 8:
                return BACKSPACE
            if ord(k1) < 32:
                return CTRL[ord(k1)]
            return k1
        else:
            return ''
'''
x=''
while x!=QUIT:
    x=getKey(1)
    print(x)'''
