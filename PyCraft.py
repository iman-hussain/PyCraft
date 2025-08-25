# First, you need to install the ursina engine.
# Open your terminal or command prompt and run: pip install ursina

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Create the main application window
app = Ursina()

# --- Block Color Definitions ---
# Using a list makes it easy to manage colors and the toolbar.
block_colors = [
    color.black,
    color.white,
    color.blue,
    color.green,
    color.red,
    color.yellow,
    color.rgb(128, 0, 128), # Purple
    color.orange
]

# --- Game State ---
# This variable will hold the index of the currently selected color.
block_pick = 3  # Start with green selected

# --- Game Window Configuration ---
# --- FIX: Set resolution to 1280x720 and disable fullscreen ---
window.size = (1280, 720)
window.fullscreen = False
window.fps_counter.enabled = False
window.exit_button.visible = False


# --- Voxel (Block) Class ---
# This class defines the behavior of each block in the world.
class Voxel(Button):
    # The 'add_collider' parameter distinguishes between solid and visual-only blocks.
    def __init__(self, position=(0, 0, 0), block_color=color.green, add_collider=True):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            color=block_color,
            highlight_color=block_color.tint(.2),
            scale=1
        )
        # Only add a collider if it's a player-placed block. This is a key optimization.
        if add_collider:
            self.collider = 'box'

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                # You can only destroy blocks that are above the ground plane (y > 0).
                if self.position.y > 0:
                    destroy(self)

            if key == 'right mouse down':
                # Prevent placing a block inside the player.
                new_block_position = self.position + mouse.normal
                if distance(new_block_position, player.position) > 1.5:
                    # Place a new block that IS solid.
                    Voxel(position=new_block_position, block_color=block_colors[block_pick], add_collider=True)

# --- World Generation ---
world_size = 32
for z in range(world_size):
    for x in range(world_size):
        # Create the VISUAL ground blocks. These have no collider to ensure performance and stability.
        Voxel(position=(x, 0, z), block_color=color.green, add_collider=False)

# --- DEFINITIVE FIX: Solid Ground Collider ---
# This is a single, large, invisible but SOLID CUBE that the player stands on.
# This is the most reliable way to prevent falling through the world.
ground_collider = Entity(
    model='cube',
    scale=(world_size, 1, world_size),
    # Position it to sit perfectly under the visual ground blocks.
    position=(world_size/2 - 0.5, -0.5, world_size/2 - 0.5),
    collider='box',
    # Make it invisible.
    visible=False
)

# --- UI Toolbar ---
toolbar = Entity(parent=camera.ui, position=(0, -0.45))
toolbar_slots = []

def set_block_pick(index):
    global block_pick
    block_pick = index
    selection_cursor.x = toolbar_slots[index].x

for i, bc in enumerate(block_colors):
    slot = Button(
        parent=toolbar,
        model='quad',
        color=bc,
        scale=0.07,
        x=(-(len(block_colors)/2) + i) * 0.08,
        on_click=Func(set_block_pick, i)
    )
    toolbar_slots.append(slot)

# --- Rainbow Selection Border ---
selection_cursor = Entity(
    parent=toolbar,
    model='quad',
    scale=0.08,
    texture='rainbow',
    z=1
)
selection_cursor.x = toolbar_slots[block_pick].x


# --- Input Handling and Game Logic ---
def update():
    # Keep player within world boundaries.
    if player.x < 0: player.x = 0
    if player.x > world_size -1: player.x = world_size -1
    if player.z < 0: player.z = 0
    if player.z > world_size -1: player.z = world_size -1

def input(key):
    global block_pick
    if key == 'scroll up':
        block_pick = (block_pick + 1) % len(block_colors)
        set_block_pick(block_pick)
    if key == 'scroll down':
        block_pick = (block_pick - 1) % len(block_colors)
        set_block_pick(block_pick)

    if key == '1': set_block_pick(0)
    if key == '2': set_block_pick(1)
    if key == '3': set_block_pick(2)
    if key == '4': set_block_pick(3)
    if key == '5': set_block_pick(4)
    if key == '6': set_block_pick(5)
    if key == '7': set_block_pick(6)
    if key == '8': set_block_pick(7)


# --- Instantiate Player and Sky ---
player = FirstPersonController(jump_height=1.5, speed=6)
player.gravity = 0.5
player.cursor.visible = False
player.set_position((world_size / 2, 5, world_size / 2))

# --- DEFINITIVE FIX: Safe Spawn Platform ---
# Create a small, solid platform directly under the spawn point as a final guarantee.
spawn_center = player.position.xz
Voxel(position=(spawn_center.x, 1, spawn_center.y), block_color=color.gold, add_collider=True)
Voxel(position=(spawn_center.x+1, 1, spawn_center.y), block_color=color.gold, add_collider=True)
Voxel(position=(spawn_center.x, 1, spawn_center.y+1), block_color=color.gold, add_collider=True)
Voxel(position=(spawn_center.x+1, 1, spawn_center.y+1), block_color=color.gold, add_collider=True)

sky = Sky()

# Start the game
app.run()
