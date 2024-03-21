#id:311453906   name : Guy Bar-dor
import sys
import socket
import selectors
import types
import time
import random
from Game import Board  # Ensure the Board class is defined as shown in your new code snippet

sel = selectors.DefaultSelector()

# Game session management
games = {}  # Dictionary to hold game sessions, with unique game IDs as keys
onlinegames = {}
waiting_players = []

def generate_unique_game_id():
    return f"{int(time.time())}-{random.randint(1000, 9999)}"


def send_opponet_move_to_client(sock, row, col):
    ai_move_msg = f"rival_move,{row},{col}"
    print("ai_move_msg"+ai_move_msg)
    sock.sendall(ai_move_msg.encode('utf-8'))

def send_opponet_move_multiplayer_to_client(sock, row, col):
    ai_move_msg = f"rival_move_multiplayer,{row},{col}"
    print("rival_move_multiplayer"+ai_move_msg)
    sock.sendall(ai_move_msg.encode('utf-8'))

def send_wait_message_multiplayer_to_client(sock, row, col):
    ai_move_msg = f"waiting,{row},{col}"
    print("notyourmove_multiplayer"+ai_move_msg)
    sock.sendall(ai_move_msg.encode('utf-8'))

def send_game_over_to_client(sock):
    ai_move_msg = f"gameover"
    print("gameover"+ai_move_msg)
    sock.sendall(ai_move_msg.encode('utf-8'))

def process_client_move(sock, gameboard, received_text, game_id):
    # Extracting the command and move details from the received text
    print(received_text)
    move,column_str = received_text.split(',')

    color="yellow"
    column = int(column_str) - 1  # Adjust column to 0-based index
    
    # Access the game board for the current game session
    game_board = gameboard
    row = game_board.find_lowest_available_row(column)
    print(row,column,color)
    # Attempt to make the move on the game board
    valid_move = game_board.set_cell_color( row,column, color)
    if valid_move:
        print(f"Move accepted: {color} in column {column + 1} for game {game_id}")
        game_board.print_board()        
        
        # Check for a win after the move
        win, winning_color = game_board.check_win()
        if win:
            print(f"{winning_color} wins the game {game_id}!")
            
            
            return True, f"{winning_color} wins!"
        else:
            return True, "Move accepted. Next player's turn."
    else:
        print(f"Invalid move attempted in game {game_id}")
        return False, "Invalid move. Try again."

def process_multiplayer_client_move(sock, gameboard, received_text, game_id):
    # Extracting the command and move details from the received text
    print(received_text)
    
    move,column_str = received_text.split(',')
    if(onlinegames[game_id].current_move %2== 0 ):
        color="yellow"  
    else:
        color = "red"
    column = int(column_str) - 1  # Adjust column to 0-based index
    onlinegames[game_id].current_move =  onlinegames[game_id].current_move +1 
    # Access the game board for the current game session
    game_board = gameboard
    row = game_board.find_lowest_available_row(column)
    print(row,column,color)
    # Attempt to make the move on the game board
    valid_move = game_board.set_cell_color( row,column, color)
    if valid_move:
        print(f"Move accepted: {color} in column {column + 1} for game {game_id}")
        game_board.print_board()        
        
        # Check for a win after the move
        win, winning_color = game_board.check_win()
        if win:
            print(f"{winning_color} wins the game {game_id}!")
            
            
            return True, f"{winning_color} wins!"
        else:
            return True, "Move accepted. Next player's turn."
    else:
        print(f"Invalid move attempted in game {game_id}")
        return False, "Invalid move. Try again."
#
def accept_wrapper(sock):
    conn, addr = sock.accept()  # קבלת החיבור
    print("Accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", game_started=False, sock=conn)  # הוספת sock לאובייקט
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

