################################################################################
# Programmed by Jade S Pickering and Marta Majewska (June, 2019)               #
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
    [1920,1080],         # exp mode
    #[800,600],          # debug mode
    color = "black",
    #fullscr = False,    # debug mode
    fullscr= True,      # exp mode
    allowGUI = False,
    units = "norm",
    monitor = "testMonitor"
    )



# ====================== #
# ===== PARAMETERS ===== #
# ====================== #
refreshRate = win.getActualFrameRate()
nConditions = 2 # 2
#nBlocks = 2     # 
#nTrials = 8    # per block, must be divisible by 8
nBlocks = 4
nTrials = 96    # per block, must be divisible by 8
respKeys = ['z', 'm', 'escape'] # allowable stimuli response keys
expKeys = ['return','escape']      # allowable break screen keys
stimPos= [0,0]
goStimWidth = 15
goStimSize = 600
goColor = '#50f442'
posVert = 0.175
negVert = -0.175
leftVert = ((posVert, posVert), (negVert, 0), (posVert,negVert))
rightVert = ((negVert, posVert), (posVert, 0), (negVert, negVert))
stopStimSize = 650
stopColor = '#fc0000'
innerBlockSize = 600
fixColor = '#d3d3d3'
fixSize = 175
fixWidth = 5
fixDuration = 0.5       # fixation should remain on screen for 500ms
fixDurF = int(round(refreshRate*fixDuration)) # number of frames the fixation should show for
ISImin = 0.25
ISImax = 0.5
goDuration = 0.07 # duration of go signal
goDurF = int(round(refreshRate*goDuration))
stopDuration = 0.07 # duration of stop signal
stopDurF = int(round(refreshRate*stopDuration))
baseBlankDuration = 1.5 # base duration for blank screen whilst waiting for a response
shortBlankDur = 0.5 # if a response is given, the blank duration is reduced to move onto the next trial quicker
blankDuration = baseBlankDuration # time allowed for a response
blankDurF = int(round(refreshRate*blankDuration))
#trialReps = nTrials/8   # older ver: the amount of times each trial will repeat will depend how many total trials we want
trialReps = int(nTrials/8) # newer ver: needs to be int of type 'float' for further operations
participant = info['Participant ID']
startSSD = 0.205 # starting point for SSD which will go up or down in steps of 50ms depending on participant response
stepSize = 0.050 # SSD will increase/decrease by 50ms each stop trial
leftSSD = startSSD
rightSSD = startSSD
minSSD = 0.005
maxSSD = 1.506
leftGo = 1
rightGo = 2
leftStop = 3
rightStop = 4
trialChoices = [rightGo, rightGo, rightGo, leftGo, leftGo, leftGo, rightStop, leftStop]  #25% chance of stop trial
trialList = trialChoices*trialReps #older version

# placeholders
ISI = random.uniform(ISImin,ISImax)   # ISI should be  in a rectangular distribution
ISIF = int(round(refreshRate*ISI))
currSSD = startSSD
currSSDF = int(round(refreshRate*currSSD))
RT = 'NaN'
trialRT = 'NaN'
trialAcc = 0
checkResp = 1
respRecorded = False
respTime = 0
blockRTAve = 0

# ========================== #
# ===== SET UP LOGGING ===== #
# ========================== #

trialClock = core.Clock()

dateStr = time.strftime("%b_%d_%H%M", time.localtime())#add the current time
dataFile = open(participant + '_' + dateStr + '.csv', 'w')

writer = csv.writer(dataFile)
writer.writerow(["participant","condition", "trialType", "keyPressed","blockNum","trialNum","ISI","SSD","trialStart", "respTime","trialRT","trialAcc"])

# ========================== #
# ===== CREATE STIMULI ===== #
# ========================== #

# Instruction text
instructions = visual.TextStim(
            win,
            height=0.07,
            text="When you see a leftward arrow, press the left button.\nWhen you see a rightward arrow, press the right button.\nWhen you see the red square, withhold your response.\n\nPlease aim to be as QUICK yet as ACCURATE as you can and DO NOT wait to see if the square appears.\n\nPlease tell the researcher when you are ready to begin.",
            )

# practice text
practiceText = visual.TextStim(
            win,
            height=0.07,
            text="We will now have a practice run. Tell the researcher when you are ready to begin."
            )


# Break screen text
breakScreen = visual.TextStim(
            win,
            height=0.07,
            text="End of block. Your average reaction time for the last block was: \n"
            )


