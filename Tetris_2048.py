################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################
import math

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)
import time
import sys

from tile import tile_colors


# The main function where this program starts execution
def start():
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas (the displayed window)
    canvas_h, canvas_w = 40 * grid_h, 50 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h - 20)
    # set the scale of the coordinate system for the drawing canvas
    stddraw.setXscale(-1, grid_w + 5)
    stddraw.setYscale(-1, grid_h)

    # set the game grid dimension values stored and used in the Tetromino class
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino()
    next_tetromino = create_tetromino()
    
    # Assign the current and next tetrominoes to the grid
    grid.current_tetromino = current_tetromino
    grid.set_next_tetromino(next_tetromino)

    grid.current_tetromino = current_tetromino
    GameGrid.score = grid.score
 
    print("Next tetromino type is: " + next_tetromino.type)


    # display a simple menu before opening the game
    # by using the display_game_menu function defined below
    display_game_menu(grid, grid_h, grid_w)
    
    paused = False  # Variable to track whether the game is paused or not

    while True:
        # Check for user interaction via the keyboard
        if stddraw.hasNextKeyTyped():  
            key_typed = stddraw.nextKeyTyped()  
            if key_typed == "p":
                paused = not paused  # Toggle paused state
            elif not paused:  # Process key inputs only if the game is not paused
                if key_typed == "left":
                    current_tetromino.move(key_typed, grid)
                elif key_typed == "right":
                    current_tetromino.move(key_typed, grid)
                elif key_typed == "down":
                    current_tetromino.move(key_typed, grid)
                elif key_typed == "up":
                    current_tetromino.rotate(grid)
                elif key_typed == "space":
                    while current_tetromino.move("down", grid):  # Move down until cannot move anymore
                        pass
                stddraw.clearKeysTyped()

        if not paused:
            success = current_tetromino.move("down", grid)

            if not success:
                tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
                game_over = grid.update_grid(tiles, pos)

                if game_over:
                    display_game_over_menu(grid, grid.score)
                    return  # Exit the game loop

                merge = check_merging(grid)
                while merge:
                    merge = check_merging(grid)

                delete_free_tiles(grid)
                clear_full_rows(grid)

                current_tetromino = next_tetromino
                next_tetromino = create_tetromino()
                grid.current_tetromino = current_tetromino
                grid.set_next_tetromino(next_tetromino)

            grid.display()

        # Add a small delay to avoid excessive CPU usage
        stddraw.show(50)
print("Game over")


# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
    # the type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'J', 'L', 'T', 'S']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)
    return tetromino


