#!/usr/bin/env python2
"""Implement the Erikson Flanker Task
described in Eichele 2008 (DOI: 10.1073/pnas.0708965105)"""
"""Timings adjusted according to results from Mattler (2003) DOI: 10.1007/s00221-003-1486-5"""
# Flanker Practice
# Created 1/22/15 by David Jangraw based on NumericalSartTask.py
# Updated 11/9/15 by David Jangraw - cleanup (https://github.com/djangraw/PsychoPyParadigms/blob/master/BasicExperiments/FlankerTask.py)
# Adapted February 2019 by Jade S Pickering and Marta Majewska using PsychoPy v1.90.3
# Last updated 17/06/19 by JSP and MM



from psychopy import core, visual, gui, data, event, sound, logging
from psychopy.tools.filetools import fromFile, toFile
import random, time, csv, numpy as np
#import AppKit # for monitor size detection

# To do:
# Cleanup

# ========================== #
# ===== SET UP LOGGING ===== #
# ========================== #
try:#try to get a previous parameters file
    expInfo = fromFile('lastFlankerParams.pickle')
    expInfo['session'] +=1 # automatically increment session number
except:#if not there then use a default set
    expInfo = {'subject':'1', 'session':1}
dateStr = time.strftime("%b_%d_%H%M", time.localtime())#add the current time


#present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Flanker task', fixed=['date'], order=['subject','session'])
if dlg.OK:
    toFile('lastFlankerParams.pickle', expInfo)#save params to file for next time
else:
    core.quit() #the user hit cancel so exit

participant = expInfo['subject']
sessionNum = expInfo['session']

# New logging
dataFile = open(participant + '_' + dateStr + '.csv', 'w')
writer = csv.writer(dataFile)
writer.writerow(["Participant","Session","BlockNum","TrialNum","FlankerDir","TargetDir","Resp","Trial start","RT"])

# ====================== #
# ======= WINDOW ======= #
# ====================== #

#create window and stimuli
screenRes = [1920,1080] #[1366,786] #define BEAM lab monitor size ([1024,768] in room 1, [1920,1080] in room 2, [1366, 768] at MM)
isFullScreen = False     # run in full screen mode?
screenToShow = 0        # display on primary screen (0) or secondary (1)?

globalClock = core.Clock()#to keep track of time
trialClock = core.Clock()#to keep track of time
win = visual.Window(screenRes, fullscr=isFullScreen, allowGUI=False, monitor='testMonitor', screen=screenToShow, units='deg', name='win')

refreshRate = win.getActualFrameRate()#(nIdentical=75, nMaxFrames=100, nWarmUpFrames=10, threshold =1)
#refreshRate = 60 # change according to PC/monitor being used

# ====================== #
# ===== PARAMETERS ===== #
# ====================== #

# Declare primary task parameters
isPractice = False      # give subject feedback when they get it wrong?
nBlocks = 2             # how many blocks will there be?
nTrialsPerBlock = 8    # how many trials between breaks? must be divisible by 4
blockLengths = [8,8]     # how many trials in each block? The length of this list will be the number of blocks.
randomizeBlocks = True   # scramble the blockLengths list, or perform blocks in order given?

fixDuration = 0.5                 # 500 ms fixation
fixDurF = int(round(refreshRate*fixDuration)) # number of frames the fixation should show for

FFD_min = 0.05            # min delay between fixation and flanker (Fixation-Flanker Delay)
FFD_max = 0.25            #FFD will be between FFD_min and FFD_min + FFD_range (in seconds)
FFD = random.uniform(FFD_min,FFD_max)   # FFD should be between 50-250ms in a rectangular distribution
FFDf = int(round(refreshRate*FFD))

flankerDur = 0.10      # time flanker arrows are onscreen before target (in seconds); aka stimulus-onset asynchrony (SOA)
flankerDurF = int(round(refreshRate*flankerDur))

targetDur = 0.050       # time target arrow is onscreen (in seconds)
targetDurF = int(round(refreshRate*targetDur))

blankDur = 1.500  # # time between target offset and new fixation in which response is recorded (in seconds)
blankDurF = int(round(refreshRate*blankDur))

respRecorded = False
respBlankDur = 0.5 # if a response is given, the blank duration is reduced to move onto the next trial quicker
baseBlankDur = 1.500 # base duration for blank screen whilst waiting for a response

IBI = 0.5                # time between end of block/probe and beginning of next block (in seconds)
IBIf = int(round(refreshRate*IBI))

respKeys = ['z', 'm']   # keys to be used for responses
triggerKey = 't'        # key from scanner that says scan is starting
arrowChars = [u"\u2190", u"\u2192"] # unicode for left and right arrows
rtDeadline = 1.500      # responses after this time will be considered too slow (in seconds)
rtTooSlowDur = 0.600    # duration of 'too slow!' message (in seconds)
#isRtThreshUsed = True   # determine response deadline according to a performance threshold?
nCoherentsAtEnd = 5    # make last few stimuli coherent to allow mind-wandering before probes

