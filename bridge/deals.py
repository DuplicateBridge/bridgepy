""" Methods related to dealing out cards randomly """

import numpy as np

from math import factorial

def vacant(n1:int, n2:int, ninit:tuple=(13,13)):
    """ Probability of n1 cards in hand 1 and n2 cards in hand 2

    Args:
        n1 (int): Number of cards in hand 1
        n2 (int): Number of cards in hand 2
        ninit (tuple, optional): _description_. Defaults to (13,13).

    Returns:
        float: Probability of n1 cards in hand 1 and n2 cards in hand 2
    """
    prob = 1.
    # Fill in hand 1
    count1=0
    while(count1 < n1):
        prob *= (ninit[0]-count1) / (ninit[0]+ninit[1]-count1)
        count1 += 1
    # Now hand 2
    count2=0
    while(count2 < n2):
        prob *= (ninit[1]-count2) / (ninit[0]+ninit[1]-count1-count2)
        count2 += 1
    # Return
    return prob

def all_probs(ntot:int):
    # Iterate
    ncards = []
    probs = []
    for n1 in range(ntot+1):
        n2 = ntot - n1
        #prob = vacant(n1, n2)
        prob = Pab(n1, n2)
        # Save
        ncards.append(n1)
        probs.append(prob)
    # Return
    return ncards, probs

def Pab(a:int,b:int,nhands:tuple=(13,13)):
    # First term
    fter = factorial(a+b)/factorial(a)/factorial(b)
    # Second term, numerator
    num = factorial(nhands[0])*factorial(nhands[1])*factorial(nhands[0]+nhands[1]-a-b)
    # Second term, denumerator
    den = factorial(nhands[0]+nhands[1])*factorial(nhands[0]-a)*factorial(nhands[1]-b)
    # Return
    return fter * num / den

def random_ncards(ntot:int, Ndeals:int):

    # Random numbers
    r = np.random.uniform(size=Ndeals)

    _, probs = all_probs(ntot)
    cum_prob = np.cumsum(probs)

    # Init to total
    n1 = np.ones(Ndeals, dtype=int)*ntot

    # Fill in
    for kk in range(ntot):
        if kk == 0:
            cprob0 = 0.
        else:
            cprob0 = cum_prob[kk-1]
        cprob1 = cum_prob[kk]
        # Find
        gd = (r >= cprob0) & (r < cprob1)
        n1[gd] = kk

    # Return
    return n1