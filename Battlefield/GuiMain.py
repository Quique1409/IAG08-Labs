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
WINDOW_BG = "#98DA4C" 
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
        self.frames["GamePage"].setup_game(HumanPlayer("Player"), player2_class(player2_name))
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

        btn1 = tk.Button(self, text="Player vs simple reflex (Easy)", **button_style,
                        command=lambda: controller.start_game(ReflexAgentPlayer, "Reflex AI"))
        btn1.pack(pady=10)

        btn2 = tk.Button(self, text="Player vs goal-based (Hard)", **button_style,
                        command=lambda: controller.start_game(GoalBasedAgentPlayer, "Goal-Based AI"))
        btn2.pack(pady=10)

        btn3 = tk.Button(self, text="Simulation: Reflex vs. Goal Based", **button_style,
                        command=lambda: controller.start_simulation())
        btn3.pack(pady=10)

        btn4 = tk.Button(self, text="Exit", **button_style,
                        command=self.quit)
        btn4.pack(pady=10)
        
# ---CREDITS SECTION ---
        credits_text = "Developed by:\nLeón Vargas Luis Guillermo\nMedrano Solano Enrique\nRamírez Valdovinos Eric\nRodríguez Zamora Joshua"
        credits_font = tkfont.Font(family=FONT_FAMILY, size=10, slant="italic")

        credits_label = tk.Label(self, text=credits_text, font=credits_font,
                                 bg=WINDOW_BG, fg="#333333")
        
        credits_label.pack(pady=(20, 10)) 