# enumerate constants
arrowNames = ['Left','Right']

# randomize list of block lengths
if randomizeBlocks:
    np.random.shuffle(blockLengths)
    
# parameters for trial ratio    
leftCon = 1 #direction of the target + congruency
rightCon = 2
leftIncon = 3
rightIncon = 4
trialChoices = [leftCon, rightCon, leftIncon, rightIncon]  #25% chance of each trial type
trialReps = int(nTrialsPerBlock/4)
trialList = trialChoices*trialReps 

# parameters for block based feedback
RT = 0
blockRTAve = 0
blockAccAve = 0

# ========================== #
# ===== SET UP STIMULI ===== #
# ========================== #

# create window and stimuli
fixation = visual.TextStim(win, pos=[0,0], color='#000000', alignHoriz='center', height=2, name='fixation', text="+")
message1 = visual.TextStim(win, pos=[0,+4], color='#000000', alignHoriz='center', name='topMsg', text="aaa")
message2 = visual.TextStim(win, pos=[0,-4], color='#000000', alignHoriz='center', name='bottomMsg', text="bbb")

# make target arrow
target = visual.TextStim(win,pos=[0,0], color='#000000', alignHoriz='center', height=4, name='target', text = arrowChars[0])
flankers = []
flankerPos = [-4, -2, 2, 4]
for i in range(0,len(flankerPos)):
    flankers.append(visual.TextStim(win,pos=[0,flankerPos[i]], color='#000000', alignHoriz='center', height=4 , name='flanker%d'%(i+1), text = arrowChars[1]))

# make too-slow message
tooSlowStim = visual.TextStim(win, pos=[0,0], color='white', alignHoriz='center', name='tooSlow', text="Missed")

# make correct message
correctStim = visual.TextStim(win, pos=[0,0], color='green', alignHoriz='center', name='correct', text="Correct")

# make incorrect message
incorrectStim = visual.TextStim(win, pos=[0,0], color='red', alignHoriz='center', name='incorrect', text="Incorrect")

# declare list of prompts
topPrompts = ["Keep your eyes on the cross at the center of the screen when it appears. You will then see a series of arrows. "
    "Press %c whenever the MIDDLE arrow points LEFT and %c when it points RIGHT."%(respKeys[0].upper(),respKeys[1].upper()), 
    "Please respond as quickly and accurately as possible."
    ]
bottomPrompts = ["Press any key to continue.        ",
    "Let the experimenter know when you're ready to begin."]
 
endtopPrompts = ["This is the end of practice. Your average reaction time in this block was:\n                    %s ms. \n Your average accuracy was:\n                    %s %%."%(blockRTAve, blockAccAve)]
endbottomPrompts = ["Please tell the experimenter that you finished."]

# ============================ #
# ======= SUBFUNCTIONS ======= #
# ============================ #

def RunTrial(targetDir,flankerDir,tStartTrial):
    global blockRTAve
      
#    totalFrames=fixDurF+FFDf+flankerDurF+targetDurF#+IBIf
    frameN = 0
#    print("total frames: ",totalFrames)

    # display fixation cross
    for frameN in range(fixDurF):
        fixation.draw()
        win.flip()
       
    # get trial time
    tTrial = globalClock.getTime()
#   print(tTrial)
    # reset clock
    trialClock.reset()
        
    #display blank screen
    for frameN in range(FFDf):
        win.flip()
#   print("total frames: ",totalFrames)
        
    # display flankers
    for frameN in range(flankerDurF):
        for flanker in flankers:
            flanker.text = arrowChars[flankerDir]
            flanker.draw()
        win.flip()
