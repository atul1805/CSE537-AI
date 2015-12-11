from util import memoize, run_search_function, INFINITY

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass


def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


def reset_nodes_expanded():
    global nodes_expanded
    nodes_expanded = {1: 0, 2: 0}


def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    current_player = board.get_current_player_id()
    
    def propagate_score(board, depth):
        if is_terminal_fn(depth, board):
            return (eval_fn(board), None)
        nodes_expanded[current_player] += 1
        # Get negation of scores propagated from next depth:
        scores = [(-(propagate_score(new_board, depth - 1)[0]), move)
                  for move, new_board in get_next_moves_fn(board)]
        # Select the score, column tuple with the highest score:
        return max(scores, key=lambda pair: pair[0])
    
    return propagate_score(board, depth)[1]


def alpha_beta_search(board, depth, eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    current_player = board.get_current_player_id()
    def propagate_score(board, depth, alpha, beta):
        if is_terminal_fn(depth, board):
            return {'score':eval_fn(board), 'column':None}
        best_value = -INFINITY
        nodes_expanded[current_player] += 1
        for (move, new_board) in get_next_moves_fn(board):
            child = propagate_score(new_board, depth-1, -beta, -alpha)
            score = -child['score']
            if score > best_value:
                best_value = score
                column = move
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
        return {'score':best_value,'column':column}
    return propagate_score(board, depth, -INFINITY, INFINITY)['column']


def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


def new_evaluate(board):
    if board.is_game_over():
        score = -1000
    else:
        # Get all potential chains for each player. A potential chain is a chain
        # which contains only that player's tokens, or empty cells.
        current_player_chains = board.chain_cells(board.get_current_player_id(),
                                                  potential=True)
        other_player_chains = board.chain_cells(board.get_other_player_id(),
                                                potential=True)
        
        def compute_score(chains):
            score = 0
            if board.longest_streak:
                goal = 0
            else:
                goal = board.connect_k
            for chain in chains:
                chain_len = len(chain)
                if chain_len >= goal:
                    chain_val = 0
                    # 1 for player cells, 0 for empty cells:
                    normalized = [min(board.get_cell(*cell), 1) for cell in chain]
                    for idx, piece in enumerate(normalized):
                        if piece == 0:
                            # Can the chain survive if this empty cell is filled?
                            if idx >= goal: # Left side can survive?
                                chain_val += sum(normalized[:idx - 1]) * 2
                            if chain_len - idx > goal: # Right side can survive?
                                chain_val += sum(normalized[idx:]) * 2
                        else:
                            chain_val += 1
                    score += chain_val**2 # Longer chains are worth more
            return score
        
        current_player_score = compute_score(current_player_chains)
        other_player_score = compute_score(other_player_chains)
        
        score = current_player_score - other_player_score
    return score


random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
alphabeta_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=new_evaluate)
