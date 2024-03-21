#id:311453906   Name:Guy Bard-dor
from locale import strcoll
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
# def wait_for_turn(sock):
#     while True:
#         response = receive_message(sock)
#         print("Server response:", response)
#         if response.startswith("your turn"):
#             return True
#         elif response.startswith("wait"):
#             time.sleep(1)  # מחכה ומנסה שוב לאחר שנייה
#         elif response.startswith("gameover"):
#             print("Game Over.")
#             return False    
def process_multiplayer_move_from_server(sock,board,received_msg):
    
    print(received_msg)
    global isGameOn
    while True:
        print(5)
        #your move in the first turn  yourmove ? 
        #here we need to take the recive message and take the move
        if received_msg.startswith("yourmove"):
            
            _, col_str = received_msg.split(',')
            enemycol=int(col_str)
            print(95)
            print(col_str)
            #print(received_msg)
            if enemycol >-1:
                enemyrow=board.find_lowest_available_row(enemycol)
                board.set_cell_color(enemyrow, enemycol, "red")  

            col = board.input_and_set_cell()
            row = board.find_lowest_available_row(col)
            #board.set_cell_color(row, col, "red")  
            board.print_board()
            make_multiplayer_move(sock,col)
            iswin,color= board.check_win()
            print(iswin)
            if iswin:
               isGameOn = False
               print("gameover")
               sock.close()
               break  # Assuming we exit the loop after processing the AI move; adjust as needed
        # elif received_msg.startswith("rival_move_multiplayer"):
        #     _, row_str, col_str = received_msg.split(',')
        #     colum=int(col_str)
        #     board.set_cell_color(row, col, "red")  
        #     board.print_board()
        #     print("Server response:", received_msg)   
        elif received_msg.startswith("Waiting"):
            received_msg = receive_message(sock)
            print("Server response:", received_msg)
            #break
            ## gbd add 
        
        elif received_msg.startswith("game-over"):
             
             isGameOn = False
             print("gameover")
             sock.close()
             break
     
                  

def main():
    #'inpt you server id host '10.0.2.15'
    # host =input("input you server host :")   # Server's IP address
    # str_port =input("input port number : ")   # Server's port
    # port= int(str_port)
    host="10.0.2.15"   # Server's port
    port=8080
    with connect_to_server(host, port) as sock:
        print("Connected to the server.")

        # Choose game mode: singleplayer or multiplayer
        str_game_mode = input("Enter game mode for singleplayer press 1 , multiplayer press 2 , game-over press 3 ")
        game_mode = int( str_game_mode)
        board = Board(6, 7, ["red", "yellow"]) 
        board.set_game_mode(game_mode)
        print(board.get_game_mode())
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
