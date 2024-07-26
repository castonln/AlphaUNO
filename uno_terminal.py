import os
import importlib
import inspect
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from engine.terminal_utils import *
from engine.uno_game import UnoGame
from engine.players.terminal_player import TerminalPlayer
from engine.players.player import Player
from engine.exceptions import NotEnoughCardsException

folder_path = "./engine/players"
file_names = [f for f in os.listdir(folder_path) if f.endswith('.py')]
                
if __name__ == '__main__':
    os.system("cls")  # clear and enable ansi escape
    print(f"""\
{COLORCODE['ENDC']}  ___  _       _          {COLORCODE['Red']} _   _{COLORCODE['Blue']} _   _{COLORCODE['Yellow']} _____{COLORCODE['Green']} _ 
{COLORCODE['ENDC']} / _ \| |     | |         {COLORCODE['Red']}| | | {COLORCODE['Blue']}| \ | {COLORCODE['Yellow']}|  _  {COLORCODE['Green']}| |
{COLORCODE['ENDC']}/ /_\ \ |_ __ | |__   __ _{COLORCODE['Red']}| | | {COLORCODE['Blue']}|  \| {COLORCODE['Yellow']}| | | {COLORCODE['Green']}| |
{COLORCODE['ENDC']}|  _  | | '_ \| '_ \ / _` {COLORCODE['Red']}| | | {COLORCODE['Blue']}| . ` {COLORCODE['Yellow']}| | | {COLORCODE['Green']}| |
{COLORCODE['ENDC']}| | | | | |_) | | | | (_| {COLORCODE['Red']}| |_| {COLORCODE['Blue']}| |\  {COLORCODE['Yellow']}| |_| {COLORCODE['Green']}|_|
{COLORCODE['ENDC']}\_| |_/_| .__/|_| |_|\__,_|{COLORCODE['Red']}\___/{COLORCODE['Blue']}\_| \_/{COLORCODE['Yellow']}\___/{COLORCODE['Green']}(_)
        {COLORCODE['ENDC']}| |                                    
        {COLORCODE['ENDC']}|_|                          Beta v1.0
        """)

    print(f"{STYLE['BOLD']}~ A Python-coded UNO game engine for AI experimentation. ~{STYLE['ENDS']}\n")

    print('Play a game or simulate games between bots?\n0) Simulate between bots\n1) Play against bots')
    human_included = select_option(0,1)
    players = []
    for file_name in file_names:
        module_name = f"engine.players.{file_name[:-3]}"  # Create the full module path
        module = importlib.import_module(module_name)
        
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Player) and obj != Player and obj != TerminalPlayer:
                num = int(input(f'Number of {name}s: '))
                for i in range(num):
                    players.append(obj(name = f'{name} {i + 1}'))

    if human_included:
        players.append(TerminalPlayer(name = f'Human'))
        game = UnoGame(players = players)
        while not game.winner:
            # Pre-turn information
            print(f"\n{STYLE['BOLD']}******* {game.current_player}'s Turn *******{STYLE['ENDS']}\n")
            print(f"{STYLE['BOLD']}Discard Top: {COLORCODE[game.discard_top.color]}{game.discard_top}{COLORCODE['ENDC']}\n")
            if isinstance(game.current_player, TerminalPlayer):
                for player in game.player_list:
                    if player != game.current_player:
                        player_hand_size = len(player.hand)
                        print(f"{STYLE['BOLD']}{player} holds {player_hand_size} cards{STYLE['ENDS']}", end = ' ')
                        if player_hand_size == 1:
                            print(f"- {COLORCODE['Red']}U{COLORCODE['Blue']}N{COLORCODE['Yellow']}O{COLORCODE['Green']}!{COLORCODE['ENDC']}\n")
                        else:
                            print(end = '\n')
            try:
                game.play_turn()
            except NotEnoughCardsException:
                break

        print(f'{COLORCODE["MAGENTA"]}{game.winner} wins!{COLORCODE["ENDC"]}')

    else:
        # {'player' : int(num of wins)}
        player_wins = {}

        num_of_games = int(input('Number of games to be run: '))
        for iteration in range(num_of_games):
            game = UnoGame(players = players)
            while not game.winner:
                try:
                    game.play_turn()
                    # print(game.de.encoded_data)
                except NotEnoughCardsException:
                    break
            winner = str(game.winner)
            print(f'{COLORCODE["MAGENTA"]}{winner} wins!{COLORCODE["ENDC"]}')

            # append to the dictionary of player wins
            if winner in player_wins:
                player_wins[winner] += 1
            else:
                player_wins[winner] = 1

            # how close was each game? this could be another plot in future additions
            for player in game.player_list:
                print(f'{player} held {len(player.hand)} cards.')

        players = list(player_wins.keys())

        # alphabetize the players
        players.sort()
        player_wins = {i: player_wins[i] for i in players}

        wins = list(player_wins.values())
        
        fig = plt.figure(figsize = (10, 5))
        plt.bar(players, wins, color ='green', width = 0.8)
        plt.xlabel("Players")
        plt.ylabel("No. of wins")
        plt.title(f"Wins over {num_of_games} games")
        plt.show()