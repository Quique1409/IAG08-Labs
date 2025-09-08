"""
Main witch GUI from Battleship Game.
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, simpledialog
from threading import Thread
import random
import time
import os

#Export scripts from project Battleship
from Game import Game
from HumanPlayer import HumanPlayer
from ReflexAgentPlayer import ReflexAgentPlayer
from GoalBasedAgentPlayer import GoalBasedAgentPlayer

#Constants from the GUI appearance
CELL_SIZE = 35
BOARD_WIDTH = BOARD_HEIGHT = 10 * CELL_SIZE
PADDING = 10
#Escoger colores de los fondos
WINDOW_BG = "#D3D3D3" 
WATER_COLOR = "#ADD8E6"
SHIP_COLOR = "#A9A9A9"
HIT_COLOR = "#FF6347"
MISS_COLOR = "#FFFFFF"
FONT_FAMILY = "Helvetica"

class BattleshipGUI(tk.Tk):
    """
    The main class from GUI
    """
    def __init__(self):
        super().__init__()
        self.title("Battleship Project")
        self.config(bg=WINDOW_BG, padx = PADDING, pady = PADDING)
        self.resizable(False, False)

        #Font configuration
        self.title_font = tkfont.Font(family=FONT_FAMILY, size=16, weight="bold")
        self.button_font = tkfont.Font(family=FONT_FAMILY, size=12)
        self.label_font = tkfont.Font(family=FONT_FAMILY, size=12)

        #containers
        container = tk.Frame(self, bg=WINDOW_BG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        #Windows from menu, play, simulation
        for F in (MainMenu, GamePage, SimulationPage):
            page_name = F.__name__
            frame = F(parent = container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        """Show the frame"""
        frame = self.frames[page_name]
        frame.tkraise()

    def start_game(self, player2_class, player2_name):
        """Play game, and configuration the party"""
        self.frames["GamePage"].setup_game(HumanPlayer("Humane"), player2_class(player2_name))
        self.show_frame("GamePage")

    def start_simulation(self):
        """Simulation show"""
        self.show_frame("SimulationPage")

class MainMenu(tk.Frame):
    """Pantalla del Menú Principal."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=WINDOW_BG)
        self.controller = controller

        label = tk.Label(self, text="BATTLESHIP", font=controller.title_font, bg=WINDOW_BG)
        label.pack(side="top", fill="x", pady=20)

        # Buttons styles
        button_style = {'font': controller.button_font, 'height': 2, 'width': 30}

        btn1 = tk.Button(self, text="Humane vs simple reflex", **button_style,
                        command=lambda: controller.start_game(ReflexAgentPlayer, "Reflex AI"))
        btn1.pack(pady=10)

        btn2 = tk.Button(self, text="Humane vs goal-based", **button_style,
                        command=lambda: controller.start_game(GoalBasedAgentPlayer, "Goal-Based AI"))
        btn2.pack(pady=10)

        btn3 = tk.Button(self, text="Simultaion: IA vs. IA", **button_style,
                        command=lambda: controller.start_simulation())
        btn3.pack(pady=10)

        btn4 = tk.Button(self, text="Salir", **button_style,
                        command=self.quit)
        btn4.pack(pady=10)


