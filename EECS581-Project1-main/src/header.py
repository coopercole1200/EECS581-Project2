"""
New Team
Description: Header for Minesweeper Game.
Authors: Cole Cooper, Manu Redd, Riley England, Jackson Yanek, Evans Chigweshe
External Sources: Generative AI, Pygame documentation, NumPy documentation
"""


"""
Functions:
init_header -> load/scale header assets (images, fonts)
draw_header -> render header (planks, wheel, compass, buoy count, timer, "NOW PLAYING")

Inputs: 
display size, header height, buoys left, start time, stopped state, elapsed time

Outputs: 
Header bar drawn on game surface

Authors: Jacob Richards, Riley Anderson, Ryland Edwards Dustin Le
Outside sources: minor chatpgt and github copilot 
Creation Date: 9/9
"""
import pygame
import time

_ASSETS = None
_FONTS = None

def init_header(display_width: int, header_height: int):
    """Load & scale images / fonts once for the header."""
    global _ASSETS, _FONTS
    if _ASSETS is not None:
        # If window size changes, rescale planks to new width/height.
        _ASSETS["planks"] = pygame.transform.smoothscale(
            _ASSETS["planks_raw"], (display_width, header_height)
        )
        return

    # --- images ---
    planks_raw = pygame.image.load("textures/planks.png").convert_alpha()
    wheel_raw  = pygame.image.load("textures/wheel.png").convert_alpha()
    compass_raw = pygame.image.load("textures/compass.png").convert_alpha()
    buoy_raw   = pygame.image.load("textures/buoy.png").convert_alpha()

    wheel   = pygame.transform.smoothscale(wheel_raw,   (100, 100))
    compass = pygame.transform.smoothscale(compass_raw, (100, 100))
    buoy    = pygame.transform.smoothscale(buoy_raw,    (40, 80))
    planks  = pygame.transform.smoothscale(planks_raw,  (display_width, header_height))

    _ASSETS = {
        "planks_raw": planks_raw,
        "planks": planks,
        "wheel": wheel,
        "compass": compass,
        "buoy": buoy,
    }

    # --- fonts ---
    font_buoys = pygame.font.SysFont("arial", 36, bold=True)   # buoy count
    font_timer = pygame.font.SysFont("arial", 24, bold=True)   # timer
    _FONTS = {"buoys": font_buoys, "timer": font_timer}


def draw_header(surface: pygame.Surface, buoys_left: int, start_time: float,
                display_width: int, header_height: int, stopped, elapsedT):
    """Blit the header onto the given surface (top-left at 0,0)."""
    if _ASSETS is None:
        init_header(display_width, header_height)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    planks  = _ASSETS["planks"]
    wheel   = _ASSETS["wheel"]
    compass = _ASSETS["compass"]
    buoy    = _ASSETS["buoy"]

    font_buoys = _FONTS["buoys"]
    font_timer = _FONTS["timer"]

    # Background
    surface.blit(planks, (0, 0))

    # Wheel centered
    surface.blit(
        wheel,
        (display_width // 2 - wheel.get_width() // 2,
         header_height // 2 - wheel.get_height() // 2)
    )

    # Add NOW PLAYING text to wheel
    if not stopped:
        playing_text = font_timer.render("NOW PLAYING", True, WHITE)
        playing_shadow = font_timer.render("NOW PLAYING", True, BLACK)
        text_x = display_width // 2 - playing_text.get_width() // 2
        text_y = (wheel.get_height() // 2 + playing_text.get_height() // 2)
        surface.blit(playing_shadow, (text_x + 1, text_y + 1))
        surface.blit(playing_text, (text_x, text_y))

    # Compass on the right
    compass_x = display_width - compass.get_width() - 30
    compass_y = header_height // 2 - compass.get_height() // 2
    surface.blit(compass, (compass_x, compass_y))

    # Timer to the LEFT of the compass (with a soft shadow so it pops on wood)
    if not stopped:
        elapsed = int(time.time() - start_time)
    else:
        elapsed = elapsedT  # keep it frozen
    t_img = font_timer.render(str(elapsed), True, WHITE)
    t_shadow = font_timer.render(str(elapsed), True, BLACK)
    tx = compass_x - 10 - t_img.get_width()
    ty = compass_y + compass.get_height() // 2 - t_img.get_height() // 2
    surface.blit(t_shadow, (tx + 1, ty + 1))
    surface.blit(t_img, (tx, ty))

    # Buoy + count on the left (with a soft shadow)
    buoy_x = 10
    buoy_y = header_height // 2 - buoy.get_height() // 2
    surface.blit(buoy, (buoy_x, buoy_y))

    b_img = font_buoys.render(str(buoys_left), True, WHITE)
    b_shadow = font_buoys.render(str(buoys_left), True, BLACK)
    bx = buoy_x + buoy.get_width() + 5
    by = header_height // 2 - b_img.get_height() // 2
    surface.blit(b_shadow, (bx + 1, by + 1))
    surface.blit(b_img, (bx, by))