# A function for displaying a simple menu before starting the game
def display_game_menu(grid, grid_height, grid_width):
    # the colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # compute the path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # the coordinates to display the image centered horizontally
    img_center_x, img_center_y = (grid_width + 3.5 ) / 2, grid_height - 6
    # the image is modeled by using the Picture class
    image_to_display = Picture(img_file)
    # add the image to the drawing canvas
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # the dimensions for the start game button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # add the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # add the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    
    # Display tutorial prompt in a box
    box_width = 10
    box_height = 4
    box_x = 2.8
    box_y = 6.5

    # Draw box outline
    stddraw.setPenColor(Color(255, 255, 255))  # White pen color
    stddraw.rectangle(box_x, box_y, box_width, box_height)

    # Display tutorial text inside the box
    tutorial_text_size = 15
    tutorial_text_color = Color(255, 255, 255)  # White text color
    tutorial_text_y = 0.5  # y-coordinate for tutorial text
    
    tutorial_text_x = box_x + 5  # x-coordinate for tutorial text

    stddraw.setFontSize(tutorial_text_size)
    stddraw.setPenColor(tutorial_text_color)
    stddraw.text(tutorial_text_x, box_y + box_height - 0.3, "Tutorial:")  # Adjust y-coordinate
    stddraw.text(tutorial_text_x, box_y + box_height - 1.1, "- Use arrow keys to move the tetromino")  # Adjust y-coordinate
    stddraw.text(tutorial_text_x, box_y + box_height - 1.9, "- Press 'Up' arrow key to rotate")  # Adjust y-coordinate
    stddraw.text(tutorial_text_x, box_y + box_height - 2.7, "- Press 'Space' to drop the tetromino")  # Adjust y-coordinate
    stddraw.text(tutorial_text_x, box_y + box_height - 3.5, "- Press 'P' to pause the game")  # Adjust y-coordinate

    # Add buttons for easy, normal, and hard difficulty levels
    button_spacing = 1  # spacing between buttons
    button_text_size = 15  # text size for buttons
    button_text_color = Color(255, 255, 255)  # white text color
    button_text_y = button_blc_y + button_h / 2  # y-coordinate for button text

    # Calculate the total width of all buttons and the space between them
    total_button_width = 3 * button_w + 2 * button_spacing
    start_x = (total_button_width-35) / 2

    # Easy button
    easy_button_x = start_x+0.1
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(easy_button_x, button_blc_y - 4, button_w / 2, button_h)
    stddraw.setFontSize(button_text_size)
    stddraw.setPenColor(text_color)
    stddraw.text(easy_button_x + button_w / 4, button_text_y - 4, "Easy")

    # Normal button
    normal_button_x = start_x + 6
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(normal_button_x, button_blc_y - 4, button_w / 2, button_h)
    stddraw.setFontSize(button_text_size)
    stddraw.setPenColor(text_color)
    stddraw.text(normal_button_x + button_w / 4, button_text_y - 4, "Normal")

    # Hard button
    hard_button_x = start_x + button_w + button_spacing+0.4
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(hard_button_x, button_blc_y - 4, button_w / 2, button_h)
    stddraw.setFontSize(button_text_size)
    stddraw.setPenColor(text_color)
    stddraw.text(hard_button_x + button_w / 4, button_text_y - 4, "Hard")

    grid.speed = 200 #default value

    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the start game button
        if stddraw.mousePressed():

            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # Eğer tıklanan nokta "Easy" butonu içindeyse
            if easy_button_x <= mouse_x <= easy_button_x + button_w / 2 and \
                    button_blc_y - 4 <= mouse_y <= button_blc_y - 4 + button_h:

                # grid.speed'i değiştir
                grid.speed = 400 #450
                print(grid.speed)  # Örnek olarak 1000 olarak ayarladım, siz istediğiniz değeri verebilirsiniz
                pass

            elif normal_button_x <= mouse_x <= normal_button_x + button_w / 2 and \
                    button_blc_y - 4 <= mouse_y <= button_blc_y - 4 + button_h:
                # Normal butonun event handler'i buraya yazılabilir
                grid.speed = 200 #250
                print(grid.speed)  # Örnek olarak 1000 olarak ayarladım, siz istediğiniz değeri verebilirsiniz
                pass

            elif hard_button_x <= mouse_x <= hard_button_x + button_w / 2 and \
                    button_blc_y - 4 <= mouse_y <= button_blc_y - 4 + button_h:
                # Hard butonun event handler'i buraya yazılabilir
                grid.speed = 75 #125
                print(grid.speed)  # Örnek olarak 1000 olarak ayarladım, siz istediğiniz değeri verebilirsiniz
                pass

            # get the coordinates of the most recent location at which the mouse
            # has been left-clicked

            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game

def display_game_over_menu(grid,score):
    # Check if the grid contains a tile with the value 2048 or more
    win_condition = False
    for row in range(grid.grid_height):
        for col in range(grid.grid_width):
            if grid.tile_matrix[row][col] is not None and (grid.tile_matrix[row][col].number >= 2048):
                win_condition = True
                break

    # Clear the screen with the same background color as the menu
    background_color = Color(42, 69, 99)
    stddraw.clear(background_color)

    # Load and display the same image as the menu screen
    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + "/images/menu_image.png"
    img_center_x, img_center_y = (grid.grid_width + 3.5) / 2, grid.grid_height - 7
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)

    # Display appropriate message based on win condition
    if win_condition:
        stddraw.setFontSize(34)
        stddraw.setPenColor(Color(0, 255, 0))  # Green color for "You Win!"
        stddraw.text(8, 7, "You Win!")
    else:
        stddraw.setFontSize(34)
        stddraw.setPenColor(Color(188, 173, 165))
        stddraw.text(8, 7, "Game Over!")

    # Display player's score
    stddraw.setFontSize(24)
    stddraw.text(8, 6, "Your Score: " + str(score))

    # Display options
    stddraw.setFontSize(22)
    stddraw.text(8, 3, "Press 'R' to Restart")
    stddraw.text(8, 2, "Press 'Q' to Quit")

    while True:
        # Check if any key is typed
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == "escape":
                break  # Exit the game if Esc is pressed
            elif key == "r":
                print("pressed R")
                restart()
                break
            elif key == "q":
                print("pressed Q")
                exit()
                break

        # Add a small delay to avoid excessive CPU usage
        stddraw.show(50)

