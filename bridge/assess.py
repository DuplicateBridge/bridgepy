""" Perform assessment on random deals """

import numpy as np

from IPython import embed

# Format
# [card, min_n1, max_n1, hand]

def test_deals(deals:np.ndarray, n1:np.ndarray,
               query:list):

    # Slice
    final = np.ones(deals.shape[0], dtype=bool)
    for item in query:
        # Is it multiple?
        if isinstance(item, list):
            # Loop on items
            sub_final = np.zeros(deals.shape[0], dtype=bool)
            for subitem in item:
                # Parse
                qdict = parse_query(subitem)
                # Query
                assess = query_deals(deals, n1, qdict)
                sub_final |= assess
        else:
            # Parse
            qdict = parse_query(item)
            # Query
            assess = query_deals(deals, n1, qdict)
            sub_final = assess
        # Combine
        final &= sub_final
    # Return
    return final

def parse_query(query:list):
    # Parse
    card, min_n, max_n, hand = query
    # Build a dict
    qdict = dict()
    qdict['card'] = card
    qdict['min_n'] = min_n
    qdict['max_n'] = max_n
    qdict['hand'] = hand
    return qdict

def query_deals(deals:np.ndarray, n1:np.ndarray,
               qdict:dict):

    # Prep
    ntot = deals.shape[1]
    n2 = ntot - n1

    # Build hands
    if qdict['hand'] == 1:
        n = n1
    else:
        n = n2

    # Good hands
    gdi = (n >= qdict['min_n']) & (n <= qdict['max_n'])
    hands = []
    for ii in np.where(gdi)[0]:
        if qdict['hand'] == 1:
            hands.append(deals[ii,0:n1[ii]])
        else:
            hands.append(deals[ii,n1[ii]:])

    # Query
    in_hand = [qdict['card'] in hand for hand in hands]
    #embed(header='assess.query_deals 48')

    # Finish assessment
    assess = np.zeros(deals.shape[0], dtype=bool)
    assess[gdi] = in_hand

    return assess
        
    