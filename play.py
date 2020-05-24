#! /usr/bin/env python3
# coding: utf-8

"""start the states machine"""

from manager import Manage, Menu, Game

app = Manage()

state_dict = {"menu": Menu(), "game": Game()}
app.setup_states(state_dict, "menu")
app.main_game_loop()
