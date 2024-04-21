import math
import random

import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
import copy as cp # the copy module is used for copying tile positions


# Define a list of colors for different tile numbers
tile_colors = [
   Color(238, 228, 218),
   Color(236, 224, 202),
   Color(242, 177, 121),
   Color(245, 149, 101),
   Color(245, 124, 95),
   Color(246, 93, 59),
   Color(237, 207, 114),
   Color(237, 204, 97),
   Color(236, 200, 80),
   Color(239, 197, 63),
   Color(238, 194, 46),
   Color(107, 101, 89)
]


# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and font size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # A constructor that creates a tile with 2 as the number on it
   def __init__(self):
      # set the number on this tile
      self.number = random.choice([2, 4])
      # set the colors of this tile
      # Set the colors of this tile based on the tile number
      tile_color_index = int(math.log(self.number, 2)) - 1
      self.background_color = tile_colors[tile_color_index]
      self.foreground_color = Color(0, 0, 0)  # Black text color
      self.box_color = Color(188, 173, 165)  # Box (boundary) color


   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1):  # length defaults to 1
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))

   # Setter method for the position of the tile
   def set_position(self, position):
      # set the position of the tile as the given position
      self.position = cp.copy(position)