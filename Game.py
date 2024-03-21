#id:311453906   name : Guy Bar-dor
from colorama import Fore, Style, init
init(autoreset=True)  # הפעלת colorama, עם אופציה לאיפוס הצבע לאחר כל הדפסה
# הגדרת מחלקת תא

import random

class Cell:
    # פונקציה ליצירת אובייקט חדש של תא, מקבלת האם התא זמין ואת הצבע שלו
    def __init__(self, available=True, color=None): 
        self.available = available  # הגדרת התא כזמין לברירת מחדל
        self.color = color  # הגדרת הצבע של התא

    # פונקציה להדפסת הצבע של התא
    def print_color(self):
        if self.color == 'red':
            print(Fore.RED + self.color)
        elif self.color == 'yellow':
            print(Fore.YELLOW + self.color)
        else:
            print(self.color)

    # פונקציה להגדרת התא כזמין או לא זמין
    def set_available(self, available): 
        self.available = available  # עדכון הסטטוס של התא

    # פונקציה להגדרת הצבע של התא
    def set_color(self, color): 
        self.color = color.lower()  # עדכון הצבע של התא

    # פונקציה לבדיקת אם התא זמין
    def available_cell(self): 
        return self.available  # מחזירה את הסטטוס של התא

    

# הגדרת מחלקת לוח
class Board:
    # פונקציה ליצירת אובייקט חדש של לוח, מקבלת מספר שורות, עמודות וצבעים
    def __init__(self, rows, columns, colors):
        self.rows = rows  # הגדרת מספר השורות בלוח
        self.columns = columns  # הגדרת מספר העמודות בלוח
        self.colors = colors  # הגדרת הצבעים המשמשים בלוח
        self.current_color="yellow"
        # יצירת לוח של תאים, כאשר כל תא הוא אובייקט של המחלקה Cell
        self.grid = [[Cell() for _ in range(columns)] for _ in range(rows)]
        self.game_mode = ""
        

    # פונקציה להגדרת הצבע של תא מסוים בלוח
    def set_cell_color(self, row, column, color):
        print("set cell color")  # הדפסת הודעה
        # בדיקה אם האינדקסים תקינים והתא זמין
        if 0 <= row < self.rows and 0 <= column < self.columns:
            if self.grid[row][column].available:  # בדיקה אם התא זמין
                self.grid[row][column].set_color(color)  # עדכון הצבע של התא
                self.grid[row][column].print_color()  # הדפסת הצבע של התא
                self.grid[row][column].set_available(False)  # סימון התא כלא זמין
                if self.current_color=="yellow":
                    self.current_color="red"
                    
                else:
                    self.current_color="yellow"
                return True   

            else:
                print("That cell is not available. Choose another one.")  # הדפסת הודעת שגיאה אם התא לא זמין
        
        else:
            print("Error: Invalid row or column index.")  # הדפסת הודעת שגיאה אם האינדקסים לא תקינים
        return False
    #get current color
    def Get_current_color(self):
        return self.current_color
    
    def set_current_color(self):
        self.Get_current_color("the currenct color is " + self.Get_current_color()) 
        if(self.Get_current_color() == 'red'):
            self.current_color = "yellow"
        else :
            self.current_color = "red"
    def print_current_color(self):
        print("the current color is " + self.current_color)

    # פונקציה להדפסת הלוח
    def print_board(self):
        color_map = {
            'red': Fore.RED,
            'yellow': Fore.YELLOW,
            'none': ''
        }
        max_color_length = max(
            (len(cell.color) for row in self.grid for cell in row if cell.color), default=5
        )
        cell_width = max(max_color_length + 2, 7)  # Ensure minimum cell width to fit 'yellow'
        separator = ("+" + "-" * cell_width) * self.columns + "+"
        print(separator)

        for row in self.grid:
            cell_row = "|"
            for cell in row:
                cell_color = color_map.get(cell.color, '')  # Get the color code
                cell_content = cell.color if cell.color else " " * (cell_width - 2)
                # Wrap the content in the color code, and reset the style after the content
                formatted_content = f"{cell_color}{cell_content.center(cell_width - 2)}{Style.RESET_ALL}"
                cell_row += f" {formatted_content} |"
            print(cell_row)
            print(separator)

    # פונקציה לקבלת תא מסוים בלוח
    def get_cell(self, row, column):
        # בדיקה אם האינדקסים תקינים
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.grid[row][column]  # החזרת התא
        else:
            print("Invalid row or column index")  # הדפסת הודעת שגיאה אם האינדקסים לא תקינים
            return None

    # פונקציה למציאת השורה הנמוכה ביותר הזמינה בעמודה מסוימת
    def find_lowest_available_row(self, col):
        for row in range(self.rows-1, -1, -1):  # לולאה מהשורה האחרונה לראשונה
            if self.grid[row][col].available:  # בדיקה אם התא זמין
                return row  # החזרת האינדקס של השורה
        return -1  # החזרת -1 אם אין שורה זמינה

    def input_and_set_cell(self):
        try:
            print("the current playet is :"+self.current_color)
            user_input = input("Enter column,  (e.g. 1,2, 3 ,4,5,6): ")  # קבלת קלט מהמשתמש
            col = user_input  # פיצול הקלט לעמודה וצבע
            col = int(col) - 1  # התאמת האינדקס של העמודה לאינדקס בפייתון
            print(col,self.current_color)
            # בדיקה אם העמודה תקינה והצבע הוא מחרוזת
            if col < 0 or col >= self.columns or not self.current_color.isalpha() :
                print("Error: Column is out of bounds.")  # הדפסת שגיאה אם העמודה לא תקינה
                return
            else: 
                row = self.find_lowest_available_row(col)  # מציאת השורה הנמוכה ביותר הזמינה
                self.set_cell_color(row, col, self.current_color)  # קביעת הצבע לתא
                print(f"Set cell ({row+1}, {col+1}) to color {self.current_color}.")  # הדפסת הודעת אישור
                return row ,col + 1, self.current_color

        except ValueError as e:
            print(f"Invalid input. Please enter column, and color separated by spaces. Error: {e}")  # הדפסת שגיאה אם הקלט לא תקין

    # פונקציה לבדיקת ניצחון על ידי קו מסוים
    def check_line_win(self, start_row, start_col, d_row, d_col, color):
        consecutive_count = 0  # מונה לספירת צבעים רצופים
        r, c = start_row, start_col  # התחלה מנקודת התחלה מסוימת
        # לולאה שרצה כל עוד אנחנו בתוך הגבולות של הלוח
        while 0 <= r < self.rows and 0 <= c < self.columns:
            if self.grid[r][c].color == color:  # אם הצבע של התא תואם
                consecutive_count += 1  # עדכון המונה
                if consecutive_count == 4:  # אם מצאנו 4 רצופים
                    return True  # יש ניצחון
            else:
                consecutive_count = 0  # איפוס המונה אם הסדרה נקטעת
            r += d_row  # תקדם בשורות לפי הפרמטר
            c += d_col  # תקדם בעמודות לפי הפרמטר
        return False  # אם לא מצאנו 4 רצופים
    def teko():
        pass
    #need to implement 
    # פונקציה לבדיקת ניצחון בלוח
    def check_win(self):
        # לולאה על כל הצבעים בלוח
        for color in self.colors:  
            # דריכה על כל השורות והעמודות
            for row in range(self.rows):
                for col in range(self.columns):
                    if self.grid[row][col].color == color:
                        # בדיקת כל הכיוונים לניצחון
                        if self.check_line_win(row, col, 0, 1, color):  # אופקי
                            return True,color
                        if self.check_line_win(row, col, 1, 0, color):  # אנכי
                            return True,color
                        if self.check_line_win(row, col, 1, 1, color):  # אלכסוני ימינה למטה
                            return True,color
                        if self.check_line_win(row, col, 1, -1, color):  # אלכסוני שמאלה למטה
                            return True,color
        return False,"none"  # אם לא נמצא ניצחון
    #ai move
    def ai_move(self):
        print("ai move")
        available_columns = [col for col in range(self.columns) if self.find_lowest_available_row(col) != -1]
        if available_columns:
            col = random.choice(available_columns)  # Randomly choose from available columns
            row = self.find_lowest_available_row(col)
            self.set_cell_color(row, col, self.current_color)
            print(f"AI ({self.current_color}) placed a piece in column {col + 1}")
            return row, col 
        else:
            print("No available moves for the AI.")
        

    def set_game_mode(self,gmaemode):
        self.game_mode = gmaemode

    def get_game_mode(self):
        return self.game_mode


    def Game(self, c_game_mode):
        game_mode = c_game_mode
        print("game mode is " + game_mode)
        isGameOn = True
        while isGameOn:
            self.print_board()
            if game_mode.lower() == "singalplayer":
                print("we are goint to play singleplayer")
                if self.Get_current_color().lower() == "yellow":
                    self.input_and_set_cell()
                else:
                    self.ai_move()
            elif game_mode.lower() == "multiplayer":
                print("we are goint to play multiplayer")
                self.input_and_set_cell()
            y, color = self.check_win()
            if y:
                self.print_board()
                print(f"The {color} wins!!!!")
       
#board = Board(6, 7, ["red", "yellow"])    # מספר הסיבובים לשחק
#board.Game()
      