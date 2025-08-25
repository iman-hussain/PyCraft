# First, you need to install the ursina engine.
# Open your terminal or command prompt and run: pip install ursina

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Create the main application window
app = Ursina()

# --- Block Color Definitions ---
# Expanded list of colors as requested.
block_colors = [
    color.black,
    color.white,
    color.blue,
    color.green,
    color.red,
    color.yellow,
    color.purple,
    color.orange
]

# --- Game State ---
block_pick = 3  # Start with green selected (index 3)

# --- Game Window Configuration ---
window.fps_counter.enabled = False
window.exit_button.visible = False
window.fullscreen = True

# --- Voxel (Block) Class ---
# This class defines the behavior of each block in the world.
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), block_color=color.green):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            color=block_color,
            highlight_color=block_color.tint(.2),
            scale=1
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                # Don't destroy the ground plane
                if self.position.y > 0:
                    destroy(self)

            if key == 'right mouse down':
                # Place a new block using the selected color from the list
                Voxel(position=self.position + mouse.normal, block_color=block_colors[block_pick])

# --- Ground Plane ---
# A single entity for the ground is much more performant than many individual blocks.
ground = Entity(
    model='plane',
    scale=(64, 1, 64),
    color=color.rgb(34, 139, 34),
    texture='white_cube',
    texture_scale=(64, 64),
    collider='box'
)

# --- UI Toolbar ---
# A wider toolbar to accommodate 8 blocks.
toolbar = Entity(parent=camera.ui, model='quad', scale=(0.8, 0.08), position=(0, -0.45), color=color.dark_gray)
toolbar_slots = []
for i, bc in enumerate(block_colors):
    slot = Button(
        parent=toolbar,
        model='quad',
        color=bc,
        scale=0.1,
        # Position each slot next to the previous one
        x=-0.44 + (i * 0.11)
    )
    toolbar_slots.append(slot)

# A highlight to show the selected block
selection_cursor = Entity(parent=toolbar, model='quad', scale=(0.11, 0.9), color=color.white, z=-1)


# --- Input Handling and Game Logic ---
def update():
    global block_pick

    # Handle block selection with number keys 1 through 8
    if held_keys['1']: block_pick = 0
    if held_keys['2']: block_pick = 1
    if held_keys['3']: block_pick = 2
    if held_keys['4']: block_pick = 3
    if held_keys['5']: block_pick = 4
    if held_keys['6']: block_pick = 5
    if held_keys['7']: block_pick = 6
    if held_keys['8']: block_pick = 7

    # Move the selection cursor to the currently selected slot
    selection_cursor.x = toolbar_slots[block_pick].x


# --- Instantiate Player and Sky ---
player = FirstPersonController(jump_height=1.5, speed=6)
player.gravity = 0.5
player.cursor.visible = False
# Start the player above the ground plane
player.set_position((0, 5, 0))

sky = Sky()

# Start the game
app.run()