def start_new_game(player1, player2):
    game_id = generate_unique_game_id()
    onlinegames[game_id] = Board(6, 7, ["red", "yellow"])
    onlinegames[game_id].print_board()
    onlinegames[game_id].print_current_color()
    print(f"Game {game_id} started between {player1.addr} and {player2.addr}")
    onlinegames[game_id].game_id=game_id
    onlinegames[game_id].player1=player1
    onlinegames[game_id].player2=player2
    onlinegames[game_id].player1.game_started = True
    onlinegames[game_id].player2.game_started = False
    onlinegames[game_id].player1.isMyTurn=True
    onlinegames[game_id].player2.isMyTurn=False
    onlinegames[game_id].current_move = 0
    onlinegames[game_id].player1.color="yellow"
    onlinegames[game_id].player2.isMyTurn="red"
    
    onlinegames[game_id].player1.isFirstMove=False
    onlinegames[game_id].player2.isFirstMove=True

    player1.game_id = game_id
    player2.game_id = game_id


    player1.win=0
    player2.win=0
    #here to send message to each one of the players the first player start the second not
    player1.sock.sendall(f"yourmove multiplayer game has started.enter Your move.,{-1}".encode('utf-8'))
    #player2.sock.sendall(b"notyourmove,multiplayer game has started.enter Your move.")
    print("player 1 sock " ,player1.sock)
    print("player 2 sock" , player2.sock)
def change_turn(game_id,col):
    if onlinegames[game_id].player1.isMyTurn:
        onlinegames[game_id].player1.isMyTurn = False
        onlinegames[game_id].player2.isMyTurn = True
        onlinegames[game_id].player2.sock.sendall(f"yourmove multiplayer game has started.enter Your move.,{col}".encode('utf-8'))
    else:
        onlinegames[game_id].player1.isMyTurn = True
        onlinegames[game_id].player2.isMyTurn = False
        onlinegames[game_id].player1.sock.sendall(f"yourmove multiplayer game has started.enter Your move.,{col}".encode('utf-8'))
    print(f"Turn changed: Player 1's turn: {onlinegames[game_id].player1.isMyTurn}, Player 2's turn: {onlinegames[game_id].player2.isMyTurn}")
# def change_turn(game_id):
#     onlinegames[game_id].player1.isMyTurn=not onlinegames[game_id].player1.isMyTurn
#     onlinegames[game_id].player2.isMyTurn=not onlinegames[game_id].player2.isMyTurn
#     print(onlinegames[game_id].player1.isMyTurn)
#     print(onlinegames[game_id].player2.isMyTurn)

