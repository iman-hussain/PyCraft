# First, you need to install the ursina engine.
# Open your terminal or command prompt and run: pip install ursina

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json # Import the json library for saving and loading

# Create the main application window
app = Ursina(title='PyCraft')

# --- Game Window Configuration ---
window.size = (1280, 720)
window.fullscreen = False
window.fps_counter.enabled = False
window.exit_button.visible = False

# --- Block Color Definitions ---
block_colors = [
    color.black, color.white, color.blue, color.green,
    color.red, color.yellow, color.rgb(128, 0, 128), color.orange
]

# --- Game State ---
block_pick = 3

# --- Voxel (Block) Class ---
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), block_color=color.green, is_ground=False, add_collider=True):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            color=block_color,
            highlight_color=block_color.tint(.2),
            scale=1
        )
        self.is_ground = is_ground
        if add_collider:
            self.collider = 'box'

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if not self.is_ground and self.y > 0:
                    destroy(self)
            if key == 'right mouse down':
                new_block_position = self.position + mouse.normal
                if distance(new_block_position, player.position) > 1.5:
                    Voxel(position=new_block_position, block_color=block_colors[block_pick])

# --- World Generation & Management ---
world_size = 32

def clear_canvas():
    """ Destroys all player-placed blocks. """
    # Use a list comprehension to avoid modifying the list while iterating
    blocks_to_destroy = [e for e in scene.children if isinstance(e, Voxel) and not e.is_ground]
    for block in blocks_to_destroy:
        destroy(block)

def save_canvas():
    """ Saves the position and color of all player-placed blocks to a file. """
    saved_blocks = []
    for entity in scene.children:
        if isinstance(entity, Voxel) and not entity.is_ground:
            pos = [entity.x, entity.y, entity.z]
            col = [entity.color.r, entity.color.g, entity.color.b, entity.color.a]
            saved_blocks.append({'position': pos, 'color': col})
    
    with open('pycraft_save.json', 'w') as f:
        json.dump(saved_blocks, f, indent=4)
    
    print("Canvas Saved!")
    confirm_text.text = "Canvas Saved!"
    confirm_text.fade_in(duration=0.1)
    confirm_text.fade_out(duration=1, delay=1)


def load_canvas():
    """ Loads block data from a file and reconstructs the world. """
    clear_canvas()
    try:
        with open('pycraft_save.json', 'r') as f:
            loaded_blocks = json.load(f)
        
        for block_data in loaded_blocks:
            pos = tuple(block_data['position'])
            # Convert color from 0-1 float to 0-255 int for rgba function
            col = color.rgba(*[int(c*255) for c in block_data['color']])
            Voxel(position=pos, block_color=col)
        print("Canvas Loaded!")
    except FileNotFoundError:
        print("No save file found.")
    
    start_game()

def start_new_canvas():
    """ Clears any existing blocks and starts a fresh game. """
    clear_canvas()
    start_game()

# --- Game State Transitions ---
def start_game():
    """ Enables all in-game elements and disables menus. """
    title_screen.disable()
    pause_menu.disable()
    player.enable()
    toolbar.enable()
    mouse.locked = True
    application.paused = False

def show_pause_menu():
    pause_menu.enable()
    player.disable()
    mouse.locked = False
    application.paused = True

def hide_pause_menu():
    pause_menu.disable()
    player.enable()
    mouse.locked = True
    application.paused = False

# --- UI Elements ---
# Title Screen
title_screen = Entity(parent=camera.ui, enabled=True)
Text(parent=title_screen, text="PyCraft", scale=5, origin=(0,0), y=0.2)
Button(parent=title_screen, text="New Canvas", color=color.azure, scale=(0.3, 0.1), y=0, on_click=start_new_canvas)
Button(parent=title_screen, text="Load Canvas", color=color.azure, scale=(0.3, 0.1), y=-0.15, on_click=load_canvas)

# Pause Menu
pause_menu = Entity(parent=camera.ui, enabled=False)
Text(parent=pause_menu, text="Paused", scale=3, origin=(0,0), y=0.25)
Button(parent=pause_menu, text="Return", color=color.azure, scale=(0.3, 0.1), y=0.1, on_click=hide_pause_menu)
Button(parent=pause_menu, text="Save Canvas", color=color.azure, scale=(0.3, 0.1), y=0, on_click=save_canvas)
Button(parent=pause_menu, text="Load Canvas", color=color.azure, scale=(0.3, 0.1), y=-0.1, on_click=load_canvas)
Button(parent=pause_menu, text="New Canvas", color=color.azure, scale=(0.3, 0.1), y=-0.2, on_click=start_new_canvas)

# In-Game Toolbar
toolbar = Entity(parent=camera.ui, position=(0, -0.45), enabled=False)
toolbar_slots = []
selection_cursor = Entity(parent=toolbar, model='quad', scale=0.08, texture='rainbow', z=1)

def set_block_pick(index):
    global block_pick
    block_pick = index
    selection_cursor.x = toolbar_slots[index].x

for i, bc in enumerate(block_colors):
    slot = Button(parent=toolbar, model='quad', color=bc, scale=0.07, x=(-(len(block_colors)/2) + i) * 0.08, on_click=Func(set_block_pick, i))
    toolbar_slots.append(slot)
selection_cursor.x = toolbar_slots[block_pick].x

# Save confirmation text
confirm_text = Text(parent=camera.ui, text="", origin=(0,0), y=0.3, color=color.lime)
confirm_text.disable()


# --- Initial World Setup (Done once at the start) ---
# Visual Ground
for z in range(world_size):
    for x in range(world_size):
        Voxel(position=(x, 0, z), block_color=color.green, add_collider=False, is_ground=True)
# Solid Ground Collider
ground_collider = Entity(model='cube', scale=(world_size, 1, world_size), position=(world_size/2 - 0.5, -0.5, world_size/2 - 0.5), collider='box', visible=False)

# Player
player = FirstPersonController(jump_height=1.5, speed=6, gravity=0.5)
player.cursor.visible = False
player.set_position((world_size / 2, 5, world_size / 2))
player.disable() # Start with player disabled

# Sky
sky = Sky()

# --- Input Handling ---
def input(key):
    global block_pick
    if key == 'escape':
        if not title_screen.enabled:
            if pause_menu.enabled:
                hide_pause_menu()
            else:
                show_pause_menu()

    if not application.paused:
        if key == 'scroll up':
            block_pick = (block_pick + 1) % len(block_colors)
            set_block_pick(block_pick)
        if key == 'scroll down':
            block_pick = (block_pick - 1) % len(block_colors)
            set_block_pick(block_pick)
        if key in '12345678':
            set_block_pick(int(key)-1)

# Start the game
app.run()
