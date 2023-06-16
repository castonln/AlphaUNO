import os
import matplotlib.pyplot as plt
from engine.terminal_utils import *
from engine.uno_game import UnoGame
from engine.players.terminal_player import TerminalPlayer
from engine.exceptions import NotEnoughCardsException

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
    num_of_wild = int(input('Number of Wild Card Bots: '))
    num_of_random = int(input('Number of Random Bots: '))

    if human_included:
        game = UnoGame(wild_bots = num_of_wild, random_bots = num_of_random, human_included = human_included)
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
            game.check_win()

        print(f'{COLORCODE["MAGENTA"]}{game.winner} wins!{COLORCODE["ENDC"]}')

    else:
        # {'player' : int(num of wins)}
        player_wins = {}

        num_of_games = int(input('Number of games to be run: '))
        for iteration in range(num_of_games):
            game = UnoGame(wild_bots = num_of_wild, random_bots = num_of_random, human_included = human_included)
            while not game.winner:
                try:
                    game.play_turn()
                except NotEnoughCardsException:
                    break
                game.check_win()
            
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