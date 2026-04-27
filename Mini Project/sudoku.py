def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


def is_valid(board, row, col, num):
    for x in range(9):
        if x != col and board[row][x] == num:
            return False

    for x in range(9):
        if x != row and board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            r = start_row + i
            c = start_col + j
            if (r != row or c != col) and board[r][c] == num:
                return False

    return True


def solve(board):
    empty = find_empty(board)

    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False


def solve_steps(board):
    empty = find_empty(board)
    if not empty:
        yield("done" , None, None , None)
        return True
    
    row, col = empty
    
    for num in range(1,10):
        if is_valid(board, row, col,num):
            board[row][col] = num
            yield("place" , row, col,num)
            
            solved = yield from solve_steps(board)
            if solved:
                return True
            board[row][col] = 0
            yield("remove" , row, col,0)
    
    return False        