# End screen text
endScreen = visual.TextStim(
            win,
            height=0.07,
            text="End of task - thank you!\n\nPlease tell the researcher that you have finished.",
            )

# Go stimulus
goStim = visual.ShapeStim(
        win,
        units='pix',
        lineWidth=goStimWidth,
        lineColor=goColor,
        vertices=rightVert,
        closeShape=False,
        pos=stimPos,
        size=goStimSize
        )

# Stop stimulus
stopSignalStim = visual.Rect(
        win,
        units="pix",
        size = stopStimSize,
        lineColor=stopColor,
        fillColor=stopColor,
        pos=stimPos
        )

# Hidden inner block so that the square looks neater
innerBlock = visual.Rect(
        win,
        units="pix",
        size = innerBlockSize,
        lineWidth=0,
        lineColor="black",
        fillColor='black',
        pos=stimPos
        )      


# Fixation stimulus
fixationStim1 = visual.ShapeStim(
            win,
            units='pix',
            lineWidth = fixWidth,
            lineColor=fixColor,
            vertices = ((-0.2,0),(0.2,0)),
            closeShape = False,
            pos=stimPos,
            size = fixSize)

fixationStim2 = visual.ShapeStim(
            win,
            units='pix',
            lineWidth = fixWidth,
            lineColor=fixColor,
            vertices = ((0,0.2),(0,-0.2)),
            closeShape = False,
            pos=stimPos,
            size = fixSize)
           

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

