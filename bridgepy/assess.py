""" Perform assessment on random deals """

import numpy as np

from IPython import embed

# Format
# [card, min_n1, max_n1, hand]

def test_deals(deals:np.ndarray, n1:np.ndarray,
               query:list):
    """
    Test the deals based on the given query.

    Args:
        deals (np.ndarray): Array of deals.
            shape = (n_deals, n_cards)
        n1 (np.ndarray): Array of n1, the number of cards in hand1.
            shape = (n_deals,) 
        query (list): List of queries.
            Each item in this list has the format
            [card, min_n1, max_n1, hand]
            where:
                card (int): Card to query
                min_n1 (int): Minimum number of card in hand
                max_n1 (int): Maximum number of card in hand
                hand (int): 1 for hand1, 2 for hand2
            Items in the top level of the list use & logic.
            Items in the second level of the list use | logic.

    Returns:
        np.ndarray: Boolean array indicating which deals pass the query.
            shape = (n_deals,)
    """

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
    """
    Parses a query list and returns a dictionary.

    Args:
        query (list): A list containing card, min_n, max_n, and hand.

    Returns:
        dict: A dictionary containing the parsed values.

    Example:
        >>> query = ['A', 2, 5, 'Spades']
        >>> parse_query(query)
        {'card': 'A', 'min_n': 2, 'max_n': 5, 'hand': 'Spades'}
    """
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
    """
    Query the deals based on specified criteria.

    Args:
        deals (np.ndarray): Array of deals.
            shape = (n_deals, n_cards)
        n1 (np.ndarray): Array of lengths for the first hand.
            shape = (n_deals,)
        qdict (dict): Dictionary containing query criteria.

    Returns:
        np.ndarray: Array of boolean values indicating whether each deal meets the query criteria.
            shape = (n_deals,)
    """

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

    # Finish assessment
    assess = np.zeros(deals.shape[0], dtype=bool)
    assess[gdi] = in_hand

    return assess
        
    