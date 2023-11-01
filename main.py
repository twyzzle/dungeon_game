### CODE IS DEMONSTRATIVE ONLY, DOES NOT WORK.

# main.py

from player import Player
from scenery import Scenery
from game import Game

# Create instances of your classes
player = Player()
scenery = Scenery()

# Start the game
game = Game(player, scenery)
game.run()

