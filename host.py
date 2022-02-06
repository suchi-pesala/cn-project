import socket
import pickle

#importing the tic_tac_toe module created as game
from tic_tac_toe import game

host_addr = '127.0.0.1'
port_addr = 12784


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_addr, port_addr))
server_socket.listen(5)


socket_client, client_address = server_socket.accept()
print(f"\nConnnected to {client_address}!")

# starting the game
player_one = game("X")

#variable to enable the players to play again
play_again = True

while play_again == True:
    # a header for an intense tic-tac-toe match! 
    print(f"\n\n T I C - T A C - T O E ")

    #Game is in loop, if any of the player wins loop will end
    while player_one.player_win("X") == False and player_one.player_win("O") == False and player_one.is_draw() == False:
        # draw grid, ask for coordinate
        print(f"\n       Your turn!")
        player_one.draw_grid()
        player_coordinates = input(f"Enter coordinate: ")
        player_one.edit_square(player_coordinates)

        #Drawing the grid for each entry 
        player_one.draw_grid()

        #sending the symbol list
        symbol_list_of_player_one = pickle.dumps(player_one.list_of_symbols)
        socket_client.send(symbol_list_of_player_one)

        #exiting the loop if player one wins with the last step or game is drawn 
        if player_one.player_win("X") == True or player_one.is_draw() == True:
            break

        #waiting for the other player to play and update the list 
        print(f"\nWaiting for other player...")
        symbol_list_of_player_two = socket_client.recv(1024)
        symbol_list_of_player_two = pickle.loads(symbol_list_of_player_two)
        player_one.update_symbol_list(symbol_list_of_player_two)

    # end game messages
    if player_one.player_win("X") == True:
        print(f"Congrats, you won!")
        player_one.printing_latencies()
    elif player_one.is_draw() == True:
        print(f"It's a draw!")
        player_one.printing_latencies()
    else:
        print(f"Sorry, the client won.")
    
    #waiting to play again
    response_of_host = input(f"\nRematch? (Y/N): ")
    response_of_host = response_of_host.capitalize()
    host_resp_temporary = response_of_host
    response_of_client = ""

    # pickle response and send it to the client 
    response_of_host = pickle.dumps(response_of_host)
    socket_client.send(response_of_host)

    # if the host doesn't want a rematch, we're done here
    if host_resp_temporary == "N":
        play_again = False

    # if the host does want a rematch, we ask the client for their opinion
    else:
        # receive client's response 
        print(f"Waiting for client response...")
        response_of_client = socket_client.recv(1024)
        response_of_client = pickle.loads(response_of_client)

        # if the client doesn't want a rematch, exit the loop 
        if response_of_client == "N":
            print(f"\nThe client does not want a rematch.")
            play_again = False

        # if both the host and client want a rematch, restart the game
        else:
            player_one.restart()

spacer = input(f"\nThank you for playing!\nPress enter to quit...\n")

socket_client.close()