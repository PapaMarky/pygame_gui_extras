"""
Testing how root window resizing works in pygame_gui.

This is pure pygame_gui. No use of pygame_gui_extras classes

Tweak the layout parameters (anchors and container) and see what happens
when you resize the window.
"""

import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIPanel, UIDropDownMenu, UILabel

# BOILERPLATE
WINDOW_SIZE = (800, 600)

pygame.init()

pygame.display.set_caption('Resize Testing')
window_surface = pygame.display.set_mode(WINDOW_SIZE, flags=pygame.RESIZABLE)
manager = pygame_gui.UIManager(WINDOW_SIZE)

background_surface = pygame.Surface(WINDOW_SIZE)
BACKGROUND_FILL_COLOR = manager.ui_theme.get_colour('dark_bg')

clock = pygame.time.Clock()
is_running = True


def handle_resize():
    """
    Resize Event Handler
    :return: None
    """
    global background_surface
    new_size = window_surface.get_size()
    print(f'NEW SIZE: {new_size}')
    manager.set_window_resolution(new_size)
    background_surface = pygame.Surface(new_size)


# layout calculation variables
margin = 10
butt_w = 300
butt_h = 75
butt_x = window_surface.get_width() - margin - butt_w
butt_y = window_surface.get_height() - margin - butt_h
br_rect = pygame.Rect(0, 0, butt_w, butt_h)
br_rect.bottomright = (-margin, -margin)
print(f'UIButton rect: {br_rect}')
# Prints: "UIButton rect: <rect(-310, -85, 300, 75)>"
# Anchor values are relative to the anchored position.
# Because we are anchoring this element's (top, left) to the (bottom, right)
# of the containing element (screen in this case), we use negative values
# for x and y.
# If you anchor to bottom or right and provide positive x or y the element
# will be positioned off of the drawing surface and will not be shown.
#
br_button = UIButton(
    br_rect,
    'Toggle Layer Debug',
    manager,
    anchors={
        'top': 'bottom',  # x position relative to bottom of container
        'left': 'right',  # y position relative to right of container
        'bottom': 'bottom',
        'right': 'right'
    }
)
panel_x = margin
panel_y = margin
panel_w = window_surface.get_width() - (2 * margin)
panel_h = window_surface.get_height() / 3
panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
print(f'UIPanel(top) rect: {panel_rect}')
# Prints: "UIPanel(top) rect: <rect(10, 10, 780, 200)>"
# We anchor the (top, left) to (top, left) so we use positive values for
# x, y.
# We are anchoring our right side to the right side of the container, so
# when the container's width changes, this element will stretch or shrink
# to maintain the distance between the right side of this element and the
# right side of the container.
top_panel = UIPanel(
    panel_rect,
    1,
    manager,
    anchors={
        'top': 'top',
        'left': 'left',
        'bottom': 'top',
        'right': 'right'
    },
)
label_rect = pygame.Rect(0, 0, 200, butt_h)
print(f'label_rect: {label_rect}')
# Prints: "label_rect: <rect(0, 0, 200, 75)>"
# We specify our container as 'top_panel', so our anchor is relative to that
# element. Changes in position or size of `top_panel` will affect this element.
# We set our position to 0, 0 and anchor our (top, left) to the (top, left) of
# `top_panel`. This will keep our top, left at the top, left of the top_panel.
label = UILabel(label_rect,
                'Some Options:',
                manager,
                container=top_panel,
                anchors={
                    'top': 'top',
                    'left': 'left',
                    'bottom': 'top',
                    'right': 'right'
                }

                )

drop_down_rect = pygame.Rect(0, 0, 200, butt_h)
print(f'drop_down_rect: {drop_down_rect}')
# Prints: "drop_down_rect: <rect(0, 0, 200, 75)>"
# We specify our container as 'top_panel', so our anchor is relative
# to that element.
# This part is a little tricky. Remember that anchor targets are reversed. This means that
# specifying a left_target will anchor our left side to the targets right side.
# For the Dropdown menu we anchor (top, left) to (top, left). Our x, y
# is relative to top, left of the anchor target, so we use positive x,y
# in the relative_rect.
# We specify our left_target as the UILabel we created above, so our left
# side (y) is relative to the right side (y + width) of `label`.
# We anchor our (bottom, right) to the (top, right) of our container.
drop_down = UIDropDownMenu(
    ['option 1', 'option 2', 'option 3', 'option 4', 'option 5', 'option 6'],
    'option 2',
    drop_down_rect,
    manager,
    container=top_panel,
    anchors={
        'top': 'top',
        'left': 'left',
        'bottom': 'top',
        'right': 'right',
        'left_target': label
    }
)

# mid_panel:
# top and bottom both anchored to top of target, so no vertical stretching. (we maintain height)
# specify top_target as `top_panel`, so our top follows the bottom of `top_panel`
mid_panel = UIPanel(
    pygame.Rect(panel_x, panel_y, panel_w, panel_h),
    1,
    manager,
    anchors={
        'top': 'top',
        'left': 'left',
        'bottom': 'top',
        'right': 'right',
        'top_target': top_panel
    }
)
DEBUG_MODE = False
manager.set_visual_debug_mode(DEBUG_MODE)
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.WINDOWRESIZED:
            print(f'WINDOWRESIZED: {event}')
        if event.type == pygame.VIDEORESIZE:
            print(f'VIDEORESIZE: {event}')
        if event.type == pygame.WINDOWSIZECHANGED:
            print(f'WINDOWSIZECHANGED: {event}')
            handle_resize()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == br_button:
            DEBUG_MODE = not DEBUG_MODE
            manager.set_visual_debug_mode(DEBUG_MODE)

        manager.process_events(event)
    background_surface.fill(BACKGROUND_FILL_COLOR)
    manager.update(time_delta)

    window_surface.blit(background_surface, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
