import socket
import pickle


from tic_tac_toe import game

host_addr = '127.0.0.1'
port_addr = 12784

#establishing the connection with host
socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_s.connect((host_addr, port_addr))
print(f"\nConnected to {socket_s.getsockname()}!")

#starting the game
player_two = game("O")

# allow the player to suggest playing again
play_again = True

while play_again == True:
    # a header for an intense tic-tac-toe match! 
    print(f"\n\n T I C - T A C - T O E ")

    # draw the grid
    player_two.draw_grid()

    # host goes first, client receives first
    print(f"\nWaiting for other player...")
    symbol_list_of_player_one = socket_s.recv(1024)
    symbol_list_of_player_one = pickle.loads(symbol_list_of_player_one)
    player_two.update_symbol_list(symbol_list_of_player_one)

    # the rest is in a loop; if either player has won, it exits 
    while player_two.player_win("O") == False and player_two.player_win("X") == False and player_two.is_draw() == False:
        #getting the input from the player
        print(f"\n       Your turn!")
        player_two.draw_grid()
        player_coordinates = input(f"Enter coordinate: ")
        player_two.edit_square(player_coordinates)

        #printing the grid
        player_two.draw_grid()

        #getting the inputs list and sending it
        symbol_list_of_player_two = pickle.dumps(player_two.list_of_symbols)
        socket_s.send(symbol_list_of_player_two)


        # if the player won with the last move or it's a draw, exit the loop 
        if player_two.player_win("O") == True or player_two.is_draw() == True:
            break

        # wait to receive the symbol list and update it
        print(f"\nWaiting for other player...")
        symbol_list_of_player_one = socket_s.recv(1024)
        symbol_list_of_player_one = pickle.loads(symbol_list_of_player_one)
        player_two.update_symbol_list(symbol_list_of_player_one)


    if player_two.player_win("O") == True:
        print(f"Congrats, you won!")
        player_two.printing_latencies()
    elif player_two.is_draw() == True:
        print(f"It's a draw!")
    else:
        print(f"Sorry, the host won.")

    #asking host to play again and waiting for the confirmation 
    print(f"\nWaiting for host...")
    response_of_host = socket_s.recv(1024)
    response_of_host = pickle.loads(response_of_host)
    response_of_client = "N"

    # if the host wants a rematch, then the client is asked 
    if response_of_host == "Y":
        print(f"\nThe host would like a rematch!")
        response_of_client = input("Rematch? (Y/N): ")
        response_of_client = response_of_client.capitalize()
        temporary_client_resp = response_of_client

        # let the host know what the client decided 
        response_of_client = pickle.dumps(response_of_client)
        socket_s.send(response_of_client)

        # if the client wants a rematch, restart the game
        if temporary_client_resp == "Y":
            player_two.restart()

        # if the client said no, then no rematch 
        else:
            play_again = False

    # if the host said no, then no rematch 
    else:
        print(f"\nThe host does not want a rematch.")
        play_again = False

spacer = input(f"\nThank you for playing!\nPress enter to quit...\n")

socket_s.close()