def find_opponent_and_start_game(player):
    if waiting_players:
        opponent = waiting_players.pop(0)
        print("player" , player)
        print("opponet" ,opponent)
        start_new_game(player, opponent)
    else:
        waiting_players.append(player)
        player.outb += b"Waiting for opponent..."

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("Accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", game_started=False)
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    game_id = generate_unique_game_id() 

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            received_text = recv_data.decode('utf-8').strip()
            print(received_text)
            print(f"Received data: {received_text} from: {data.addr}")

            # Process game start or moves
              # Process game start or moves
            if received_text in ["singleplayer", "multiplayer"] and not data.game_started:
                if received_text=="singleplayer":
                    print("singleplayer")
                    # Initialize game session
                    games[game_id] = Board(6, 7, ["red", "yellow"])
                    data.game_id = game_id
                    data.game_started = True
                    # Send confirmation back to the client
                    start_msg = f"{received_text} game has started. Your move."
                    data.outb += start_msg.encode('utf-8')
                    games[game_id].print_board()
                    print(f"Game {game_id} started in {received_text} mode for {data.addr}")
                else:
                    print(f"Game {game_id} started in {received_text} mode for {data.addr}")
                    print(" multiplayer")
                    data.sock = sock
                    find_opponent_and_start_game(data)
                    
                    # Initialize game session
                    #if there is player wating check and connect them 
                    #else start  a new queue for them

            elif received_text.startswith("game-over"):
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()

            elif received_text.startswith("move,") and data.game_started:
                # Process move
                game_id = data.game_id
                valid_move, response_message = process_client_move(sock, games[game_id], received_text, game_id)  # Ensure process_client_move returns a tuple
                if valid_move:
                   # data.outb += "Move accepted. ".encode('utf-8') + response_message.encode('utf-8')
                    games[game_id].print_board()  # Print the updated board after a move
                    games[game_id].print_current_color()
                    #the ai do his move :
                    print("the ai will do his move")
                    row,col = games[game_id].ai_move()
                    games[game_id].print_board()
                    send_opponet_move_to_client(sock,row,col)
                    iswin,color=games[game_id].check_win()
                    print(iswin)
                    if iswin:
                        if(color == "yellow"):
                            print("yellow win")
                            games[game_id].player1.win=games[game_id].player1.win+1
                            print("win of player one" + games[game_id].player1.win )
                        else :
                            print("Red win") 
                            games[game_id].player2.win=games[game_id].player2.win+1
                            print("win of player two" + games[game_id].player2.win)
                        send_game_over_to_client(sock)
                # else:
                #     data.outb += "Invalid move. ".encode('utf-8') + response_message.encode('utf-8')
      
               
                
             #       
            elif received_text.startswith("multiplayermove,") and data.game_started:
                # Process move
                print(received_text)
                game_id = data.game_id
                print(192)
                valid_move, response_message = process_multiplayer_client_move(sock, onlinegames[game_id], received_text, game_id)  # Ensure process_client_move returns a tuple
                if valid_move:
                   # data.outb += "Move accepted. ".encode('utf-8') + response_message.encode('utf-8')
                    onlinegames[game_id].print_board()  # Print the updated board after a move
                    onlinegames[game_id].print_current_color()
                    #the ai do his move :
                    _,col  =  received_text.split(',')
                   
                    #  row,col = games[game_id].ai_move()
                    onlinegames[game_id].print_board()
                    row=onlinegames[game_id].find_lowest_available_row(int(col))
                    #to idenify the current sock to send the ,essage that his turn 
                    #to send the user that send the message that he need to wait 
                    if onlinegames[game_id].player2.game_started==False:
                        onlinegames[game_id].player2.game_started=True
                        onlinegames[game_id].player2.isMyTurn=True
                        onlinegames[game_id].player1.isMyTurn=False
                        #onlinegames[game_id].player1.isMyTurn=False
                       #to rerplacr to rival move with the function 
                        onlinegames[game_id].player2.sock.sendall(f"yourmove multiplayer game has started.enter Your move.,{col}".encode('utf-8'))
                       
                        return

                    if (onlinegames[game_id].player2.isMyTurn==True):
                        print("player 2 turn")
                        #onlinegames[game_id].player1.sock.sendall(b"yourmove,multiplayer game has started.enter Your move.")
                        change_turn(game_id,col)
                        return
                    else:
                        print("player 1 turn ")
                        #onlinegames[game_id].player2.sock.sendall(b"yourmove,multiplayer game has started.enter Your move.")
                        change_turn(game_id,col)
                        return
                    
                    iswin,color=onlinegames[game_id].check_win()
                    # change_turn(game_id)
                    print(iswin)
                    if iswin:
                        if(color == "yellow"):
                            print("yellow win")
                            onlinegames[game_id].player1.win=onlinegames[game_id].player1.win+1
                        else :
                            print("Red win") 
                            onlinegames[game_id].player2.win=onlinegames[game_id].player2.win+1
                        send_game_over_to_client(sock)
                # else:
                #     data.outb += "Invalid move. ".encode('utf-8') + response_message.encode('utf-8')             
            
            
        
        

    if mask & selectors.EVENT_WRITE and data.outb:
        sent = sock.send(data.outb)
        data.outb = data.outb[sent:]



def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
    lsock.bind((host, port))
    lsock.listen()
    print(f"Server is listening on {host}:{port}")  # Print the listening host and port
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

if __name__ == "__main__":
    main()
