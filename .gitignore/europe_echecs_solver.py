import requests, time, sys, threading
from datetime import date
from colorama import init, Fore


'''This Python script finds the solution move to Europe Echecs's diagram of the day'''
starttime = time.time()
init()
GREEN = Fore.GREEN # setting up green writing in the shell for when a solution is found
RESET = Fore.RESET
RED = Fore.RED # setting up red writing in the shell for when a solution is not found

# Create all possible moves playable on a chess board (except promotions and disambiguation moves such as Red4)

piece_symbol, rows, columns, moves_list = ['K','Q','N','R','B'], [str(i) for i in range(1,9)], ['a','b','c','d','e','f','g','h'], []
d = {k:columns.index(k) for k in columns}

moves_list = [piece+column+row for piece in piece_symbol for row in rows for column in columns] \
    + [piece+ 'x'+column+row for piece in piece_symbol for row in rows for column in columns] \
        + [column+row for row in rows for column in columns] \
            +[colstart+'x'+colend+row for row in rows for colstart in columns for colend in columns if d[colend] - d[colstart] == 1 ] \
                + ['0-0','0-0-0','...0-0','...0-0-0'] \
                    + [piece+column+row+'%2B' for piece in piece_symbol for row in rows for column in columns] \
                        + [piece+ 'x'+column+row+'%2B' for piece in piece_symbol for row in rows for column in columns] 


def get_EE_diagram_solution(moves_iterable, date = str(date.today()).replace('-','') , verbose = False):
    '''This function returns the solution to europe echecs' tactical diagram for the given yyyymmdd date (default current date's diagram)'''
    
    # step 1 : check the requests that are made when a move is submitted by a user. 
    # Turns out it is the below POST request (GET works, too) and this yields an HTML page with answer in plain text

    url = 'https://www.europe-echecs.com/ajax.php?mode=ajax&function=dailypuzzle&action=play&id='+date+'&movepgn='
    
    # step 2 : iterate on the moves list by making requests
    
    for move in moves_iterable:
        try:
            if verbose == True:
                print(f'Testing {move}')
            response = requests.post(url+move).json() 
            if response['result'] == 1:
                print(f'{GREEN}The solution for {date} is {move} : {response["solutionpgn"]}{RESET}')
                endtime = time.time()
                duration = endtime - starttime
                print(f'\nDone in {round(duration,1)} seconds.')
                break            
        except Exception as e:
            if verbose == True:
                print(f'{RED}Could not test {move}: {e}{RESET}')
            continue

moves_gen = (move for move in moves_list)
get_EE_diagram_solution(moves_gen,verbose=True)

