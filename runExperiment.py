import numpy as np
import pygame
from tqdm import tqdm
from time import sleep

INSTRUCTION_TRACKS = [None, None, None]

def playInstructions(type):
    # Spend 5 seconds reading instructions for what to do in this trial:
    WAIT_TIME_SEC = 5.0
    INSTRUCTION_TRACKS[type].play()
    sleep(5.0)

# Given an ordering of types, make sure it follows the rules.
def validTypeOrder(typeOrder):
    # Each pair order must appear the same number of times
    pairCounts = np.zeros((3, 3))
    for i in range(0, len(typeOrder)):
        pairCounts[typeOrder[i - 1], typeOrder[i]] += 1
    if np.max(pairCounts) != np.min(pairCounts):
        return False

    # Can at most have 3 in a row
    MAX_RUN_LENGTH = 3
    maxRun, at = 0, 0
    while at < len(typeOrder):
        runStart = at
        runFirst = typeOrder[at]
        while at < len(typeOrder) and typeOrder[at] == typeOrder[runStart]:
            at += 1
        maxRun = max(maxRun, at - runStart)
    if maxRun > MAX_RUN_LENGTH:
        return False

    return True

# Generate order of types, by randomly shuffling until we get a valid one:
def generateOrder(seed=1234):
    np.random.seed(seed)
    EACH_PAIR_TIMES = 11
    EACH_TYPE_TIMES = EACH_PAIR_TIMES * 3

    typeOrder = np.concatenate([
        0 * np.ones(EACH_TYPE_TIMES, dtype=np.int),
        1 * np.ones(EACH_TYPE_TIMES, dtype=np.int),
        2 * np.ones(EACH_TYPE_TIMES, dtype=np.int),
    ])
    while not validTypeOrder(typeOrder):
        typeOrder = np.random.permutation(typeOrder)
    return typeOrder

# Runs a single trial, save results
def runTrial(trialNumber, trialType):
    playInstructions(trialType)

# Run all the trials
def runExperiment():
    # HACK
    subjectID = "1"
    typeOrder = generateOrder()

    print("Subject : %s" % (subjectID))
    print("Trial   : %s" % ("".join(map(str, typeOrder))))

    # TODO - add pauses?
    # for trial in tqdm(range(len(typeOrder))):
    for trial in tqdm(range(3)):
        runTrial(trial, typeOrder[trial])

# Initialize dependencies
def init():
    global INSTRUCTION_TRACKS

    # Used for playing sounds.
    print ("Initializing...")
    pygame.init()
    pygame.mixer.init()

    # From https://text-to-speech-demo.mybluemix.net/
    # HACK: need better?
    INSTRUCTION_TRACKS[0] = pygame.mixer.Sound("/home/pat/code/python/eegbci/audio/commands/0.wav")
    INSTRUCTION_TRACKS[1] = pygame.mixer.Sound("/home/pat/code/python/eegbci/audio/commands/1.wav")
    INSTRUCTION_TRACKS[2] = pygame.mixer.Sound("/home/pat/code/python/eegbci/audio/commands/2.wav")


if __name__ == "__main__":
    init()
    runExperiment()
