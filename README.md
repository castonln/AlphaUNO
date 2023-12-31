<p align="center">
  <img src="https://raw.githubusercontent.com/castonln/AlphaUNO/main/img/AlphaUNO-Logo.png" width="150" height="150">
 </p>
 <h1 align="center">AlphaUNO</h1>
 <p align="center">An UNO game engine for AI experimentation in Python.</p>

## How to setup and run
`pip install -r requirements.txt` in /AlphaUNO

For the simplest way to play, run `python uno_terminal.py` for a terminal implementation. From there, you can run bot-only simulations or play againt models of your choosing.

Bot vs bot simulations will run for a defined number of games and will return a nifty bar graph as seen below.

![Example graph](https://raw.githubusercontent.com/castonln/AlphaUNO/main/img/Figure_1.png)

## Ruleset
The game is played according to the most updated ruleset (2023). 

Disabling the Challenge Rule can be done in engine/standard_uno_config.py

Action Cards are continuously flipped at the start of the match until a number card is drawn for the top of the discard pile.

It is assumed that all players say "UNO" at the correct time. There is no "going out" mechanic.

## Creating your own AI
Create a .py file in engine/players

Inside, create a derived class from Player (engine.players.player) with the following behavior:
```python
from engine.players.player import Player
from engine.standard_uno_config import COLORS

class Bot(Player):  # Must be derived from Player
    def __init__(self, name):
        Player.__init__(self, name)

    def select_card(self, discard_top):
        """
        Activates at the start of a turn.
        Returns a a card object from self.hand (see Player obj) or 'd' to indicate drawing a card.
        """
        pass
    
    def select_color(self):
        """
        Activates when placing down a Wild Card.
        Returns a color from COLORS.
        """
        pass
    
    def select_renege(self, drawn_card):
        """
        Activates after drawing a card that is possible to be played on top of the game's current discard_top.
        Returns True to play drawn_card, False to keep in self.hand (see Player obj).
        """
        pass
    
    def challenge_select(self):
        """
        Activates when the player is the victim of a +4 and the CHALLENGERULE is True 
        (see the official UNO game rules and engine/standard_uno_config.py).
        Returns True to accept challenge, False to decline challenge.
        """
        pass
```