def check_merging(grid):
    merged = False
    for a in range(1, 19):
        for b in range(12):
            if grid.tile_matrix[a][b] is not None and grid.tile_matrix[a - 1][b] is not None and grid.tile_matrix[a][b].number == grid.tile_matrix[a - 1][b].number:
                merged_number = grid.tile_matrix[a][b].number + grid.tile_matrix[a - 1][b].number
                merged_value = grid.tile_matrix[a][b].number * 2  # Calculate the merged value
                grid.tile_matrix[a - 1][b].number = merged_value
                grid.score += grid.tile_matrix[a][b].number * 2  # Calculate the merged value

                # If the merged number is greater than 4096, use the color for 4096
                if merged_number >= 4096:
                    tile_color_index = int(math.log(4096, 2)) - 1
                else:
                    tile_color_index = int(math.log(merged_number, 2)) - 1

                grid.tile_matrix[a - 1][b].background_color = tile_colors[tile_color_index]

                # grid.score += grid.tile_matrix[a][b].number
                row = a
                while row < 18:
                    grid.tile_matrix[row][b] = grid.tile_matrix[row + 1][b]
                    if grid.tile_matrix[row + 1][b] is not None:
                        grid.tile_matrix[row + 1][b].set_position((row, b))
                    row += 1
                grid.tile_matrix[18][b] = None
                merged = True


                grid.display()

                return merged
    return merged


# Function to detect and return a list of coordinates of free tiles in the grid
def detect_free_tiles(grid):
    free_tiles = []
    visited = [[False for _ in range(grid.grid_width)] for _ in range(grid.grid_height)]

    # Mark tiles of the current tetromino as connected
    if grid.current_tetromino is not None:
        for tile in grid.current_tetromino.tiles:
            row, col = tile.position.y, tile.position.x
            visited[row][col] = True

    # Mark tiles connected to the bottom as visited
    for col in range(grid.grid_width):
        if grid.tile_matrix[0][col] is not None:
            is_connected_to_bottom(grid, 0, col, visited)

    # Iterate over grid to detect free tiles
    for row in range(grid.grid_height):
        for col in range(grid.grid_width):
            if grid.tile_matrix[row][col] is not None and not visited[row][col]:
                free_tiles.append((row, col))

    return free_tiles


# Helper function to check if there is a path to the bottom
def is_connected_to_bottom(grid, row, col, visited):
    # Create a stack for DFS
    stack = [(row, col)]

    while stack:
        row, col = stack.pop()
        if not visited[row][col]:
            visited[row][col] = True

            # Check all four directions (up, down, left, right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < grid.grid_height and 0 <= new_col < grid.grid_width and
                        grid.tile_matrix[new_row][new_col] is not None and not visited[new_row][new_col]):
                    stack.append((new_row, new_col))


# Function to delete free tiles from the grid
def delete_free_tiles(grid):
    free_tiles = detect_free_tiles(grid)
    for row, col in free_tiles:
        if grid.tile_matrix[row][col] is not None:
            grid.score += grid.tile_matrix[row][col].number  # Add the tile value to the total before deleting the tile
            grid.tile_matrix[row][col] = None


    grid.display()

def clear_full_rows(grid):
    # Create an empty row to be reused
    empty_row = [None] * grid.grid_width
    rows_to_clear = []

    # Identify full rows
    for i in range(grid.grid_height):
        is_full = True
        for j in range(grid.grid_width):
            if grid.tile_matrix[i][j] is None:
                is_full = False
                break
        if is_full:
            rows_to_clear.append(i)

    # Clear and shift rows
    if rows_to_clear:
        num_rows_cleared = len(rows_to_clear)
        for row in reversed(rows_to_clear):
            row_sum = 0  # To store the sum of tile values in the cleared row
            for j in range(grid.grid_width):
                if grid.tile_matrix[row][j] is not None:
                    grid.score += grid.tile_matrix[row][j].number


            # Shift all rows above the cleared row down
            for next_row in range(row, grid.grid_height - num_rows_cleared):
                for col in range(grid.grid_width):
                    grid.tile_matrix[next_row][col] = grid.tile_matrix[next_row + 1][col]

            # Set the topmost row to the empty row
            for col in range(grid.grid_width):
                grid.tile_matrix[grid.grid_height - num_rows_cleared][col] = None

            num_rows_cleared -= 1

def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)
    stdDraw.setVisible(True)


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
