try:
    from screen import Screen
    import time, os

    print('\x1b[?25l',end='')

    screen1 = Screen()

    screen1.userInit()
    screen1.mainInit()

    randt = None

    def ScenesLoad(scene, timeStep):
        s=scene
        if scene == 0:s=screen1.mainControlSys()
        elif scene == 1 or scene == 2:s=screen1.fileControlSys()
        elif scene == 11:s=screen1.txtRun()
        elif scene == 3:s=screen1.gdRun()
        elif scene == 4:s=screen1.flappyRun()
        elif scene == 5:s=screen1.flappyHighest()
        elif scene == 6:s=screen1.caveHighest()
        if s == None:s = scene
        return s

    scene = 0
    once = True
    onceTxt = True
    timeStep = 0

    screen1.tmpPath = ['','','']

    while True:
        if screen1.logged:
            if scene == 0:once = True
            if scene == 4:onceTxt = True
            if scene == 1 and once:
                screen1.fileInit()
                once = False
            if scene == 4 and once:
                screen1.flappyBirdInit()
                once = False
            if scene == 11 and onceTxt:
                screen1.txtInit()
                onceTxt = False
            if scene == 3 and once:
                screen1.gdInit()
                once = False
            scene = ScenesLoad(scene, timeStep)
        else:
            randt = screen1.login(timeStep, randt=randt)
        screen1.loadTime()
        if not screen1.output():
            break
        timeStep+=1
    screen1.endscr(timeStep)

    os.system('cls' if os.name == 'nt' else 'clear')
    print('\x1b[?25hComputer exited with code 0')

    #recommended 6 lines space to see the whole screen, or else the cursor won't be able to move up and thus causes bugs
except:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\x1b[64A\x1b[?25hYour Computer ran out of battery :(')