################################################################################
# Programmed by Jade S Pickering and Marta Majewska (March, 2019)              #
# Using PsychoPy v1.90.3                                                       #
################################################################################

# Import libraries
from psychopy import core, visual, gui, data, event, logging
#from psychopy.tools.filetools import fromFile, toFile, os, sys
import random, time, csv, numpy as np



# ====================== #
# ==== DIALOGUE BOX ==== #
# ====================== #

# create a DlgFromDict
info = {
    'Participant ID': '',                       # participant number
    }
infoDlg = gui.DlgFromDict(
    dictionary=info,
    title='Please set parameters', 
    order=['Participant ID'],
    )
if infoDlg.OK: #this will be True (user hit OK) or False (cancelled)
    print(info)
else:
    print('User Cancelled')

# Create window
win = visual.Window(
    #[800,600],          # debug mode
    #fullscr = False,    # debug mode
    [1920,1080],         # exp mode
    fullscr= True,      # exp mode
    allowGUI = False,
    units = "norm",
    monitor = "testMonitor"
    )


# ====================== #
# ===== PARAMETERS ===== #
# ====================== #
refreshRate = win.getActualFrameRate()#(nIdentical=75, nMaxFrames=100, nWarmUpFrames=10, threshold =1)
#refreshRate = 60 # change according to PC/monitor being used
nConditions = 2 # 2
#nBlocks = 2
#nTrials = 6  # per block - must be divisible by 6
nBlocks = 4     #
nTrials = 90    # per block - must be divisible by 6
respKeys = ['space', 'escape'] # allowable stimuli response keys
expKeys = ['return','escape']      # allowable break screen keys
stimPos= [0,0]
go1 = 'A'
go2 = 'E'
go3 = 'I'
go4 = 'O'
go5 = 'U'
nogo = 'K'
stimHeight = 250
stimColor = 'black'
fixation = '+'
fixColor = 'white'
fixHeight = 100         # fixation needs to be slightly smaller than stimulus
fixDuration = 0.5       # fixation should remain on screen for 500ms
fixDurF = int(round(refreshRate*fixDuration)) # number of frames the fixation should show for
textHeight = 40   # size of text in pixels
textWrap = 1000 # how many pixels across the screen the text should run before continuing on new line
ISImin = 0.25
#ISIminF = (refreshRate*ISImin) # number of minimum frames for the ISI
ISImax = 0.5
#ISImaxF = (refreshRate*ISImax) # number of maximum frames for the ISI
#ISI = int(round(random.uniform(ISIminF,ISImaxF)))   # ISI in a rectangular distribution
ISI = random.uniform(ISImin,ISImax)
ISIF = int(round(refreshRate*ISI))
stimDuration = 0.15
stimDurF = int(round(refreshRate*stimDuration))
blankDuration = 1.5
blankDurF = int(round(refreshRate*blankDuration))
trialChoices = [go1, go2, go3, go4, go5, nogo]  #20% chance of nogo
trialReps = nTrials/6   #the amount of times each trial will repeat will depend how many total trials we want
participant = info['Participant ID']
trialList = trialChoices*trialReps #this will multiply the current trialChoices so that we have the correct number of trials according to the proportion of Go and NoGo that we want as well as the total trials required
respTime = 0


# ========================== #
# ===== SET UP LOGGING ===== #
# ========================== #

trialClock = core.Clock()
dateStr = time.strftime("%b_%d_%H%M", time.localtime())#add the current time

dataFile = open(participant + '_' + dateStr + '.csv', 'w')
writer = csv.writer(dataFile)
writer.writerow(["participant","condition","blockNum","trialNum","trialType","ISI","trial start", "keytime", "trialRT", "trialAcc"])



# ========================== #
# ===== CREATE STIMULI ===== #
# ========================== #


# Instruction text
instructions = visual.TextStim(
            win,
            units='pix',
            wrapWidth=textWrap,
            height=textHeight,
            text="Your goal in this task is to respond to some letters on the screen whilst not responding to others.\n\nIf you see one of the vowels (%s, %s, %s, %s, or %s) you must press the SPACEBAR. However, if you see the letter %s you must not press anything at all. Each letter will appear quite quickly and you'll have a very limited amount of time to make your decision as to whether you should press the SPACEBAR. Please aim to respond as QUICKLY and as ACCURATELY as you can\n\nPress ENTER to continue."%(go1, go2, go3, go4, go5, nogo),
            )

# practice text
practiceText = visual.TextStim(
            win,
            units='pix',
            wrapWidth=textWrap,
            height=textHeight,
            text="We will now have a practice run. Tell the researcher when you are ready to begin."
            )

# Break screen text
breakScreen = visual.TextStim(
            win,
            units='pix',
            wrapWidth=textWrap,
            height=textHeight,
            text="End of block. Please take this opportunity for a break and then tell the researcher when you are ready to continue.",
            )

# End screen text
endScreen = visual.TextStim(
            win,
            units='pix',
            wrapWidth=textWrap,
            height=textHeight,
            text="End of task - thank you!\n\nPlease tell the researcher that you have finished.",
            )

#  setting up Go stimulus
goStim = visual.TextStim(
        win,
        units='pix',
        pos=stimPos,
        text=go1,       #placeholder as this will update throughout  the task
        height=stimHeight,
        color=stimColor
        )

