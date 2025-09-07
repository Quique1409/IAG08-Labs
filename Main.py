def main():
    """Main function to run the Battleship game menu."""
    while True:
        clear_screen()
        print(" B A T T L E S H I P")
        print("======================")
        print("1. Humano vs. IA Refleja")
        print("2. Humano vs. IA Basada en Objetivos")
        print("3. Simulación: IA vs. IA")
        print("4. Salir")
        choice = input("Elige una opción (1-4): ")

        if choice == '1':
            player1 = HumanPlayer("Humano")
            player2 = ReflexAgent()
            game = Game(player1, player2)
            game.run_game()
            input("\nPresiona Enter para volver al menú.")
        elif choice == '2':
            player1 = HumanPlayer("Humano")
            player2 = GoalBasedAgent()
            game = Game(player1, player2)
            game.run_game()
            input("\nPresiona Enter para volver al menú.")
        elif choice == '3':
            try:
                num_games = int(input("¿Cuántas partidas deben jugar las IAs? "))
            except ValueError:
                print("Número inválido. Por favor, ingresa un entero.")
                time.sleep(2)
                continue
            
            stats = { "Reflex AI": 0, "Goal-Based AI": 0 }
            print(f"\nEjecutando {num_games} simulaciones...")
            for i in range(num_games):
                p1 = ReflexAgent()
                p2 = GoalBasedAgent()
                # Intercambia aleatoriamente quién empieza para que sea justo
                if random.choice([True, False]):
                    game = Game(p1, p2)
                else:
                    game = Game(p2, p1)
                
                winner = game.run_game(silent_mode=True)
                stats[winner.name] += 1
                print(f"Partida {i+1}/{num_games} completa. Ganador: {winner.name}")

            print("\n--- Simulación Completa ---")
            print(f"Victorias IA Refleja: {stats['Reflex AI']} ({stats['Reflex AI']/num_games:.2%})")
            print(f"Victorias IA Basada en Objetivos: {stats['Goal-Based AI']} ({stats['Goal-Based AI']/num_games:.2%})")
            input("\nPresiona Enter para volver al menú.")
        elif choice == '4':
            print("¡Gracias por jugar!")
            break
        else:
            print("Opción inválida, por favor intenta de nuevo.")
            time.sleep(2)

if __name__ == "__main__":
    main()