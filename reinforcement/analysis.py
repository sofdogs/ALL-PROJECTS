# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2a():
    """
      Prefer the close exit (+1), risking the cliff (-10).
    """
    answerDiscount = 1 # no discount so we don't consider further out paths
    answerNoise = 0 # want pacman to go straight to exit, don't want him to accidentally go into cliff because of noise
    answerLivingReward = -2 # penalize pacman for living, we want him to exit as soon as possible
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question2b():
    """
      Prefer the close exit (+1), but avoiding the cliff (-10).
    """
    #want moves to be < 9 but > 5 (bot to +10)
    answerDiscount = .2 # don't want pacman to go to longer +10 exit, need discount
    answerNoise = .1 # don't want pacman to deviate from path & go to unexpected route (off cliff / down cliff route)
    answerLivingReward = .5 #reward for going longer path, must make it worth it to take longer path to 1.0 instead of shorter cliff to 10.0, but not worthwhile to go down longer path up top to +10
    return answerDiscount, answerNoise, answerLivingReward
    

def question2c():
    """
      Prefer the distant exit (+10), risking the cliff (-10).
    """
    #take between 5-6 moves
    answerDiscount = 1 #we want the agent to make it to the further exit, we don't want it to see +1 as more profitable because of the discount
    answerNoise = 0 #no alternate path, all will lead off cliff if we are along it
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question2d():
    """
      Prefer the distant exit (+10), avoiding the cliff (-10).
    """
    answerDiscount = .9
    answerNoise = 0.5
    answerLivingReward = -.2
    #return 'NOT POSSIBLE'
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question2e():
    """
      Avoid both exits and the cliff (so an episode should never terminate).
    """
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = 200 #we want the reward for living a unit of time to be higher than any exit reward so we will never chose to exit with +10
    #answerDiscount = 0
    # answerNoise = 0
    # answerLivingReward = 0
    
    return answerDiscount, answerNoise, answerLivingReward
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'


if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