#   print("total frames: ",totalFrames)

    event.clearEvents()
    checkResp = 1
    breakTrial = False
    
    # display flankers AND target arrow
    for frameN in range(targetDurF):
        if frameN == 0:
            tStim = trialClock.getTime() # get time when stim was displayed
            event.clearEvents() # flush buffer
        for flanker in flankers:
            flanker.draw()
        target.text = arrowChars[targetDir]
        target.draw()
        win.flip()
        
        # check for a response
        if checkResp == 1:
            allKeys = event.getKeys(timeStamped=trialClock)
            if allKeys == []:
                respRecorded = False
            else:
                respRecorded = True
                breakTrial = True
                checkResp = 0
                        
    if breakTrial == True: #if response is given during target display, there will be only 500 ms blank screen
        blankDur = respBlankDur 
        blankDurF = int(round(refreshRate*blankDur))
    elif breakTrial == False: #otherwise there will be 1500 ms given to respond
        blankDur = baseBlankDur
        blankDurF = int(round(refreshRate*blankDur))    
    
    breakTrial = False # reset so that it doesn't skip the short blank entirely
            
    for frameN in range(blankDurF):
        win.flip()
        # check for a response
        if checkResp == 1:
            allKeys = event.getKeys(timeStamped=trialClock)
            if allKeys == []:
                respRecorded = False
            else:
                respRecorded = True
                breakTrial = True
                checkResp = 0
                break
    if breakTrial == True:
        blankDur = respBlankDur #There is a 500 ms blank after every response within 1500 ms of target onset -> another lvl of RT: during target display, within first 1000 ms, and base
        blankDurF = int(refreshRate*blankDur)
        for frameN in range(blankDurF):
            win.flip()

    event.clearEvents()

    # find RT
    RT = float('Inf')
    for thisKey in allKeys:
        if thisKey[0] in respKeys:
            RT = thisKey[1]-tStim
            break
            
    if respRecorded == True:
        blockRT.extend([RT*1000])
        np.array(blockRT).astype(np.float)
        blockRTAve = int(np.median(blockRT))

    if RT >= rtDeadline:
        print("TooSlow triggered")
        thisResp = False
        tooSlowStim.draw()
        win.logOnFlip(level=logging.EXP, msg='Display TooSlow')
        win.flip()
        core.wait(rtTooSlowDur,rtTooSlowDur)

    # return trial time, response(s)
    return (tTrial,allKeys)
    print("Start and RT: ",tTrial,RT)

# =========================== #
# ======= RUN PROMPTS ======= #
# =========================== #

# display prompts
iProbe = 0
while iProbe < len(topPrompts):
    message1.setText(topPrompts[iProbe])
    message2.setText(bottomPrompts[iProbe])
    #display instructions and wait
    message1.draw()
    message2.draw()
    win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(iProbe+1))
    win.flip()
    #check for a keypress
    thisKey = event.waitKeys()
    if thisKey[0] in ['q','escape']:
        core.quit()
    elif thisKey[0] == 'backspace':
        iProbe = 0
    else:
        iProbe += 1

# do brief wait before first stimulus
for frameN in range(IBIf):
    win.flip()

# =========================== #
# ===== MAIN EXPERIMENT ===== #
# =========================== #

# set up performance variables
wasTarget = False # was the last trial a target?
isCorrect_alltrials = np.zeros(nBlocks*nTrialsPerBlock, dtype=np.bool)
isCongruent_alltrials = np.zeros(nBlocks*nTrialsPerBlock, dtype=np.bool)
RT_alltrials = np.zeros(nBlocks*nTrialsPerBlock)

# set up other stuff
tNextTrial = 0 # to make first trial start immediately
logging.log(level=logging.EXP, msg='---START EXPERIMENT---')

