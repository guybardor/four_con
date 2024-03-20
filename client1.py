import socket
import time
from Game import Board
isGameOn = True   
ismyturn=False  
def connect_to_server(host, port):
    """Establish a connection to the game server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def send_message(sock, message):
    """Send a message to the server."""
    print(message)
    sock.sendall(message.encode('utf-8'))

def receive_message(sock):
    """Receive a message from the server."""
    return sock.recv(1024).decode('utf-8')

def start_game(sock, game_mode):
    """Send a request to the server to start a game in the specified mode."""
    send_message(sock, game_mode)
    print("Waiting for game to start...")
    response = receive_message(sock)
    print("Server response:", response)
    return response

def make_move(sock,inputmove):
    """Prompt the player to make a move and send it to the server."""
    send_message(sock, f"move,{inputmove}")
    response = receive_message(sock)
    print("Server response:", response)
    return response

def make_multiplayer_move(sock,inputmove):
    """Prompt the player to make a move and send it to the server."""
    send_message(sock, f"multiplayermove,{inputmove}")
    response = receive_message(sock)
    print("Server response:", response)
    return response
def ismymove(sock):
    """Prompt the player to make a move and send it to the server."""
    response = receive_message(sock)
    print("Server response:", response)
    return response

def process_ai_move_from_server(sock,board,received_msg):
    print("process ai move")
    global isGameOn
    while True:
        
        if received_msg.startswith("rival_move"):
            _, row_str, col_str = received_msg.split(',')
            row, col = int(row_str), int(col_str)
            board.set_cell_color(row, col, "red")  # Assuming AI always plays "yellow"
            board.print_board()
            iswin,color= board.check_win()
            print(iswin)
            if iswin:
              
               isGameOn = False
               print("gameover")
               sock.close()
            break  # Assuming we exit the loop after processing the AI move; adjust as needed
        elif received_msg.startswith("gameover"):
             isGameOn = False
             print("gameover")
             sock.close()
             break
def wait_for_turn(sock):
    while True:
        response = receive_message(sock)
        print("Server response:", response)
        if response.startswith("your turn"):
            return True
        elif response.startswith("wait"):
            time.sleep(1)  # מחכה ומנסה שוב לאחר שנייה
        elif response.startswith("gameover"):
            print("Game Over.")
            return False    
def process_multiplayer_move_from_server(sock,board,received_msg):
    
    print(received_msg)
    global isGameOn
    while True:
        #here we need to take the recive message and take the move
        if received_msg.startswith("yourmove"):
            #_, row_str, col_str = received_msg.split(',')
            col = board.input_and_set_cell()
            row = board.find_lowest_available_row(col)
            board.set_cell_color(row, col, "red")  
            board.print_board()
            make_multiplayer_move(sock,col)
            iswin,color= board.check_win()
            print(iswin)
            if iswin:
              
               isGameOn = False
               print("gameover")
               sock.close()
            break  # Assuming we exit the loop after processing the AI move; adjust as needed
        elif received_msg.startswith("Waiting"):
            received_msg = receive_message(sock)
            print("Server response:", received_msg)
            time.sleep(1)
        
        elif received_msg.startswith("gameover"):
             
             isGameOn = False
             print("gameover")
             sock.close()
             break
     
                  

def main():
    host = '10.0.2.15'  # Server's IP address
    port = 8080  # Server's port

    with connect_to_server(host, port) as sock:
        print("Connected to the server.")

        # Choose game mode: singleplayer or multiplayer
        game_mode = input("Enter game mode (singleplayer/multiplayer): ")
        board = Board(6, 7, ["red", "yellow"]) 
        board.set_game_mode(game_mode)
        res=start_game(sock,board.get_game_mode())
        global isGameOn
        isGameOn = True
        while isGameOn:
          
           
            
                if board.get_game_mode() == "singleplayer":
                    print("singleplayer")
                    print("now the current turn is " + board.Get_current_color())
                    if board.Get_current_color().lower() == "yellow":
                        input_move = board.input_and_set_cell()
                        board.print_board()
                        move=make_move(sock, input_move)
                        print(move)
                        process_ai_move_from_server(sock, board,move)
                elif board.get_game_mode() == "multiplayer":
                    print("multiplayer")
                    #ismymove2=ismymove(sock)
                    board.print_board()
                    
                    process_multiplayer_move_from_server(sock, board,res)
               
                else:

                    print("ma atha osa i metomtem po le po")
                
            
              #  print("somthin wrong in the inpeut section ")
#            else:
#                print("multiplayer")
#                board.input_and_set_cell()
#            y, color = board.check_win()
#            if y:
#                board.print_board()
#                print(f"The {color} wins!!!!")
#                return color
#        

if __name__ == "__main__":
    main()