# BLOCK LOOP STARTS HERE
for iBlock in range (0,nBlocks):
    
    random.shuffle(trialList)
    currTrial = 0   # start with the first item from the shuffled trial list
    blockRT = []
    stopAcc = []
    
    # TRIAL LOOP STARTS HERE
    for iTrial in range (0,nTrials):
        
        trial = trialList[currTrial]   # ready for whichever trial we're on
        respRecorded = False
        
        if trial == leftGo or trial == leftStop:
            currSSD = leftSSD 
        elif trial == rightGo or trial == rightStop:
            currSSD = rightSSD
            
        currSSDF = int(round(refreshRate*currSSD))
        ISI = random.uniform(ISImin,ISImax)
        ISIF = int(round(refreshRate*ISI))
        frameN = 0
        
        # display fixation cross       
        for frameN in range(fixDurF):
            fixationStim1.draw()
            fixationStim2.draw()
            win.flip()
        
        #display blank ISI
        for frameN in range(ISIF):
            win.flip()
        
        
        # update go stim text depending on trial type
        if trial == leftGo or trial ==leftStop:
            goStim.vertices = leftVert
        elif trial == rightGo or trial == rightStop:
            goStim.vertices = rightVert
            
        # clear buffer of any keyboard presses
        event.clearEvents()
        checkResp = 1
        breakTrial = False
        
        #start timing for RT
        trialClock.reset()
        
        if trial == leftGo or trial == rightGo:
            condition = 'go'
            for frameN in range(goDurF):
                if frameN == 0:
                    trialStart = trialClock.getTime()
                    print(trialStart)
                
                # display Go signal
                goStim.draw()
                win.flip()
                
                # check for a response
                if checkResp == 1:
                    trialResp = event.getKeys(keyList = respKeys)
                    if trialResp == []:
                        respRecorded = False
                    elif trialResp[0] == 'z':
                        respRecorded = True
                        breakTrial = True
                        checkResp = 0
                        respTime = trialClock.getTime()
                    elif trialResp[0] == 'm':
                        respRecorded = True
                        breakTrial = True
                        checkResp = 0
                        respTime = trialClock.getTime()
                    elif trialResp[0] == 'escape':
                        print("Warning: Session aborted by user")
                        win.close()
                        core.quit()
                        
            
            
            if breakTrial == True:
                blankDuration = shortBlankDur
                blankDurF = int(round(refreshRate*blankDuration))
            elif breakTrial == False:
                blankDuration = baseBlankDuration
                blankDurF = int(round(refreshRate*blankDuration))
            
            breakTrial = False # reset so that it doesn't skip the short blank entirely
            
            for frameN in range(blankDurF):
                win.flip()
                
                # check for a response
                if checkResp == 1:
                    trialResp = event.getKeys(keyList = respKeys)
                    if trialResp == []:
                        respRecorded = False
                    elif trialResp[0] == 'z':
                        respRecorded = True
                        breakTrial= True
                        checkResp = 0
                        respTime = trialClock.getTime()
                        break
                    elif trialResp[0] == 'm':
                        respRecorded = True
                        breakTrial = True
                        checkResp = 0
                        respTime = trialClock.getTime()
                        break
                    elif trialResp[0] == 'escape':
                        print("Warning: Session aborted by user")
                        win.close()
                        core.quit()
            
            
            
            if breakTrial == True:
                blankDuration = shortBlankDur
                blankDurF = int(round(refreshRate*blankDuration))
                for frameN in range(blankDurF):
                    win.flip()
            elif breakTrial == False:
                blankDuration = baseBlankDuration
                blankDurF = int(round(refreshRate*blankDuration))
        
            
            
        elif trial == leftStop or trial == rightStop:
            condition = 'stop'
            for frameN in range(goDurF+currSSDF+stopDurF):
                if frameN == 0:
                    trialStart = trialClock.getTime()
                    print(trialStart)
                
                # display Go signal
                if frameN <= goDurF:
                    goStim.draw()
                
                # display Stop signal
                if frameN > currSSDF:
                    if frameN < currSSDF+stopDurF:
                        stopSignalStim.draw()
                        innerBlock.draw()
                        stopOnset = trialClock.getTime()
                        print(stopOnset)
                       
                win.flip()
                
                # check for a response        
                if checkResp == 1:
                    trialResp = event.getKeys(keyList = respKeys)
                    if trialResp == []:
                        respRecorded = False
                    elif trialResp[0] == 'z':
                        respRecorded = True
                        breakTrial = True
                        checkResp = 0
                        respTime = trialClock.getTime()
                    elif trialResp[0] == 'm':
                        respRecorded = True
                        breakTrial = True
                        checkResp = 0
                        respTime = trialClock.getTime()
                    elif trialResp[0] == 'escape':
                        print("Warning: Session aborted by user")
                        win.close()
                        core.quit()
            
                
            
            if breakTrial == True:
                blankDuration = shortBlankDur
                blankDurF = int(round(refreshRate*blankDuration))
            elif breakTrial == False:
                blankDuration = baseBlankDuration
                blankDurF = int(round(refreshRate*blankDuration))
            
            breakTrial = False # reset so that it doesn't skip the short blank entirely
            
            for frameN in range(blankDurF):
                win.flip()
                
                # check for a response        
                if checkResp == 1:
                    trialResp = event.getKeys(keyList = respKeys)
                    if trialResp == []:
                        respRecorded = False
                    elif trialResp[0] == 'z':
                        respRecorded = True
                        breakTrial = True
                        checkResp = 0
                        respTime = trialClock.getTime()
                        break
                    elif trialResp[0] == 'm':
                        respRecorded = True
                        breakTrial = True
                        checkResp = 0
                        respTime = trialClock.getTime()
                        break
                    elif trialResp[0] == 'escape':
                        print("Warning: Session aborted by user")
                        win.close()
                        core.quit()
            
            
            
            if breakTrial == True:
                blankDuration = shortBlankDur
                blankDurF = int(round(refreshRate*blankDuration))
                for frameN in range(blankDurF):
                    win.flip()
            elif breakTrial == False:
                blankDuration = baseBlankDuration
                blankDurF = int(round(refreshRate*blankDuration))
        
            
            
        event.clearEvents()
        
        # check whether a response was correct or not
        if respRecorded == True:
            RT = respTime - trialStart
            trialRT = RT*1000
            if trial == leftGo:
                if trialResp[0] == 'z':
                    trialAcc = "correct"
                elif trialResp[0] == 'm':
                    trialAcc = "wrong arrow"
            elif trial == rightGo:
                if trialResp[0] == 'm':
                    trialAcc = "correct"
                elif trialResp[0] == 'z':
                    trialAcc = "wrong arrow"
            elif trial == leftStop or trial == rightStop:
                trialAcc = "failed stop"
        elif respRecorded == False:
            trialRT = 'NaN'
            if trial == leftGo or trial == rightGo:
                trialAcc = "missed"
            if trial == leftStop or trial == rightStop:
                trialAcc = "successful stop"
                
        
        if trialResp == []:
            keyPress = 0
        elif trialResp[0] == 'm':
            keyPress = 'm'
        elif trialResp[0] == 'z':
            keyPress = 'z'
        
        # technical info
        print("Frame rate: ",refreshRate,"Trial start time: ",trialStart," Response time: ",respTime," Response recorded: ",respRecorded)
        # output info
        print("Block number: ",iBlock," Trial number: ",iTrial," Current Trial: ",trial," ISI: ",ISI*1000," SSD: ", currSSD," Trial accuracy: ",trialAcc, " Trial RT: ",trialRT)
        
        # info for block based feedback
        if respRecorded == True:
            blockRT.extend([trialRT])
        print(blockRT)
        
        if trialAcc == "failed stop":
            stopAcc.extend([0])
        elif trialAcc == "successful stop":
            stopAcc.extend([1])
        print("Stop accuracy: ",stopAcc)
        
        
        currISI = ISI*1000
        
        # write all data to file
        dataFile.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \n'%(participant,condition,trial,keyPress,iBlock+1,currTrial+1, currISI, currSSD*1000, trialStart,respTime,trialRT, trialAcc))



        # updates the left and right SSD depending on accuracy UNLESS the minimum and maximum values have been reached
        if currSSD > minSSD and currSSD < maxSSD:
            if trialAcc == 'successful stop':
                if trial == rightStop:
                    rightSSD = (currSSD + stepSize)
                elif trial == leftStop:
                    leftSSD = (currSSD + stepSize)
            elif trialAcc == 'failed stop':
                if trial == rightStop:
                    rightSSD = (currSSD - stepSize)
                elif trial == leftStop:
                    leftSSD = (currSSD - stepSize)
        elif currSSD < 0.05:
            if trialAcc == 'successful stop':
                if trial == rightStop:
                    rightSSD = (currSSD + stepSize)
                elif trial == leftStop:
                    leftSSD = (currSSD + stepSize)
            elif trialAcc == 'failed stop':
                if trial == rightStop:
                    rightSSD = currSSD
                elif trial == leftStop:
                    leftSSD = currSSD
        elif currSSD > 1.46:
            if trialAcc == 'successful stop':
                if trial == rightStop:
                    rightSSD = currSSD
                elif trial == leftStop:
                    leftSSD = currSSD
            elif trialAcc == 'failed stop':
                if trial == rightStop:
                    rightSSD = (currSSD - stepSize)
                elif trial == leftStop:
                    leftSSD = (currSSD - stepSize)
        
        
        # reset for next trial
        currSSDF = int(round(refreshRate*currSSD))
        checkResp = 1
        blankDuration = baseBlankDuration
        blankDurF = int(round(refreshRate*blankDuration))
        #trialResp = 'none'
        
        # move onto next trial
        currTrial+=1
        
    # draw a break screen if the experiment hasn't finished, and an end screen if it has
    
    np.array(blockRT).astype(np.float)
    print("Changed to floats: ",blockRT)
    blockRTAve = int(np.median(blockRT))
    print("Median RT: ",blockRTAve)
    
    np.array(stopAcc).astype(np.float)
    print("Changed stopAcc to floats: ",stopAcc)
    stopAccAve = 100*(np.mean(stopAcc))
    print("Average stop accuracy: ",stopAccAve)
    
    if stopAccAve <= 40:
        accuracyFeedback = "Remember to try and stop yourself from pressing the button when you see the red square"
    elif stopAccAve >40 and stopAccAve <60:
        accuracyFeedback = "Remember to keep responding as QUICKLY yet as ACCURATELY as you can"
    elif stopAccAve >= 60:
        accuracyFeedback = "Remember to try to respond to the arrows quickly without waiting to see if the red square appears"
    print("Accuracy feedback: ",accuracyFeedback)    
       
    if iBlock < nBlocks-1:

        breakScreen.text = "End of block. Your average reaction time for the last block was: \n%sms.\n\n%s\n\nPlease tell the researcher when you are ready to continue."%(blockRTAve,accuracyFeedback)
        breakScreen.draw()
        win.flip()
        
        thisKey = event.waitKeys(keyList = expKeys)
        if thisKey == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()
            
    elif iBlock == nBlocks-1:
        endScreen.text = "End of task - thank you!\n\n Your average reaction time for the last block was: \n%sms.\n\nPlease tell the researcher that you have finished."%(blockRTAve)
        endScreen.draw()
        win.flip()
        thisKey = event.waitKeys(keyList = expKeys)
        if thisKey == ['escape']:
            print("Warning: Session aborted by user")
            win.close()
            core.quit()

win.close()
core.quit()
