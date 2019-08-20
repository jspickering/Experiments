################################################################################
# Programmed by Jade S Pickering (April 2019)                                  #
# Using PsychoPy v1.90.3                                                       #
# Based on the Cambridge Gambling Task as described in Rogers et al. (1999)    #
################################################################################

# Import libraries
from psychopy import core, visual, gui, data, event, sound, logging
from psychopy.tools.filetools import fromFile, toFile, os, sys
import random, time, csv, numpy as np


# ====================== #
# ==== DIALOGUE BOX ==== #
# ====================== #

# create a DlgFromDict
info = {
    'Participant ID': '',                       # participant number
    'First condition':['asc', 'desc']           # which counterbalancing option participant is assigned to
    }
infoDlg = gui.DlgFromDict(
    dictionary=info, 
    title='TestExperiment', 
    order=['Participant ID', 'First condition'], 
    )
if infoDlg.OK: #this will be True (user hit OK) or False (cancelled)
    print(info)
else: 
    print('User Cancelled')

# Create window
win = visual.Window(
    [1024,768],
    fullscr = True, 
    allowGUI = False,
    monitor = "testMonitor"
    )

# ====================== #
# ===== PARAMETERS ===== #
# ====================== #
nConditions = 2 # 2 conditions (asc and desc)
nBlocks = 1 # 8 blocks (4 for ascending, 4 for descending condition)
nTrials = 3 # 9 trials per block with different box ratios
bankPerc = [0.05, 0.25, 0.50, 0.75, 0.95] # % of current bank total to be used to inform available bets
respKeysBox = ['z', 'm', 'escape'] # allowable keys for choosing box (z = left/red, m = right/blue)
respKeysBet = ['space', 'escape']  # to stop the bet choices ascending/descending
expKeys = ['return','escape']      # keys allowed on break screens
boxWidth = 70
boxHeight = 70
boxPosy = 200
boxPosx = [-360, -280, -200, -120, -40, 40, 120, 200, 280, 360]
tokenChoices = [0,1,2,3,4,5,6,7,8,9] # use this to randomly pick which box the token is hidden under on each trial
tokenPos = random.choice(tokenChoices) # choose token hiding place
durITI = 1 # duration of inter-trial interval
Trial1 = ["red", "red", "red", "red", "red", "red", "red", "red", "red", "blue"]
Trial2 = ["red", "red", "red", "red", "red", "red", "red", "red", "blue", "blue"]
Trial3 = ["red", "red", "red", "red", "red", "red", "red", "blue", "blue", "blue"]
Trial4 = ["red", "red", "red", "red", "red", "red", "blue", "blue", "blue", "blue"]
Trial5 = ["red", "red", "red", "red", "red", "blue", "blue", "blue", "blue", "blue"]
Trial6 = ["red", "red", "red", "red", "blue", "blue", "blue", "blue", "blue", "blue"]
Trial7 = ["red", "red", "red", "blue", "blue", "blue", "blue", "blue", "blue", "blue"]
Trial8 = ["red", "red", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue"]
Trial9 = ["red", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue"]
TrialNum = [1,2,3,4,5,6,7,8,9] # use this list to shuffle trial order per block
Trials = [Trial3, Trial6, Trial9]
trialTypes = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
optionPosX = 280
optionPosY = -180
startBank = 100 # number of points in the bank at the start of each block
betPercAsc = [0.05, 0.25, 0.5, 0.75, 0.95] # percentage of current score to display as bet options (ascending condition)
betPercDesc = [0.95, 0.75, 0.5, 0.25, 0.05] # percentage of current score to display as bet options (descending condition)
currentBank = startBank 
greyCol = "#262626" # colour variable used a lot
betOption = int(round((currentBank*betPercAsc[0]),0)) # calculation for bet options
iBet = 0.05 # placeholder for bet percentage, will be automatically updated in the betAsc and betDesc functions
betDuration = 1.5 # time each bet is available on screen before changing
updatePoints = 8 # random placeholder for updatePoints that will never appear on the first trial
wedges = [72, 144, 216, 288, 360]   # degrees for each wedge segment in bet counter
participant = info['Participant ID']
bet = core.Clock()

if info['First condition'] == 'asc':
    firstCond = 'asc'
    secondCond = 'desc'
    firstInstr = 'INCREASING'
    secondInstr = 'DECREASING'
elif info['First condition'] == 'desc':
    firstCond = 'desc'
    secondCond = 'asc'
    firstInstr = 'DECREASING'
    secondInstr = 'INCREASING'



# ========================== #
# ===== SET UP LOGGING ===== #
# ========================== #

trialClock = core.Clock()

dateStr = time.strftime("%b_%d_%H%M", time.localtime())#add the current time
    
dataFile = open(participant + '_' + dateStr + '.csv', 'w')
writer = csv.writer(dataFile)
writer.writerow(["participant","condition","blockNum","trialNum","trialType","colourRT","colourChoice","betRT","betChoice","winlose","betValue","totalPoints","failedBlock"])


# ========================== #
# ===== CREATE STIMULI ===== #
# ========================== #

# Instruction screen
instructions = visual.TextStim(
            win,
            units="pix",
            height=20,
            text="In this task a yellow token has been hidden under one of the boxes at the top of the screen. The boxes will always be a mix of RED and BLUE, and your task is to guess the colour that you think the token is hidden under, and then place a stake on your choice.\n\nFirst you must select your box colour choice by pressing the LEFT key for a red box or the RIGHT key for a blue box.\n\nNext, you will see 5 stake options appear on the screen one by one. You must press the SPACEBAR when the counter stops on an option you'd like to select. For half of the task these stake options will be shown in INCREASING order, and in the other half they will DECREASE. You'll be warned at the start of each section when this changes.\n\nThe goal is to win as many points as you can.\n\nPress ENTER to continue.",
            )


# block message for first condition and second condition
blockMessage1 = visual.TextStim(
            win, 
            units="pix",
            height=20,
            text="Your stake choices will be shown in %s order.\n\nPress ENTER to start."%firstInstr)
blockMessage2 = visual.TextStim(
            win, 
            units="pix",
            height=20,
            text="Your stake choices will be shown in %s order.\n\nPress ENTER to start."%secondInstr)

endPrompts = visual.TextStim(
            win, 
            units="pix",
            height=20,
            text="Final score: %s\n\nThis is the end of practice. Please tell the researcher that you have finished, and take this opportunity to ask questions if you're unsure of anything in the task."%(currentBank))

# Displays the current score at the top of the screen
#bankText = visual.TextStim(
#win,
#text="Score: %s"%currentBank,
#units="pix",
#height=30,
#color=greyCol,
#pos=(0,275)
#)

# displays current bet choice
#betCircle = visual.Circle(
#        win,
#        units="pix",
#        size = 225,
#        lineWidth=5,
#        lineColor=greyCol,
#        pos=(0,0)
#        )
#betText = visual.TextStim(
#        win,
#        units="pix",
#        text="%s"%betOption,
#        height=80,
#        color="black",
#        alignHoriz='center',
#        pos=(0,0)
#        )


# displays options of choosing red or blue 
optionRedBox = visual.Rect(
        win,
        units="pix",
        size = 225,
        lineWidth=5,
        lineColor=greyCol,
        pos=(500,200)
        )
optionRedText = visual.TextStim(
        win,
        units="pix",
        text="%s"%betOption,
        height=70,
        color="#16720E",
        alignHoriz='center',
        pos=(500,200)
        )


# Displays the boxes in a line
box1 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[0],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box2 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[1],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box3 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[2],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box4 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[3],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box5 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[4],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box6 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[5],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box7 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[6],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box8 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[7],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box9 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[8],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )
box10 = visual.Rect(
    win, 
    units ="pix",
    width=boxWidth, 
    height=boxHeight,
    pos=[boxPosx[9],boxPosy],
    fillColor="blue",
    lineColor ="black"
    )

boxes_stim = [box1, box2, box3, box4, box5, box6, box7, box8, box9, box10]


# display yellow token
yellowToken = visual.Circle(
    win,
    units = "pix",
    radius = 25,
    pos=[boxPosx[tokenPos],boxPosy],
    fillColor = "yellow",
    lineColor = "black"
    )

# displays the choices and highlights the chosen box colour
optionRedBox = visual.Rect(
        win,
        units="pix",
        pos=[-optionPosX,optionPosY],
        height = 100,
        width = 150,
        lineWidth=2,
        lineColor="black"
        )
optionRedText = visual.TextStim(
        win,
        units="pix",
        pos=[-optionPosX,optionPosY],
        text="RED",
        height=50,
        color="red",
        alignHoriz='center'
        )
optionBlueBox = visual.Rect(
        win,
        units="pix",
        pos=[optionPosX,optionPosY],
        height = 100,
        width = 150,
        lineWidth=2,
        lineColor="black"
        )
optionBlueText = visual.TextStim(
        win,
        units="pix",
        pos=[optionPosX,optionPosY],
        text="BLUE",
        height=50,
        color="blue",
        alignHoriz='center'
        )
redChosenBox = visual.Rect(
        win,
        units="pix",
        pos=[-optionPosX,optionPosY],
        height = 100,
        width = 150,
        lineWidth=2,
        fillColor="red",
        lineColor="black"
        )
redChosenText = visual.TextStim(
        win,
        units="pix",
        pos=[-optionPosX,optionPosY],
        text="RED",
        height=50,
        color="black",
        alignHoriz='center'
        )
blueChosenBox = visual.Rect(
        win,
        units="pix",
        pos=[optionPosX,optionPosY],
        height = 100,
        width = 150,
        lineWidth=2,
        fillColor="blue",
        lineColor="black"
        )
blueChosenText = visual.TextStim(
        win,
        units="pix",
        pos=[optionPosX,optionPosY],
        text="BLUE",
        height=50,
        color="black",
        alignHoriz='center'
        )

# yellow token question text
optionQuestion = visual.TextStim(
        win,
        units="pix",
        pos=(0,0),
        text="Where is the yellow \ntoken?",
        height=50,
        color=greyCol,
        alignHoriz='center',
        alignVert='center'
        )


# stimuli for bet choices
bankText = visual.TextStim(
        win,
        text="Score: %s"%currentBank,
        units="pix",
        pos=(0,275),
        height=50,
        color=greyCol #,
#        alignHoriz='center',
#        alignVert='center', 
        )
        
        
betCircle = visual.Circle(
        win,
        units="pix",
        size = 220,
        lineWidth=5,
        lineColor=greyCol,
        pos=(0,0)
        )
betText = visual.TextStim(
        win,
        units="pix",
        text="%s"%betOption,
        height=80,
        color="black",
        alignHoriz='center',
        pos=(0,0)
        )
segments = visual.RadialStim(
        win=win,
        units="pix",
        color="#696969",
        angularCycles = 0,
        radialCycles = 0,
        ori= 0,
        pos=(0,0),
        size=(220,220), 
        visibleWedge=(0.0, wedges[0])
        )
overlayCircle = visual.Circle(
        win,
        units="pix",
        size = 180,
        fillColor = "gray",
        lineColor = "gray",
        pos = (0,0),
        )

# "place bet" text
placebetText = visual.TextStim(
        win,
        units = "pix",
        pos=(0,0),
        text="Get ready to place your stake...",
        height=50,
        color=greyCol,
        alignHoriz='center',
        alignVert='center'
        )






# ========================== #
# ======= FUNCTIONs ======== #
# ========================== #

def betAsc():
    global updatePoints
    global bet
    global betTime
    global betOption
    global currSegment
    expBreak = False
    currSegment = 0
    event.clearEvents()
    bet.reset()
    bet = core.Clock()
    betTime = 0 #placeholder as we know it should never be zero
    betFinished = False
    for iBet in betPercAsc:
        print(iBet)
        print("looping")
        betOption = int(round((currentBank*iBet),0)) # work out the current proportion to display on screen
        print(betOption)
        betText.text=(betOption)
        segments.visibleWedge = [0, wedges[currSegment]]
        print(currSegment)
        segments.draw()
        betCircle.draw()
        overlayCircle.draw()
        betText.draw()
        
        #redraw chosen box
        if boxChoice == ['z']:
            redChosenBox.draw()
            redChosenText.draw()
        elif boxChoice ==['m']:
            blueChosenBox.draw()
            blueChosenText.draw()
        
        #redraw bank info
        for box in boxes_stim:
            box.draw()
        bankText.draw()   
        
        win.flip()
        core.wait(betDuration)
        currSegment = currSegment+1
        
        #wait for response,break loop if choice made, quit if esc, wait and move onto the next iteration if no response recorded
        betMade = event.getKeys(keyList = respKeysBet)
        if betMade == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()   
        elif betMade == ['space']:
            print("Choice made: %d"%betOption)
            betSec = bet.getTime()
            betTime = betSec*1000
            expBreak = True
            betFinished = True
            print(betOption)
            print("breaking loop")

            
        if expBreak == True:
            break

    if betFinished == False:
        print("maximum time reached, auto choosing last bet")
        betTime = betDuration*5
    updatePoints = betOption
    print("exited loop")
    print("Participant chose: %d"% betOption) # displays the betOption chosen OR the last bet presented if nothing was chosen
    

def betDesc():
    global updatePoints
    global bet
    global betTime
    global betOption
    global currSegment
    expBreak = False
    currSegment = 0
    event.clearEvents()
    bet.reset()
    bet = core.Clock()
    betTime = 0 #placeholder as we know it should never be zero
    betFinished = False
    for iBet in betPercDesc:
        print(iBet)
        print("looping")
        betOption = int(round((currentBank*iBet),0)) # work out the current proportion to display on screen
        print(betOption)
        betText.text=(betOption)
        segments.visibleWedge = [0, wedges[currSegment]]
        print(currSegment)
        segments.draw()
        overlayCircle.draw()
        betCircle.draw()
        betText.draw()
        
        #redraw chosen box
        if boxChoice == ['z']:
            redChosenBox.draw()
            redChosenText.draw()
        elif boxChoice ==['m']:
            blueChosenBox.draw()
            blueChosenText.draw()
        
        #redraw bank info
        for box in boxes_stim:
            box.draw()
        bankText.draw()           
        
        win.flip()
        core.wait(betDuration)
        currSegment = currSegment + 1
        
        #wait for response,break loop if choice made, quit if esc, wait and move onto the next iteration if no response recorded
        betMade = event.getKeys(keyList = respKeysBet)
        if betMade == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()   
        elif betMade == ['space']:
            print("Choice made: %d"%betOption)
            betSec = bet.getTime()
            betTime = betSec*1000
            expBreak = True
            betFinished = True
            
            print(betOption)
            print("breaking loop")
          
            
        if expBreak == True:
            break
    
    if betFinished == False:
        print("maximum time reached, auto choosing last bet")
        betTime = (betDuration*5)*1000
    updatePoints = betOption
    print(updatePoints)
    print("exited loop")
    print("Participant chose: %d"% betOption) # displays the betOption chosen OR the last bet presented if nothing was chosen


def placeBet():
    #draw chosen box
    if boxChoice == ['z']:
        redChosenBox.draw()
        redChosenText.draw()
    elif boxChoice ==['m']:
        blueChosenBox.draw()
        blueChosenText.draw()
    #draw box choices    
    for box in boxes_stim:
        box.draw()
        bankText.draw()
    
    # draw "Get ready to place your bet..." text
    placebetText.draw()
    
    win.flip()
    core.wait(2)

def dispFeedback():
    global currentBank
    winMsg = "You win %s points"%updatePoints
    loseMsg = "You lose %s points"%updatePoints
    
    # Feedback text
    winText = visual.TextStim(
            win,
            units="pix",
            text="%s"%winMsg,
            height=50,
            color="black",
            alignHoriz='center',
            pos=(0,0)
            )
    
    loseText = visual.TextStim(
            win,
            units="pix",
            text="%s"%loseMsg,
            height=50,
            color="black",
            alignHoriz='center',
            pos=(0,0)
            )    
    
    if trialOutcome == 'win':
        currentBank = currentBank+updatePoints
        winText.draw()
    elif trialOutcome == 'lose':
        currentBank = currentBank-updatePoints
        loseText.draw()
        



# ========================== #
# === EXPERIMENT OUTLINE === #
# ========================== #

instructions.draw() # PsychoPy prepares stimulus
win.flip()          # PsychoPy updates the screen when stimulus is ready to prevent tears

thisKey = event.waitKeys(keyList = expKeys) #psychopy waits for a key press before moving on
if thisKey == ['escape']:
    print("Warning: Session aborted by user")
    win.close()
    core.quit()

blockMessage1.draw()
win.flip()

#thisKey = event.waitKeys(keyList = expKeys)
#if thisKey == ['escape']:
#    print("Warning: Session aborted by user")
#    win.close()
#    core.quit()


 #Main experiment body

# BLOCK LOOP STARTS HERE
for iBlock in range (0,nBlocks):
    if iBlock <= 3:
        condition = firstCond
    elif iBlock > 3:
        condition = secondCond
    
    if iBlock <= 3:
        blockMessage1.draw()
        win.flip()
        thisKey = event.waitKeys(keyList = expKeys)
        if thisKey == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()
    elif iBlock > 3:
        blockMessage2.draw()
        win.flip()
        thisKey = event.waitKeys(keyList = expKeys)
        if thisKey == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()
    
    
    # shuffle Trials and TrialNum to the same order
    combined = list(zip(Trials,TrialNum, trialTypes))
    random.shuffle(combined)        
    Trials, TrialNum, trialTypes = zip(*combined)
    print(TrialNum)
    print(Trials)
    print(trialTypes)
    currTrial=0
    currentBank=startBank
    failedBlock = False
    
    # TRIAL LOOP STARTS HERE
    for iTrial in Trials:
        clock=core.Clock()
        trialType = trialTypes[currTrial]
        tokenPos = random.choice(tokenChoices) # choose token hiding place
        yellowToken.pos=[boxPosx[tokenPos],boxPosy] # assign token hiding place

        # assign box colours depending on ratio for this trial
        boxCol=0
        for box in boxes_stim:
            box.fillColor=Trials[currTrial][boxCol]
            boxCol+=1

        # draw boxes
        for box in boxes_stim:
            box.draw()
        # assign and draw bank total
        bankText.text = "Score: %s"%currentBank
        bankText.draw()
        # draw options for choosing red or blue
        optionQuestion.draw()
        optionBlueBox.draw()
        optionBlueText.draw()
        optionRedBox.draw()
        optionRedText.draw()
        # display boxes, bank total, options

        win.flip()
        RT = core.Clock() # start timing RT here
        
        # check for keyboard input before displaying choice
        boxChoice = event.waitKeys(keyList = respKeysBox)
        if boxChoice == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()
        elif boxChoice == ['z']:    # if they choose red
            print(boxChoice)
            # display other stimuli too
            redChosenBox.draw()
            redChosenText.draw()
            rtSecs = RT.getTime()
            delibTime = rtSecs *1000
        elif boxChoice ==['m']:     # if they choose blue
            print(boxChoice)
            blueChosenBox.draw()
            blueChosenText.draw()
            rtSecs = RT.getTime()
            delibTime = rtSecs *1000
        
        print("Time is: %f"%delibTime)
        
        # draw boxes, bank total, ask options
        for box in boxes_stim:
            box.draw()
        bankText.draw()        
        optionQuestion.draw()
        win.flip()

        # draw "place your bet" screen
        placeBet()
        
        # display bet choices (in functions) along with relevant stimuli
        if iBlock <= 3:
            if firstCond == 'asc':
                betAsc()
            elif firstCond == 'desc':    
                betDesc()
        elif iBlock > 3:
            if secondCond == 'asc':
                betAsc()
            elif secondCond == 'desc':
                betDesc()
        
        # work out which colour the token is hidden behind
        for box in boxes_stim:
            if box.pos[0] == yellowToken.pos[0]:
                tokenBox = box.fillColor
        
        # work out if the participant was correct or not based on their choice
        if tokenBox == 'red':
            if boxChoice == ['z']:
                trialOutcome = 'win'
            elif boxChoice == ['m']:
                trialOutcome = 'lose'
        elif tokenBox == 'blue':
            if boxChoice == ['z']:
                trialOutcome = 'lose'
            elif boxChoice == ['m']:
                trialOutcome = 'win'

        core.wait(1)

        # draw boxes, chosen colour, bank total, and reveal token location
        for box in boxes_stim:
#            if box.pos[0] != yellowToken.pos[0]: # only draws boxes thate DON'T have a hidden token
            box.draw()
        if boxChoice == ['z']:
            redChosenBox.draw()
            redChosenText.draw()
            boxOutcome = "red"
        elif boxChoice ==['m']:
            blueChosenBox.draw()
            blueChosenText.draw()
            boxOutcome = "blue"
        yellowToken.draw()
        bankText.draw()
        # need to draw a box outline here for the one replaced by yellow token                
        
        win.flip()
        core.wait(0.75)
        
        # draws boxes, chosen colour, bank total, yellow token, and a win/lose message and points gained/lost
        for box in boxes_stim:
#            if box.pos[0] != yellowToken.pos[0]: # only draws boxes thate DON'T have a hidden token
            box.draw()
        if boxChoice == ['z']:
            redChosenBox.draw()
            redChosenText.draw()
        elif boxChoice ==['m']:
            blueChosenBox.draw()
            blueChosenText.draw()
        yellowToken.draw()
        bankText.draw()
        dispFeedback()

        # display stims
        win.flip()
        core.wait(2)
        
        # did participant fail block by going as low as <=1 points?
        if currentBank <=1:
            failedBlock = True
        else:
            failedBlock = False
        
        # write all data to file
        dataFile.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \n'%(participant,condition,iBlock+1,currTrial+1, trialType, delibTime,boxOutcome,betTime,currSegment,trialOutcome,betOption,currentBank,failedBlock))
        
        # update trial number
        currTrial+=1
        RT.reset()
        clock.reset()
        
        # if the participant failed move onto next block instead of next trial
        if failedBlock == True:
            break
     
    #display end prompts
    endPrompts.text = ("Final score: %s\n\nThis is the end of practice. Please tell the researcher that you have finished, and take this opportunity to ask questions if you're unsure of anything in the task."%(currentBank))
    endPrompts.draw()
    win.flip()
    thisKey = event.waitKeys(keyList = expKeys)
    if thisKey == ['escape']:
        print("Practice finished")
        win.close()
        core.quit()


# END OF EXPERIMENT
dataFile.close()

win.close()
core.quit()