class GamePage(tk.Frame):
    """The game window"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=WINDOW_BG)
        self.controller = controller
        self.game = None
        self.player1 = None
        self.player2 = None
        self.opponent_buttons = []

        top_frame = tk.Frame(self, bg=WINDOW_BG)
        top_frame.pack(pady=10)
        self.status_label = tk.Label(top_frame, text="Started..", font=controller.label_font, bg=WINDOW_BG, width=50)
        self.status_label.pack()

        boards_frame = tk.Frame(self, bg=WINDOW_BG)
        boards_frame.pack(padx=20, pady=10)
        
        # The user board
        p1_frame = tk.Frame(boards_frame, bg=WINDOW_BG)
        p1_frame.pack(side="left", padx=10)
        tk.Label(p1_frame, text="Board", font=controller.button_font, bg=WINDOW_BG).pack()
        self.player1_canvas = tk.Canvas(p1_frame, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=WATER_COLOR)
        self.player1_canvas.pack()

        # 
        p2_frame = tk.Frame(boards_frame, bg=WINDOW_BG)
        p2_frame.pack(side="right", padx=10)
        tk.Label(p2_frame, text="Opponent Board", font=controller.button_font, bg=WINDOW_BG).pack()
        self.player2_board = tk.Frame(p2_frame)
        self.player2_board.pack()
        self._create_opponent_grid()

        # Botón para volver al menú
        back_button = tk.Button(self, text="Menu", font=controller.button_font,
                                command=self.go_to_main_menu)
        back_button.pack(pady=20)

    def go_to_main_menu(self):
        """Displays a confirmation and returns to the main menu."""
        if messagebox.askyesno("Are you sure you want to left the game?"):
            self.controller.show_frame("MainMenu")

    def setup_game(self, player1, player2):
        """The new game congiguration"""
        self.player1 = player1
        self.player2 = player2
        self.game = Game(self.player1, self.player2) # La clase Game se encarga de colocar los barcos
        
        self.update_boards()
        self.status_label.config(text="Your turn! Click on your opponent's board to shoot.")
        self.enable_opponent_grid()

    def _create_opponent_grid(self):
        """Create the matrix from board"""
        self.opponent_buttons = []
        for r in range(10):
            row_list = []
            for c in range(10):
                btn = tk.Button(self.player2_board, text="", width=2, height=1, bg=WATER_COLOR,
                                command=lambda row=r, col=c: self.on_grid_click(row, col))
                btn.grid(row=r, column=c)
                row_list.append(btn)
            self.opponent_buttons.append(row_list)

    def on_grid_click(self, row, col):
        """The mouse event"""
        self.disable_opponent_grid()
        result = self.game.make_move((row, col))
        self.update_boards()

        if self.game.is_game_over(): #Se puede cambiar
            self.end_game()
            return
        
        self.status_label.config(text=f"You shot in ({row}, {col})... ¡{result}! Turn the IA.")
        self.controller.after(1500, self.play_ai_turn) # Espera 1.5s

    def play_ai_turn(self):
        """IA turn"""
        ai_move, result = self.game.jelou() #Cambiar por el método de nosotros 
        self.update_boards()

        if self.game.is_game_over():
            self.end_game()
            return
            
        self.status_label.config(text=f"The AI ​​shot in {ai_move}... ¡{result}! It's your turn")
        self.enable_opponent_grid()

    def update_boards(self):
        """Redraw both boards according to the current game state."""
        # Tablero del jugador
        self.player1_canvas.delete("all")
        
        p1_grid = self.player1.board  #depende de como accesamos al tablero
        for r in range(10):
            for c in range(10):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = WATER_COLOR
                cell = p1_grid[r][c]
                if cell == 'S': # Casilla sin nada
                    color = SHIP_COLOR
                elif cell == 'H': # Hit
                    color = HIT_COLOR
                elif cell == 'M': # Miss
                    color = MISS_COLOR
                self.player1_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # Tablero del oponente (se actualizan los botones)
        
        p2_tracking_grid = self.player1.tracking_board #Acceder la tablero de la IA
        for r in range(10):
            for c in range(10):
                cell = p2_tracking_grid[r][c]
                color = WATER_COLOR
                if cell == 'H':
                    color = HIT_COLOR
                elif cell == 'M':
                    color = MISS_COLOR
                self.opponent_buttons[r][c].config(bg=color, activebackground=color)

    def end_game(self):
        """Show the results"""
        winner_name = self.game.winner.name
        messagebox.showinfo("Finish", f"¡The winner is: {winner_name}!")
        self.disable_opponent_grid()
        self.status_label.config(text=f"The winner is: {winner_name}")

    def disable_opponent_grid(self):
        for row in self.opponent_buttons:
            for btn in row:
                btn.config(state="disabled")

    def enable_opponent_grid(self):
        p2_tracking_grid = self.player1.tracking_board #tablero con las casillas ya atacadas
        for r in range(10):
            for c in range(10):
                if p2_tracking_grid[r][c] is None: # O el valor que uses para "no atacado"
                    self.opponent_buttons[r][c].config(state="normal")

class SimulationPage(tk.Frame):
    """Display from simulation IA vs IA."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=WINDOW_BG)
        self.controller = controller
        
        tk.Label(self, text="simulation IA vs IA.", font=controller.title_font, bg=WINDOW_BG).pack(pady=20)
        
        input_frame = tk.Frame(self, bg=WINDOW_BG)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Count:", font=controller.label_font, bg=WINDOW_BG).pack(side="left", padx=5)
        self.num_games_entry = tk.Entry(input_frame, font=controller.label_font, width=10)
        self.num_games_entry.pack(side="left")
        self.num_games_entry.insert(0, "100") # Valor por defecto

        self.run_button = tk.Button(self, text="Run Simulation", font=controller.button_font, command=self.run_simulation_thread)
        self.run_button.pack(pady=20)
        
        self.result_text = tk.Text(self, height=10, width=60, font=controller.label_font, state="disabled")
        self.result_text.pack(pady=10)

        back_button = tk.Button(self, text="Menu", font=controller.button_font,
                                command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=10)

    def run_simulation_thread(self):
        """Inicia la simulación en un hilo separado para no congelar la GUI."""
        try:
            num_games = int(self.num_games_entry.get())
            if num_games <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número entero positivo.")
            return

        self.run_button.config(state="disabled")
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"Ejecutando {num_games} simulaciones...\n")
        self.result_text.config(state="disabled")

        # El hilo permite que la simulación se ejecute en segundo plano
        thread = Thread(target=self.execute_simulation, args=(num_games,))
        thread.start()

    def execute_simulation(self, num_games):
        """Lógica de la simulación (la que tenías en tu main)."""
        stats = {"Reflex AI": 0, "Goal-Based AI": 0}
        start_time = time.time()

        for i in range(num_games):
            p1 = ReflexAgentPlayer("Reflex AI")
            p2 = GoalBasedAgentPlayer("Goal-Based AI")
            
            game = Game(p1, p2) if random.choice([True, False]) else Game(p2, p1)
            
            winner = game.run_game(silent_mode=True)
            if winner:
                stats[winner.name] += 1
            
            # Actualiza la GUI de forma segura desde el hilo
            if (i + 1) % 10 == 0 or i == num_games - 1: #a las 10 se reinicia
                progress_msg = f"Game {i+1}/{num_games} finished\n"
                self.controller.after(0, self.update_results, progress_msg)

        end_time = time.time()
        total_time = end_time - start_time
        
        #Muestra de resultados finales
        final_results = "\n--- Simulation finished ---\n"
        final_results += f"Time: {total_time:.2f} seconds\n"
        
        reflex_wins = stats["Reflex AI"]
        goal_wins = stats["Goal-Based AI"]
        
        reflex_perc = (reflex_wins / num_games) * 100 if num_games > 0 else 0
        goal_perc = (goal_wins / num_games) * 100 if num_games > 0 else 0
        
        final_results += f"IA Victories: {reflex_wins} ({reflex_perc:.2f}%)\n"
        final_results += f"IA Pro Victories: {goal_wins} ({goal_perc:.2f}%)\n"
        
        self.controller.after(0, self.update_results, final_results)
        self.controller.after(0, lambda: self.run_button.config(state="normal"))

    def update_results(self, message):
        """Function to safely update the text widget."""
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, message)
        self.result_text.see(tk.END) # Auto-scroll
        self.result_text.config(state="disabled")


if __name__ == "__main__":
    app = BattleshipGUI()
    app.mainloop()