import requests, time, sys, threading
from datetime import date
from colorama import init, Fore


'''This Python script finds the solution move to Europe Echecs's diagram of the day'''
starttime = time.time()
init()
GREEN = Fore.GREEN # setting up green writing in the shell for when a solution is found
RESET = Fore.RESET
RED = Fore.RED # setting up red writing in the shell for when a solution is not found
YELLOW = Fore.YELLOW

# Create all possible moves playable on a chess board (except promotions and disambiguation moves such as Red4)

piece_symbol, rows, columns, moves_list = ['K','Q','N','R','B'], [str(i) for i in range(1,9)], ['a','b','c','d','e','f','g','h'], []
d = {k:columns.index(k) for k in columns}

moves_list = [piece+column+row for piece in piece_symbol for row in rows for column in columns] \
    + [piece+ 'x'+column+row for piece in piece_symbol for row in rows for column in columns] \
        + [column+row for row in rows for column in columns] \
            +[colstart+'x'+colend+row for row in rows[2:] for colstart in columns for colend in columns if d[colend] - d[colstart] in (-1,1)] \
                + ['0-0','0-0-0','...0-0','...0-0-0'] \
                    + [piece+column+row+'%2B' for piece in piece_symbol for row in rows for column in columns] \
                        + [piece+ 'x'+column+row+'%2B' for piece in piece_symbol for row in rows for column in columns] 

found = 0

def get_solution_without_threading(moves_iterable, date = str(date.today()).replace('-','') , verbose = True):
    '''This function returns the solution to europe echecs' tactical diagram for the given yyyymmdd date (default current date's diagram)'''
    global found
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
                move = move.replace('%2B','+')
                print(f'{GREEN}The solution for {date} is {move} : {response["solutionpgn"]}{RESET}')
                endtime = time.time()
                duration = endtime - starttime
                print(f'{YELLOW}Done in {round(duration,1)} seconds.{RESET}\n')
                found = 1            
        except Exception as e: # this is better than just 'except:' as it still enables Ctrl+C to stop the code in the shell
            if verbose == True:
                print(f'{RED}Could not test {move}: {e}{RESET}')
            continue


def get_solution_with_threading(thread_moves_checks, date):# this argument defines how many moves each thread is going to check. The smaller the quicker the program finds the solution, in principle
    # parallelizing the search for the solution
     # main thread
    def isfound():
        while found != 1:
            pass

    MainThread = threading.Thread(target = isfound)
    MainThread.start()  # this is just a dummy function that is used to stop all daemon threads whenever it stops running (meaning when solution is found)

    # searching threads (they are daemon threads)

    for i in range(0,len(moves_list),thread_moves_checks):
        moves_gen = (move for move in moves_list[i:i+thread_moves_checks])  # a generator containing the moves to test against the solution
        NewThread = threading.Thread(target = get_solution_without_threading, args = (moves_gen,) , kwargs = {'date': date, 'verbose': 'False'}, daemon = True ) # the daemon argument allows to shutdown all threads when one of them has found the solutio move
        NewThread.start()

get_solution_with_threading(3,str(date.today()).replace('-',''))
