import numpy as numpy
import pygame
import sys
import math


def empty_row(board,col):
    for i in range(6):
        if board[i][col] == 0:
            return i


def find_win(board,n):
    #horizontal
    for i in range(4):
        for j in range(6):
            if board[j][i] == n:
                if board[j][i+1] == n:
                    if board[j][i+2] == n:
                        if board[j][i+3] == n:
                            return True
    #vertical
    for i in range(7):
        for j in range(3):
            if board[j][i] == n:
                if board[j+1][i] == n:
                    if board[j+2][i] == n:
                        if board[j+3][i] == n:
                            return True
#diaganols

    for i in range(4):
        for j in range(6):
            if j < 3:
                if board[j][i] == n:
                    if board[j + 1][i + 1] == n:
                        if board[j + 2][i + 2] == n:
                            if board[j + 3][i + 3] == n:
                                return True
            else:
                if board[j][i] == n:
                    if board[j - 1][i + 1] == n:
                        if board[j - 2][i + 2] == n:
                            if board[j - 3][i + 3] == n:
                                return True

def evaluate(line,n):
    score = 0
    list_n = [1,2]
    list_n.remove(n)
    m = int(list_n[0])

    if line.count(n) == 4:
            score += 150
    elif line.count(n) == 3:
        if line.count(0) == 1:
            score += 50
    elif line.count(n) == 2:
        if line.count(0) == 2:
            score += 5

    if line.count(m) == 3:
        if line.count(0) == 1:
            score -= 10
    elif line.count(m) == 2:
        if line.count(0) == 2:
            score -= 3
    return score

def score(board,n):
    score = 0
    #center col
    center = [int(i) for i in list(board[:,3])]
    center_count = center.count(n)
    score += center_count * 3

    # horizontal
    for r in range(6):
        row = [int(i) for i in list(board[r,:])]
        for c in range(4):
            score += evaluate(row[c:c+4],n)
    # vertical

    for c in range(7):
        col = [int(i) for i in list(board[:,c])]
        for r in range(3):
            score += evaluate(col[r:r+4],n)
#diagonal
    for r in range(3):
        for c in range(4):
            line = [board[r+i][c+i] for i in range(4)]
            score += evaluate(line,n)
            line = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate(line,n)
    return score


def max(board, depth, alpha, beta, work):
    valid_location2 = valid_location(board)

    terminal = (find_win(board,1) or find_win(board,2) or len(valid_location(board)) == 0)
    if depth == 0 or terminal:
        if terminal:
            if find_win(board, 2):
                return (None, 100000000000000)
            elif find_win(board, 1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score(board, 2))


    if work:
        value = -10000000000
        column = 0
        for col in valid_location2:
            board2 = board.copy()
            board2[empty_row(board, col)][col] = 2
            new_score = mini(board2, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            if alpha > value:
                alpha = alpha
            else:
                alpha = value
            if alpha >= beta:
                break
        return column, value

def mini(board, depth, alpha, beta, work):
    valid_location2 = valid_location(board)

    terminal = (find_win(board, 1) or find_win(board, 2) or len(valid_location(board)) == 0)
    if depth == 0 or terminal:
        if terminal:
            if find_win(board, 2):
                return (None, 100000000000000)
            elif find_win(board, 1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score(board, 2))
  #  else:  # Minimizing player

    value = 10000000000
    column = 0
    for col in valid_location2:
        board2 = board.copy()
        board2[empty_row(board, col)][col] = 1
        new_score = max(board2, depth - 1, alpha, beta, True)[1]
        if new_score < value:
            value = new_score
            column = col
        if beta < value:
            beta = beta
        else:
            beta = value
        if alpha >= beta:
            break
    return column, value


def valid_location(board):
    vl = []
    for c in range(7):
        if board[5][c] == 0:
            vl.append(c)
    return vl


def print_board(board):
    blue = (30,144,255)
    black = (0,0,0)
    red = (255,69,0)
    yellow = (238,238,0)
    white = (253,245,230)
    for i in range(7):
        for j in range(6):
            pygame.draw.rect(screen,blue,(i*100,j*100+100,100,100))
            pygame.draw.circle(screen,black,(int(i*100+100/2),int(j*100+100+100/2)),45)
    for i in range(7):
        for j in range(6):
            if board[j][i] == 1:
                pygame.draw.circle(screen, red, (int(i * 100 + 50), height - int(j * 100 + 50)), 45)
            elif board[j][i] == 2:
                pygame.draw.circle(screen, yellow, (int(i * 100 + 50), height - int(j * 100 + 50)), 45)
    pygame.display.update()

if __name__ == '__main__':
    board = numpy.zeros((6,7))
    print(numpy.flip(board,0))
    finish = False
    turn = 0

    pygame.init()
    s = 100
    width = 7 * s
    height = 7 * s

    size = (width,height)

    screen = pygame.display.set_mode(size)
    print_board(board)
    pygame.display.update()
    font = pygame.font.SysFont('monospace',75)
    turn = 0

    while not finish:
        red = (255, 69, 0)
        yellow = (255, 255, 0)
        black = (0,0,0)
        white= (248,248,255)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen,black,(0,0,width,100))
                pos = event.pos[0]
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen,black,(0,0,width,100))
                # player1 step
                if turn == 0:
                    pos1 = event.pos[0]
                    p1_col = int(math.floor(pos1 / 100))

                    if board[5][p1_col] == 0:
                        row = empty_row(board,p1_col)
                        board[row][p1_col] = 1
                        if find_win(board,1):
                            lab1 = font.render('Player win!!',1,white)
                            screen.blit(lab1,(40,10))
                            finish = True
                        turn += 1
                        turn %= 2  # switch
                        print(numpy.flip(board,0))
                        print_board(board)


                #player2 step
        if turn == 1 and not finish:

            p2_col,minimax_score = max(board,5, -10000000, 10000000,True)
            if minimax_score <= 100000:
                lab5 = font.render('+'+str(minimax_score), 1, white)
                screen.blit(lab5, (40, 10))
                pygame.display.update()
                pygame.time.wait(500)
            if board[5][p2_col] == 0:
                pygame.time.wait(500)
                row = empty_row(board,p2_col)
                board[row][p2_col] = 2
                if find_win(board,2):
                    lab2 = font.render('   Ai win!!', 1, white)
                    screen.blit(lab2, (40, 10))
                    finish = True

                print(numpy.flip(board,0))
                print_board(board)

                turn += 1
                turn %= 2  # switch

        if finish:
            pygame.time.wait(5000)