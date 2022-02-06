"""
Tic Tac Toe
"""
from tcp_latency import measure_latency

class game():

    def __init__(self, symbol_of_player):
        self.list_of_symbols = []
        for i in range(9):
            self.list_of_symbols.append(" ") 

        self.symbol_of_player = symbol_of_player


    def restart(self):
        # clears the grid 
        for i in range(9):
            self.symbol_list[i] = " "


    def draw_grid(self):
        #printing columns
        print("\n       A   B   C\n")
        
        #printing row one
        first_row = "   1   " + self.list_of_symbols[0]
        first_row += " ║ " + self.list_of_symbols[1]
        first_row += " ║ " + self.list_of_symbols[2]
        print(first_row)

        #separating rows
        print("      ═══╬═══╬═══")

        #printing row two
        second_row = "   2   " + self.list_of_symbols[3]
        second_row += " ║ " + self.list_of_symbols[4]
        second_row += " ║ " + self.list_of_symbols[5]
        print(second_row)

        #separating rows
        print("      ═══╬═══╬═══")

        # display third and last row 
        third_row = "   3   " + self.list_of_symbols[6]
        third_row += " ║ " + self.list_of_symbols[7]
        third_row += " ║ " + self.list_of_symbols[8]
        print(third_row, "\n")


    def edit_square(self, grid_co_ordinate):
        #code to swap the coordinates from 1a to a1 
        if grid_co_ordinate[0].isdigit():
            grid_co_ordinate = grid_co_ordinate[1] + grid_co_ordinate[0]

        #separates the row and column from the given coordinate
        column = grid_co_ordinate[0].capitalize()
        row = grid_co_ordinate[1]

        # converts "A1" to 0, "C3" to 8, and so forth 
        index_of_grid = 0

        if row == "1":
            if column == "A":
                index_of_grid = 0
            elif column == "B":
                index_of_grid = 1
            elif column == "C":
                index_of_grid = 2
        elif row == "2":
            if column == "A":
                index_of_grid = 3
            elif column == "B":
                index_of_grid = 4
            elif column == "C":
                index_of_grid = 5
        elif row == "3":
            if column == "A":
                index_of_grid = 6
            elif column == "B":
                index_of_grid = 7
            elif column == "C":
                index_of_grid = 8

        if self.list_of_symbols[index_of_grid] == " ":
            self.list_of_symbols[index_of_grid] = self.symbol_of_player
        

    def printing_latencies(self):
        propogation_delays = measure_latency(host='192.168.1.4', port = 12784, timeout =15, runs = 3)
        sample_rtts = [ 2 * propogation_delays[0] , 2 * propogation_delays[1],2 * propogation_delays[2]]
        estimated_rtt = float(sum(sample_rtts) / len(sample_rtts))
        print("Estimate RTT={}ms".format(round(estimated_rtt,4)))
        propogation_delay =  measure_latency(host='192.168.1.4', port = 12784, timeout =15)
        sample_rtt = float(2 * propogation_delay[0])
        estimated_rtt = (1 - 0.125) * estimated_rtt + (0.125) * sample_rtt
        print("Propagation Delay={}ms".format(round(propogation_delays[1],4)))
        print("Round trip time={}ms".format(round(estimated_rtt,4)))
        print("Sample RTT={}ms".format(round(sample_rtt,4)))


    def update_symbol_list(self, symbol_list_updated):
        for i in range(9):
            self.list_of_symbols[i] = symbol_list_updated[i]


    def player_win(self, symbol_of_player):
        symbols = []
        for i in range(9):
            symbols.append(self.list_of_symbols[i])
    
        symbol = symbol_of_player

        #checking the winning pattern across top, middle and bottom rows
        if symbols[0] == symbol and symbols[1] == symbol and symbols[2] == symbol:
            return True

        elif symbols[3] == symbol and symbols[4] == symbol and symbols[5] == symbol:
            return True
        
        elif symbols[6] == symbol and symbols[7] == symbol and symbols[8] == symbol:
            return True 

        #checking the winning pattern across left, middle, right columns 
        elif symbols[0] == symbol and symbols[3] == symbol and symbols[6] == symbol:
            return True 

        elif symbols[1] == symbol and symbols[4] == symbol and symbols[7] == symbol:
            return True 

        elif symbols[2] == symbol and symbols[5] == symbol and symbols[8] == symbol:
            return True

        #checking the winning pattern across the diagonals
        elif symbols[2] == symbol and symbols[4] == symbol and symbols[6] == ssymbolym:
            return True 

        elif symbols[0] == symbol and symbols[4] == symbol and symbols[8] == symbol:
            return True 

        #nothing matched!!
        return False


    def is_draw(self):
        #checking whether all the grids are filled
        blank_grids = 0
        for i in range(9):
                if self.list_of_symbols[i] == " ":
                    blank_grids += 1

        # if the player didn't win and no spaces are left, it's a draw
        if self.player_win(self.symbol_of_player) == False and blank_grids == 0:
            return True
        else:
            return False