class GamePage(tk.Frame):
    """The game window"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=WINDOW_BG)
        self.controller = controller
        self.game = None
        self.player1 = None #Player
        self.player2 = None #IA
        self.opponent_buttons = []

        #Controles para la fase de colocación
        self.placement_frame = tk.Frame(self, bg=WINDOW_BG)
        tk.Label(self.placement_frame, text="Orientation:", font=controller.label_font, bg=WINDOW_BG).pack(side="left", padx=5)
        self.orientation_var = tk.StringVar(value='H') # Por defecto Horizontal
        horiz_radio = tk.Radiobutton(self.placement_frame, text="Horizontal", variable=self.orientation_var, value='H', font=controller.label_font, bg=WINDOW_BG)
        horiz_radio.pack(side="left")
        vert_radio = tk.Radiobutton(self.placement_frame, text="Vertical", variable=self.orientation_var, value='V', font=controller.label_font, bg=WINDOW_BG)
        vert_radio.pack(side="left")


        top_frame = tk.Frame(self, bg=WINDOW_BG)
        top_frame.pack(pady=10)
        self.status_label = tk.Label(top_frame, text="Starting..", font=controller.label_font, bg=WINDOW_BG, width=50)
        self.status_label.pack()

        boards_frame = tk.Frame(self, bg=WINDOW_BG)
        boards_frame.pack(padx=20, pady=10)
        
        # Player 1 (Your Board) Frame Setup with Coordinates
        # ==========================================================
        p1_coord_frame = tk.Frame(boards_frame, bg=WINDOW_BG)
        p1_coord_frame.pack(side="left", padx=10)

        tk.Label(p1_coord_frame, text="Your Board", font=controller.button_font, bg=WINDOW_BG).grid(row=0, column=1, columnspan=10, pady=5)

        # Column Headers (A, B, C...)
        for i in range(10):
            col_char = chr(ord('A') + i)
            tk.Label(p1_coord_frame, text=col_char, font=controller.label_font, bg=WINDOW_BG).grid(row=1, column=i + 1)

        # Row Headers (1, 2, 3...)
        for i in range(10):
            row_num = str(i + 1)
            tk.Label(p1_coord_frame, text=row_num, font=controller.label_font, bg=WINDOW_BG, padx=5).grid(row=i + 2, column=0)

        self.player1_canvas = tk.Canvas(p1_coord_frame, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=WATER_COLOR, highlightthickness=0)
        self.player1_canvas.grid(row=2, column=1, rowspan=10, columnspan=10)
        self.player1_canvas.bind("<Button-1>", self.on_canvas_click)

        # ==========================================================
        # Opponent's Board Frame Setup with Coordinates
        # ==========================================================
        p2_coord_frame = tk.Frame(boards_frame, bg=WINDOW_BG)
        p2_coord_frame.pack(side="right", padx=10)

        tk.Label(p2_coord_frame, text="Opponent's Board", font=controller.button_font, bg=WINDOW_BG).grid(row=0, column=1, columnspan=10, pady=5)

        # Column Headers (A, B, C...)
        for i in range(10):
            col_char = chr(ord('A') + i)
            tk.Label(p2_coord_frame, text=col_char, font=controller.label_font, bg=WINDOW_BG).grid(row=1, column=i + 1)
        
        # Row Headers (1, 2, 3...) on the right side
        for i in range(10):
            row_num = str(i + 1)
            tk.Label(p2_coord_frame, text=row_num, font=controller.label_font, bg=WINDOW_BG, padx=5).grid(row=i + 2, column=11)

        self.player2_board = tk.Frame(p2_coord_frame)
        self.player2_board.grid(row=2, column=1, rowspan=10, columnspan=10)
        self._create_opponent_grid() # This is now self-contained

        # Botón para volver al menú
        self.back_button = tk.Button(self, text="Menu", font=controller.button_font,
                                    command=self.go_to_main_menu)
        self.back_button.pack(pady=20)

    def go_to_main_menu(self):
        """Displays a confirmation and returns to the main menu."""
        if messagebox.askyesno("Are you sure you want to left the game?"):
            self.controller.show_frame("MainMenu")

    def setup_game(self, player1, player2):
        """The new game congiguration"""
        self.player1 = player1
        self.player2 = player2
        self.game = Game(self.player1, self.player2) # La clase Game solo guarda el estado de los barcos

        self.disable_opponent_grid() #se desabilita el board 
        #empieza colocación
        self.ships_to_place = list(self.player1.boat_fleet) #jugador
        self.player2.place_boats_randomly() #IA
        
        self.update_boards()
        self.back_button.pack_forget()
        self.placement_frame.pack(pady=10)
        self.start_next_placement()

    def start_next_placement(self):
        """Prepares the next ship to be placed by the player."""
        if self.ships_to_place:
            # Toma el siguiente barco de la lista
            current_ship = self.ships_to_place[0]
            self.status_label.config(text=f"Place your {current_ship.name}")
        else:
            # Si no quedan barcos, termina la fase de colocación
            self.end_placement_phase()

    def on_canvas_click(self, event):
        """Handles the click on the player's board during the placement phase."""
        # Si no estamos en fase de colocación, no hace nada
        if not self.ships_to_place:
            return

        # Convierte las coordenadas del clic (pixeles) a coordenadas de la cuadrícula (fila, columna)
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        current_ship = self.ships_to_place[0]
        orientation = self.orientation_var.get()

        # Intenta colocar el barco usando el método de la clase Grid
        if self.player1.own_grid.place_boat(current_ship, row, col, orientation):
            # Si se pudo colocar, lo elimina de la lista y pasa al siguiente
            self.ships_to_place.pop(0)
            self.update_boards()
            self.start_next_placement()
        else:
            # Si no se pudo, muestra un aviso
            messagebox.showwarning("Invalid Position", "You cannot place the ship there. Try another position")

    def end_placement_phase(self):
        """Colocation phase finished"""
        # Oculta los controles de colocación
        self.placement_frame.pack_forget()

        # Vuelve a mostrar el botón de "Volver al Menú"
        self.back_button.pack(pady=20)
        
        self.status_label.config(text="Your fleet has been deployed! The battle begins.\n It's your turn!")
        self.enable_opponent_grid()

    def _create_opponent_grid(self):
        """Creates the button matrix for the opponent's board."""
        self.opponent_buttons = []
        for r in range(10): # row
            row_list = []
            for c in range(10): # column
                # The parent is self.player2_board
                btn = tk.Button(self.player2_board, text="", width=2, height=1, bg=WATER_COLOR,
                                command=lambda row=r, col=c: self.on_grid_click(row, col))
                # The grid inside this frame starts at (0, 0)
                btn.grid(row=r, column=c)
                row_list.append(btn)
            self.opponent_buttons.append(row_list)

    def on_grid_click(self, row, col):
        """The mouse event from player real turn"""
        self.disable_opponent_grid() #se evitan click accidenatales
        result = self.game.other_player.own_grid.receive_shot(row, col) #registro del disparo (script Game)

        #Se acrtualiza el board para el seguimiento del jugador
        if result in ['HIT', 'SUNK']:
            self.game.current_player.opponent_grid.grid[row][col] = "X"
        else:
            self.game.current_player.opponent_grid.grid[row][col] = "M"

        self.update_boards() #Actualzia GUI
        coord = f"{chr(ord('A') + col)}{row + 1}" # Convertimos (r,c) a "A1"
        self.status_label.config(text= f"You targetted {coord}... {result}!\n Opponent turn." )

        #Termino el juego??
        if self.game.other_player.has_lost():
            self.game.winner = self.game.current_player
            self.end_game()
            return
        
        #Si sigue el juego entonces...
        self.game.current_player, self.game.other_player = self.game.other_player, self.game.current_player
        self.controller.after(1500, self.play_ai_turn) # Espera 1.5s

    def play_ai_turn(self):
        """IA turn, current_player = IA player"""
        row, col = self.game.current_player.make_shot() #IA decide su disparo.

        result = self.game.other_player.own_grid.receive_shot(row, col) #Dispara al player real (usuario)

         # Update the AI's own tracking grid so it doesn't shoot here again.
        if result in ['HIT', 'SUNK']:
            self.game.current_player.opponent_grid.grid[row][col] = "X"
        elif result == 'MISS':
            self.game.current_player.opponent_grid.grid[row][col] = "M"
   

        #Se actualzia el resultado interno de la IA
        self.update_ai_state(self.game.current_player, result, row, col)
        self.update_boards() #se actualiza el board del juego.

        coord = f"{chr(ord('A') + col)}{row + 1}" # Convertimos (r,c) a "A1"
        self.status_label.config(text=f"The opponent fired at {coord}... ¡{result}!\n It's your turn")

    #Termino el juego??
        if self.game.other_player.has_lost():
            self.game.winner = self.game.current_player
            self.end_game()
            return
        
        #Si sigue el juego entonces...
        self.game.current_player, self.game.other_player = self.game.other_player, self.game.current_player
        self.enable_opponent_grid()

    def update_ai_state(self, ai_player, result, row, col):
        """
        Helper function to update the AI ​​status after a shot.
        """
        if isinstance(ai_player, ReflexAgentPlayer):
            if result in ['HIT', 'SUNK']:
                ai_player.last_hit = (row, col)
                if result == 'SUNK':
                    ai_player.last_hit = None # Se reinicia al hundir
            else: # MISS
                ai_player.last_hit = None
        
        if isinstance(ai_player, GoalBasedAgentPlayer):
            if result in ['HIT', 'SUNK']:
                ai_player.mode = 'TARGET'
                if (row, col) not in ai_player.target_hits:
                    ai_player.target_hits.append((row, col))
                if result == 'SUNK':
                    # Reiniciamos solo si el barco hundido contenía los objetivos
                    sunk_boat_contains_targets = False
                    for boat in self.game.other_player.own_grid.boats:
                        if boat.is_sunk() and all(hit in boat.positions for hit in ai_player.target_hits):
                            sunk_boat_contains_targets = True
                            break
                    if sunk_boat_contains_targets:
                        ai_player.mode = 'HUNT'
                        ai_player.target_hits = []

    def update_boards(self):
        """Redraw both boards according to the current game state."""
        # Tablero del jugador
        self.player1_canvas.delete("all")
        
        if self.player1 and hasattr(self.player1, 'own_grid'):
            p1_grid = self.player1.own_grid.grid  #depende de como accesamos al tablero
            for r in range(10):
                for c in range(10):
                    x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                    color = WATER_COLOR
                    cell = p1_grid[r][c]
                    if cell == 'O': # Casilla sin nada
                        color = SHIP_COLOR
                    elif cell == 'X': # Hit
                        color = HIT_COLOR
                    elif cell == 'M': # Miss
                        color = MISS_COLOR
                    self.player1_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # Tablero del oponente (se actualizan los botones)        
        if self.player1 and hasattr(self.player1, 'opponent_grid'):
            p2_tracking_grid = self.player1.opponent_grid.grid #Acceder la tablero de la IA
            for r in range(10):
                for c in range(10):
                    cell = p2_tracking_grid[r][c]
                    color = WATER_COLOR
                    if cell == 'X':
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
        p2_tracking_grid = self.player1.opponent_grid.grid #tablero con las casillas ya atacadas
        for r in range(10):
            for c in range(10):
                if p2_tracking_grid[r][c] == '.': # O el valor que uses para "no atacado"
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