# setting up No-Go stimulus
nogoStim = visual.TextStim(
        win,
        units='pix',
        pos=stimPos,
        text=nogo,
        height=stimHeight,
        color=stimColor
        )

# setting up fixation stimulus
fixationStim = visual.TextStim(
        win,
        units='pix',
        pos=stimPos,
        text=fixation,
        height = fixHeight,
        color=fixColor
        )


# ========================== #
# ======= EXPERIMENT ======= #
# ========================== #

# Initial instruction screen

instructions.draw() # PsychoPy prepares stimulus
win.flip()          # PsychoPy updates the screen when stimulus is ready to prevent tears

thisKey = event.waitKeys(keyList = expKeys) #psychopy waits for a key press before moving on
if thisKey == ['escape']:
    print("Warning: Session aborted by user")
    win.close()
    core.quit()


#WHEN FINISHED WITH MAIN EXP, COPY AND PASTE INTO HERE.

# BLOCK LOOP STARTS HERE
for iBlock in range (0,nBlocks):

    random.shuffle(trialList)
    currTrial = 0   # start with the first item from the shuffled trial list

    # TRIAL LOOP STARTS HERE
    for iTrial in range (0,nTrials):
               
        trial = trialList[currTrial]   # ready for whichever trial we're on
        respRecorded = False
        
        ISI = random.uniform(ISImin,ISImax)
        ISIF = int(round(refreshRate*ISI))
        #ISI = int(round(random.uniform(ISIminF,ISImaxF)))   # update ISI
        totalFrames=fixDurF+ISIF+stimDurF+blankDurF
        frameN = 0
        #print("total frames: ",totalFrames)

        # display fixation cross
        for frameN in range(fixDurF):
            fixationStim.draw()
            win.flip()

        # update stimulus text
        goStim.text = trial

        #display blank ISI
        for frameN in range(ISIF):
            win.flip()
        
        #print("Trial start time: ", trialStart)
        # clear buffer of any keyboard presses
        event.clearEvents()
        checkResp = 1
        
        #start timing for RT
        trialClock.reset()
        
        # display stimulus and check for responses
        for frameN in range(stimDurF):
            
            if frameN == 0:
                trialStart = trialClock.getTime()
                print(trialStart)

            goStim.draw()
            win.flip()

            if checkResp == 1:
                trialResp = event.getKeys(keyList = respKeys)
                if trialResp == []:
                    respRecorded = False
                elif trialResp[0] == 'space': # if spacebar is pressed
                    respRecorded = True
                    checkResp = 0
                    respTime = trialClock.getTime()     # time at which response was recorded
                    #print("Response time; ", respTime)
                    #print("Response recorded: ", respRecorded)
                elif trialResp[0] == 'escape':  # if escape key is pressed
                    print("Warning: Session aborted by user")
                    win.close()
                    core.quit()

        # display blank ITI and check for responses
        for frameN in range (blankDurF):
            win.flip()

            if checkResp == 1:
                trialResp = event.getKeys(keyList = respKeys)
                if trialResp == []:
                    respRecorded = False
                elif trialResp[0] == 'space': # if spacebar is pressed
                    respRecorded = True
                    checkResp = 0
                    respTime = trialClock.getTime()     # time at which response was recorded
                    #print("Response time; ", respTime)
                    #print("Response recorded: ", respRecorded)
                elif trialResp[0] == 'escape':  # if escape key is pressed
                    print("Warning: Session aborted by user")
                    win.close()
                    core.quit()

        event.clearEvents    # clear the buffer
        # assess the response
        if respRecorded == True:
            RT = respTime - trialStart
            #print(RT)
            trialRT = RT *1000
            if trial == nogo: # determine accuracy and RT
                trialAcc = 0
            else:
                trialAcc = 1
        elif respRecorded == False:
            trialRT = 'NaN'
            if trial == nogo:
                trialAcc = 1
            else:
                trialAcc = 'miss'
            # classify as a missed trial or correct NoGo and put in NaN for trialRT


        # technical info
        print("Frame rate: ",refreshRate," Total frames in trial: ", totalFrames,"Trial start time: ",trialStart," Response time: ",respTime," Response recorded: ",respRecorded)
        # output info
        print("Block number: ",iBlock," Trial number: ",iTrial," Current Trial: ",trial," ISI: ",ISI*1000,"Trial accuracy: ",trialAcc, "Trial RT: ",trialRT)


        if trial == nogo:
            condition = 0
        else:
            condition = 1

        # PLACEHOLDERS for data output info
        currISI = ISI*1000

        # write all data to file
        dataFile.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n'%(participant,condition,iBlock+1,currTrial+1, trial, currISI, trialStart, respTime, trialRT, trialAcc))


        currTrial+=1

    # draw a break screen if the experiment hasn't finished, and an end screen if it has
    if iBlock < nBlocks-1:
        breakScreen.draw()
        win.flip()
        thisKey = event.waitKeys(keyList = expKeys)
        if thisKey == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()
    elif iBlock == nBlocks-1:
        endScreen.draw()
        win.flip()
        thisKey = event.waitKeys(keyList = expKeys)
        if thisKey == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()


win.close()
core.quit()