for iBlock in range(0,nBlocks): # for each block of trials
    
    # log new block
    logging.log(level=logging.EXP, msg='Start Block %d'%iBlock)
    nTrialsPerBlock = blockLengths[iBlock]
    
    random.shuffle(trialList)
    print(trialList)
    currTrial = 0   # start with the first item from the shuffled trial list
    
    blockRT = []
    blockAcc = []
    
    for iTrial in range(0,nTrialsPerBlock): # for each trial
        
        trial = trialList[currTrial]   # ready for whichever trial we're on
                        
        # determine trial type
        #flankerDir = (np.random.random() < 0.5)
        #if iTrial>=(nTrialsPerBlock-nCoherentsAtEnd):
        #    targetDir = flankerDir # make last few stims before probe easy, coherent trials
        #else:
        #    targetDir = (np.random.random() < 0.5)
            
        # determine trial type
        if trial == leftCon or trial ==rightIncon:
            flankerDir = 0
        elif trial == rightCon or trial == leftIncon:
            flankerDir = 1
            
        if trial == leftCon or trial ==leftIncon:
            targetDir = 0
        elif trial == rightCon or trial == rightIncon:
            targetDir = 1
        
        # Run Trial
        [tTrial, allKeys] = RunTrial(targetDir,flankerDir,tNextTrial)
        
        # determine next trial time
        #ITI = ITI_min + np.random.random()*ITI_range
        FFD = (random.uniform(FFD_min,FFD_max))
        FFDf = int(round(refreshRate*FFD))
        tNextTrial = tTrial+FFD
        
        # check responses
        keyChar = 0
        RT = np.nan
        for thisKey in allKeys:
            # check for escape keypresses
            if thisKey[0] in ['q', 'escape']:
                core.quit()#abort experiment
            # check for responses
            elif thisKey[0] in respKeys:
                keyChar = thisKey[0] #record key
                RT = thisKey[1]*1000 #in ms
                        
        if keyChar == respKeys[targetDir]: #and RT <= rtDeadline:
            print("Correct triggered")
            thisResp = True # correct
            blockAcc.extend([1])
            correctStim.draw()
            win.logOnFlip(level=logging.EXP, msg='Display Correct')
            win.flip()
            core.wait(rtTooSlowDur,rtTooSlowDur)
        elif keyChar != respKeys[targetDir] and RT >= rtDeadline:
            print("Incorrect triggered")
            thisResp = False # incorrect
            blockAcc.extend([0])
            incorrectStim.draw()
            win.logOnFlip(level=logging.EXP, msg='Display Incorrect')
            win.flip()
            core.wait(rtTooSlowDur,rtTooSlowDur)
        else:
            print ("Trigger failed")
            blockAcc.extend([0]) 
        event.clearEvents('mouse')#only really needed for pygame windows
        
        np.array(blockAcc).astype(np.float)
        blockAccAve = int(round(100*(np.mean(blockAcc))))
        
        # give feedback if this is practice
        if isPractice and thisResp==0:
            message1.setText("Whoops! That was incorrect. Press %c whenever the middle arrow points LEFT and %c when it points RIGHT."%(respKeys[0].upper(),respKeys[1].upper()))
            message2.setText("Press any key to continue.")
            message1.draw()
            message2.draw()
            win.logOnFlip(level=logging.EXP, msg='Display Feedback')
            win.flip()
            core.wait(0.25) # quick pause to make sure they see it
            event.waitKeys()

        currTrial+=1
        tooSlowMsg = False
        
        # Define how to log responses
        if flankerDir == True:
            flankerDirection = 'right'
        else:
            flankerDirection = 'left'
       
        if targetDir == True:
            targetDirection = 'right'
        else:
            targetDirection = 'left'
            
        if keyChar == 'z':
            keyResp = 'left'
        elif keyChar == 'm':
            keyResp = 'right'
        else:
            keyResp = 'miss'
        
        dataFile.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, \n'%(participant,sessionNum,iBlock+1,iTrial+1,flankerDirection,targetDirection, keyResp, tTrial, RT))
        
        #===END TRIAL LOOP===#

    # skip IBI on last block
    if iBlock < (nBlocks-1):
        # Display wait screen
        message1.setText("Take a break! Your average reaction time in this block was:\n                    %s ms.\n Your average accuracy was:\n                    %s %%."%(blockRTAve, blockAccAve))
        message2.setText("Remember to try to respond as QUICKLY yet as ACCURATELY as you can. When you're ready to begin a new block, let the experimenter know.")
        message1.draw()
        message2.draw()
        win.logOnFlip(level=logging.EXP, msg='Display BreakTime')
        win.flip()
        thisKey = event.waitKeys()
        if thisKey[0] in ['q', 'escape']:
            core.quit() #abort experiment
        for frameN in range(IBIf):
            win.flip()
    
#    print(blockRT)

# display end prompts
iEnd = 0
while iEnd < len(endtopPrompts):
    endtopPrompts = ["This is the end of practice. Your average reaction time in this block was:\n                    %s ms. \n Your average accuracy was:\n                    %s %%."%(blockRTAve, blockAccAve)] # update end message
    message1.setText(endtopPrompts[iEnd])
    message2.setText(endbottomPrompts[iEnd])
    message1.draw()
    message2.draw()
    win.logOnFlip(level=logging.EXP, msg='Display End Screen%d'%(iEnd+1))
    win.flip()
    
    #check for a keypress
    thisKey = event.waitKeys()
    if thisKey[0] in ['q','escape']:
        core.quit()
    elif thisKey[0] == 'backspace':
        iProbe = 0
    else:
        iProbe += 1

#give some performance output to user
isC = isCongruent_alltrials!=0
isI = np.logical_not(isCongruent_alltrials)
#print('---Performance:')
#print('All: %d/%d = %.2f%% correct' %(np.nansum(isCorrect_alltrials), len(isCorrect_alltrials), 100*np.nanmean(isCorrect_alltrials)))
#print('Congruent: %d/%d = %.2f%% correct' %(np.nansum(isCorrect_alltrials[isC]), np.nansum(isC), 100*np.nanmean(isCorrect_alltrials[isC])))
#print('Incongruent: %d/%d = %.2f%% correct' %(np.nansum(isCorrect_alltrials[isI]), np.nansum(isI), 100*np.nanmean(isCorrect_alltrials[isI])))
#print('---Reaction Time:')
#print('All: mean = %.4f, std = %.4f' %(np.nanmean(RT_alltrials), np.nanstd(RT_alltrials)))
#print('Congruent: mean = %.4f, std = %.4f' %(np.nanmean(RT_alltrials[isC]), np.nanstd(RT_alltrials[isC])))
#print('Incongruent: mean = %.4f, std = %.4f' %(np.nanmean(RT_alltrials[isI]), np.nanstd(RT_alltrials[isI])))

# exit experiment
core.quit()