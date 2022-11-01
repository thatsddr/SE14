"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    moves = 0
    for row in board:
        for e in row:
            if e != None:
                moves += 1

    if moves == 0 or moves % 2 == 0:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set();
    # go through the board and return all empty cells
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if action is a valid action in the board
    if action not in actions(board):
        raise Exception
    # make sure that the original board is left unmodified
    newBoard = copy.deepcopy(board)
    # return new board
    newBoard[action[0]][action[1]] = player(board)
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_3(a, b, c):
        if a == b and b == c:
            return a
        return None

    # check rows
    for i in range(len(board)):
        if check_3(board[i][0], board[i][1], board[i][2]):
            return board[i][0]

    # check columns
    for j in range(len(board[0])):
        if check_3(board[0][j], board[1][j], board[2][j]):
            return board[0][j]
    
    # check diagonals
    if check_3(board[0][0], board[1][1], board[2][2]):
        return board[0][0]
    if check_3(board[0][2], board[1][1], board[2][0]):
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # return true if there is a winner
    if winner(board) != None:
        return True
    # otherwise only return false if there is at least an empty cell
    for row in board:
        for e in row:
            if e == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = winner(board)
    if res == X:
        return 1
    elif res == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        return max_value(board, float("-inf"), float("inf"))[1]
    else:
        return min_value(board, float("-inf"), float("inf"))[1]

def max_value(board):
    """
    produces biggest value of min value
    """
    
    # return the board and no move if the board is terminal
    if terminal(board):
        return (utility(board), None);
    
    move = None

    v = float('-inf') # set the maximum to the bisggest value possible
    for a in actions(board):
        # get the maximum between the current maximum (v) and the restult of min_value for the current action
        temp = min_value(result(board, a))[0]
        # if it's bigger than the current maximum, update value and optimal move
        if temp > v:
            v = temp
            move = a

    return (v, move);

def min_value(board):
    """
    produces smallest value of min value
    """
    
    # return the board and no move if the board is terminal
    if terminal(board):
        return (utility(board), None);

    move = None

    v = float('inf') # set the minimum to the the biggest value possible
    for a in actions(board):
        # get the minimum between the current minimum (v) and the restult of max_value for the current action
        temp = max_value(result(board, a))[0]
         # if it's smaller than the current minimum, update value and optimal move
        if temp < v:
            v = temp
            move = a

    return (v, move);