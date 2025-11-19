def iterative_prob_k_steps(M, v0, k):
    v_k = v0.copy()
    try:
        start_time = time.time()
        for step in range(k):
            v_k = v_k @ M  # Matrix multiplication
        end_time = time.time()
        print(f"(Calculating v_k iteratively took {end_time - start_time:.4f}s)")
        return v_k  # Return the vector of probabilities of being in all states after k moves
    except np.linalg.LinAlgError as e:
        print(f"Error obtaining v_{k} iteratively: {e}")
        return None