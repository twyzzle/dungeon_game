import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import Button, HBox, VBox, Layout, Output
from IPython.display import display, clear_output


class Player:
    def __init__(self, size, grid_size):
        self.size = size
        self.position = [grid_size // 2, grid_size // 2]
        self.grid_size = grid_size
        self.holding = None
        self.state = 'PLAYING'

    def move(self, dx, dy):
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        if (0 <= new_x < self.grid_size-self.size+1) and (0 <= new_y < self.grid_size-self.size+1):
            self.position[0] = new_x
            self.position[1] = new_y
            return True
        return False

class Scenery:
    def __init__(self, start_x, y):
        self.start_x = start_x
        self.x = start_x
        self.y = y

    def move(self, dx):
        self.x -= dx

class Game:
    def __init__(self):
        self.grid_size = 1000
        self.player = Player(125, self.grid_size)
        self.clouds = [Scenery(400, 900), Scenery(800, 850)]
        self.trees = [Scenery(i, 667) for i in range(200, 1000, 200)]
        self.output = Output()

    def draw_cloud(self, ax, cloud):
        offsets = [(0, 0), (30, 30), (-30, 30), (60, 0), (-60, 0)]
        for dx, dy in offsets:
            ax.add_patch(plt.Circle((cloud.x+dx, cloud.y+dy), 50, color='white'))

    def killed_by_signpost(self):
        """Display a message saying the player was killed by a signpost."""
        clear_output(wait=True)  # Clear previous output
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_facecolor('black')
        ax.text(0.5, 0.5, "You were killed by a signpost", color='red', fontsize=12,
                ha='center', va='center', weight='bold')
        ax.axis('off')
        plt.show()
        display(btns, game.output)  # Ensure buttons and output are redisplayed after showing message


    def create_dungeon_background(self):
        fig, ax = plt.subplots(figsize=(6,6))

        # Set a dark color for the dungeon
        ax.set_facecolor('black')

        # Draw some "walls" using gray color
        ax.axhline(y=1, color='gray', linewidth=6)
        ax.axhline(y=5, color='gray', linewidth=6)
        ax.axvline(x=1, color='gray', linewidth=6)
        ax.axvline(x=5, color='gray', linewidth=6)

        # Add some random points as "rocks" or "obstacles"
        rock_x = np.random.rand(10) * 6
        rock_y = np.random.rand(10) * 6
        ax.scatter(rock_x, rock_y, c='gray', s=100)

        # Remove axis labels and ticks
        ax.axis('off')

        # Display the dungeon background
        plt.tight_layout()
        plt.show()

    def draw_tree(self, ax, tree):
        ax.add_patch(plt.Rectangle((tree.x-25, tree.y-50), 50, 100, color='sienna'))
        ax.add_patch(plt.Circle((tree.x, tree.y + 50), 75, color='forestgreen'))
        ax.add_patch(plt.Circle((tree.x - 60, tree.y), 50, color='forestgreen'))
        ax.add_patch(plt.Circle((tree.x + 60, tree.y), 50, color='forestgreen'))

    def draw_mario(self, ax, pos):
        x, y = pos
        ax.add_patch(plt.Rectangle((x+50, y+100), 50, 50, color='red'))
        ax.add_patch(plt.Rectangle((x+25, y+50), 100, 50, color='peachpuff'))
        ax.add_patch(plt.Circle((x+45, y+75), 10, color='white'))
        ax.add_patch(plt.Circle((x+105, y+75), 10, color='white'))
        ax.add_patch(plt.Circle((x+45, y+75), 5, color='black'))
        ax.add_patch(plt.Circle((x+105, y+75), 5, color='black'))
        ax.add_patch(plt.Rectangle((x+45, y+55), 60, 10, color='black'))
        ax.add_patch(plt.Rectangle((x+25, y), 100, 50, color='red'))
        if game.player.holding == 'shank':
          # Adjusting the arm's starting position to come from the upper-right corner of his torso
          ax.add_patch(plt.Rectangle((x+50, y+30), 60, 15, color='red'))

          # Adjusting the hand's position
          ax.add_patch(plt.Circle((x+140, y+37), 12, color='peachpuff'))

          # Adjusting the blade of the cleaver's position
          blade_points = [(x+142, y+25), (x+192, y+25), (x+182, y+45), (x+132, y+45)]
          blade = plt.Polygon(blade_points, closed=True, color='silver')
          ax.add_patch(blade)

          # Adjusting the handle of the cleaver's position
          handle_points = [(x+132, y+35), (x+142, y+35), (x+142, y+55), (x+132, y+55)]
          handle = plt.Polygon(handle_points, closed=True, color='saddlebrown')
          ax.add_patch(handle)

        if game.player.holding == 'wand':
            # Drawing Mario's hand
          ax.add_patch(plt.Circle((x+125, y+50), 10, color='peachpuff'))

          # Calculate angled wand start and end positions
          length = 60  # Length of the wand
          angle = np.deg2rad(45)  # 45-degree angle
          x_end = x + 125 + length * np.cos(angle)
          y_end = y + 50 + length * np.sin(angle)

          # Drawing the wand's handle
          ax.plot([x+125, x_end], [y+50, y_end], color='black', linewidth=3)  # Reduced linewidth

          # Drawing the wand's tip
          ax.add_patch(plt.Circle((x_end, y_end), 5, color='white'))

    def draw_signpost(self, ax):
        self.sign_rect_x = self.grid_size-200
        self.sign_rect_y = 400
        self.sign_rect_width = 150
        self.sign_rect_height = 20  # Adjusted to represent the post
        ax.add_patch(plt.Rectangle((self.sign_rect_x, self.sign_rect_y),
                                  self.sign_rect_width, self.sign_rect_height, facecolor='sienna'))  # Changed to 'sienna' for wood color
        # Drawing the signboard now
        ax.add_patch(plt.Rectangle((self.sign_rect_x + 25, self.sign_rect_y + 20),
                                  self.sign_rect_width - 50, 100, facecolor='burlywood', edgecolor='sienna'))

        # Adding squiggly lines to represent text
        y_positions = [self.sign_rect_y + 40, self.sign_rect_y + 60, self.sign_rect_y + 80]
        for y in y_positions:
            x_vals = np.linspace(self.sign_rect_x + 35, self.sign_rect_x + self.sign_rect_width - 35, 300)
            y_vals = y + 5 * np.sin(10 * np.pi * x_vals / self.sign_rect_width)
            ax.plot(x_vals, y_vals, color='black', linewidth=2)

    def draw(self):
        clear_output(wait=True)
        fig, ax = plt.subplots(figsize=(5,5))

        ax.add_patch(plt.Rectangle((0, 2*self.grid_size/3), self.grid_size, self.grid_size/3, color='blue'))
        ax.add_patch(plt.Rectangle((0, self.grid_size/3), self.grid_size, self.grid_size/3, color='peru'))
        ax.add_patch(plt.Rectangle((0, 0), self.grid_size, self.grid_size/3, color='yellow'))
        ax.add_patch(plt.Circle((150, 900), 70, color='yellow'))

        for cloud in self.clouds:
            self.draw_cloud(ax, cloud)

        for tree in self.trees:
            self.draw_tree(ax, tree)

        self.draw_signpost(ax)
        self.draw_mario(ax, (self.player.position[0], self.grid_size - self.player.position[1] - self.player.size))

        ax.set_xlim(0, self.grid_size)
        ax.set_ylim(0, self.grid_size)
        ax.set_aspect('equal')
        plt.axis('off')
        plt.tight_layout()

        def on_press(event):
            if (self.sign_rect_x <= event.xdata <= self.sign_rect_x + self.sign_rect_width and
                self.sign_rect_y <= event.ydata <= self.sign_rect_y + self.sign_rect_height):
                self.interact(None)  # Call the interact method if the sign has been clicked

        fig.canvas.mpl_connect('button_press_event', on_press)

        plt.show()
        display(btns, game.output)


    def move_scenery(self, dx):
        for cloud in self.clouds:
            cloud.move(dx)

        for tree in self.trees:
            tree.move(dx)

    def sign_clicked(self, btn):
        self.killed_by_signpost()


    def can_interact(self):
        distance_x = abs(self.sign_rect_x - self.player.position[0])
        distance_y = abs((self.grid_size - self.player.position[1]) - self.sign_rect_y)

        return distance_x <= 125 and distance_y <= 125


    def interact(self, btn):
            print("Interact method called")
            if self.can_interact():
                self.killed_by_signpost()
            else:
                raise ValueError("You are too far away to interact.")


game = Game()

def move(direction):
    moved = False
    if direction == 'Up':
        moved = game.player.move(0, 25)
    elif direction == 'Down':
        moved = game.player.move(0, -25)
    elif direction == 'Left':
        moved = game.player.move(-25, 0)
    elif direction == 'Right':
        moved = game.player.move(25, 0)

    if moved and direction == 'Right':
        game.move_scenery(25)

    game.draw()

btn_up = Button(description='↑', layout=Layout(width='60px', height='60px'))
btn_down = Button(description='↓', layout=Layout(width='60px', height='60px'))
btn_left = Button(description='←', layout=Layout(width='60px', height='60px'))
btn_right = Button(description='→', layout=Layout(width='60px', height='60px'))
btn_interact = Button(description='Interact', layout=Layout(width='180px', height='60px'))
# add functionality to the Shank and Wand buttons by using the on_click method later on.
# For example:
# btn_shank.on_click(shank_function)
# btn_wand.on_click(wand_function)
btn_shank = Button(description='Shank', layout=Layout(width='60px', height='60px'))
btn_wand = Button(description='Wand', layout=Layout(width='60px', height='60px'))
#
top_row = HBox([btn_shank, btn_up, btn_wand])
middle_row = HBox([btn_left, btn_down, btn_right])

def shank_function(btn):
    if game.player.holding == 'shank':
        game.player.holding = None
    else:
        game.player.holding = 'shank'
    game.draw()

def wand_function(btn):
    if game.player.holding == 'wand':
        game.player.holding = None
    else:
        game.player.holding = 'wand'
    game.draw()


btn_shank.on_click(shank_function)
btn_wand.on_click(wand_function)

btn_up.on_click(lambda x: move('Up'))
btn_down.on_click(lambda x: move('Down'))
btn_left.on_click(lambda x: move('Left'))
btn_right.on_click(lambda x: move('Right'))
btn_interact.on_click(game.interact)

top_row = HBox([btn_shank, btn_up, btn_wand])
middle_row = HBox([btn_left, btn_down, btn_right])

btns = VBox([top_row, middle_row, btn_interact])
display(btns)
game.draw()
