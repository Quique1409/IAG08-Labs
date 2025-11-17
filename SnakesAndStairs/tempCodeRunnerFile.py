def expected_moves(P):
    """
    Calculates the average numbers of moves to win
    using the fundamental matrix N = (I - Q)^-1
    """
    # Q = Transtions between transient states (0-99 in our case)
    transient_states = N_States - 1
    Q = P[0:transient_states, 0:transient_states]
    
    # I = Identity matrix (same dimention as the number of transient states)
    I = np.identity(transient_states)