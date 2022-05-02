"""
Create a ThreePanelApp. Add labels to each of the panels identifying them.
"""
import pygame
from pygame_gui.elements import UILabel

from pygame_gui_extras.app.ThreePanelApp import ThreePanelApp

app = ThreePanelApp((1020, 800), top_height=.25, bottom_height=.10, heights_as_fractions=True)

UILabel(
    pygame.Rect(10,10,-1, -1),
    'Top Panel', app.ui_manager,
    container=app.top_panel,
    anchors={
        'top': 'top',
        'left': 'left',
        'bottom': 'top',
        'right': 'left'
    }
)
UILabel(
    pygame.Rect(10,10,-1, -1),
    'Middle Panel', app.ui_manager,
    container=app.middle_panel,
    anchors={
        'top': 'top',
        'left': 'left',
        'bottom': 'top',
        'right': 'left'
    }
)
UILabel(
    pygame.Rect(10,10,-1, -1),
    'Bottom Panel', app.ui_manager,
    container=app.bottom_panel,
    anchors={
        'top': 'top',
        'left': 'left',
        'bottom': 'top',
        'right': 'left'
    }
)
app.setup()
app.run()

