"""
App that starts with 3 panels. (`top_panel`, `middle_panel` and `bottom_panel`)
"""
from typing import Union

import pygame
from pygame_gui.elements import UIPanel

from pygame_gui_extras.app import GuiApp


class ThreePanelApp(GuiApp):
    """
    GuiApp that starts out with 3 panels which completely fill the screen.

    Add elements to each of the panels rather than to the ThreePanelApp object.
    """
    def __init__(self, *args,
                 top_height: Union[int, float] = 100,
                 bottom_height: Union[int, float] = 100,
                 heights_as_fractions: bool = False,
                 margins: Union[list, None] = None):
        """
        Create an instance of ThreePanelApp.

        Specify the heights of the top and bottom panels using `top_height` and `bottom_height`.
        The middle panel will be sized to fit the remaining space.

        Use `height_as_fractions` to specify how to interpret `top_height` and `bottom_height`.

        :param args: Args to pass to base class
        :param top_height: Sets the height of the top panel. (see `heights_as_fractions`)
        :param bottom_height: Sets the height of the bottom panel. (see `heights_as_fractions`)
        :param heights_as_fractions: If this is True, `top_height` and `bottom_height` will be interpreted
            as floating point fractions and the actual panel heights will be calculated from the root
            window's height. If this is False, the heights will be interpreted as pixel values.
        :param margins:
        """
        super().__init__(*args)
        if heights_as_fractions and (top_height > 1.0 or bottom_height > 1.0 or top_height + bottom_height > 1.0):
            raise Exception('Panels will not fit. Total is > 100%.')
        if not heights_as_fractions and (top_height + bottom_height > self.root_window_surface.get_height()):
            raise Exception('Panels will not fit. Total is > window height.')
        self._margins = margins
        self._top_height = top_height
        self._bottom_height = bottom_height
        window_height = self.root_window_surface.get_height()
        window_width = self.root_window_surface.get_width()
        _top_height = window_height * top_height if heights_as_fractions else top_height
        _bottom_height = window_height * bottom_height if heights_as_fractions else bottom_height
        _middle_height = window_height - _top_height - _bottom_height
        layer = 1
        if _middle_height <= 0:
            raise Exception('Panels will not fit. No room for middle panel.')
        self._top_panel = UIPanel(
            pygame.Rect(0, 0, window_width, _top_height), layer,
            self.ui_manager,
            margins=margins,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'right'
            }
        )
        self._bottom_panel = UIPanel(
            pygame.Rect(0,  -_bottom_height, window_width, _bottom_height), layer,
            self.ui_manager,
            margins=margins,
            anchors={
                'top': 'bottom',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'right'
            }
        )
        self._middle_panel = UIPanel(
            pygame.Rect(0, 0, window_width, window_height - (_top_height + _bottom_height)), layer,
            self.ui_manager,
            margins=margins,
            anchors={
                'top_target': self._top_panel,
                'bottom_target': self._bottom_panel,
                'top': 'top',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'right'
            }
        )

    @property
    def top_panel(self):
        """
        The top panel. Use this for adding elements to the top panel.
        :return: pygame_gui.UIPanel
        """
        return self._top_panel

    @property
    def middle_panel(self):
        """
        The middle panel. Use this for adding elements to the middle panel.
        :return: pygame_gui.UIPanel
        """
        return self._middle_panel

    @property
    def bottom_panel(self):
        """
        The bottom panel. Use this for adding elements to the bottom panel.
        :return: pygame_gui.UIPanel
        """
        return self._bottom_panel
