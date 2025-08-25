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
window.fps_counter.enabled = False
window.exit_button.visible = False
window.fullscreen = True

# --- Voxel (Block) Class ---
# This class defines the behavior of each block in the world.
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), block_color=color.green, is_ground=False):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            color=block_color,
            highlight_color=block_color.tint(.2),
            scale=1,
            # DEFINITIVE FIX: Every single block now has a solid collider. This is the most reliable method.
            collider='box'
        )
        # This flag is used to make the initial ground indestructible.
        self.is_ground = is_ground

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                # You can only destroy blocks that are not part of the ground.
                if not self.is_ground:
                    destroy(self)

            if key == 'right mouse down':
                # Prevent placing a block inside the player.
                new_block_position = self.position + mouse.normal
                if distance(new_block_position, player.position) > 1.5:
                    # Place a new block. It will be solid and NOT a ground block by default.
                    Voxel(position=new_block_position, block_color=block_colors[block_pick])

# --- World Generation ---
world_size = 32
for z in range(world_size):
    for x in range(world_size):
        # Create the ground blocks. They are solid and marked as indestructible.
        Voxel(position=(x, 0, z), block_color=color.green, is_ground=True)


# --- UI Toolbar ---
# This section creates the clickable toolbar at the bottom of the screen.
toolbar = Entity(parent=camera.ui, position=(0, -0.45))
toolbar_slots = []

# This function will be called when a toolbar slot is clicked or a number key is pressed.
def set_block_pick(index):
    global block_pick
    block_pick = index
    # Move the selection cursor to the clicked slot.
    selection_cursor.x = toolbar_slots[index].x

for i, bc in enumerate(block_colors):
    slot = Button(
        parent=toolbar,
        model='quad',
        color=bc,
        scale=0.07,
        # Position each slot horizontally.
        x=(-(len(block_colors)/2) + i) * 0.08,
        # When clicked, call the set_block_pick function with its index.
        on_click=Func(set_block_pick, i)
    )
    toolbar_slots.append(slot)

# --- NEW: Rainbow Selection Cursor ---
# A highlight to show the selected block.
selection_cursor = Entity(
    parent=toolbar,
    model='quad',
    scale=0.08,
    # Using the built-in rainbow texture for the border.
    texture='rainbow',
    z=-1
)
# Initialize the cursor position to the starting block.
selection_cursor.x = toolbar_slots[block_pick].x


# --- Input Handling and Game Logic ---
def update():
    # Keep player within world boundaries.
    if player.x < 0: player.x = 0
    if player.x > world_size -1: player.x = world_size -1
    if player.z < 0: player.z = 0
    if player.z > world_size -1: player.z = world_size -1

# This function is called by Ursina once for every key press.
def input(key):
    global block_pick
    # Mouse Wheel Block Selection
    if key == 'scroll up':
        block_pick = (block_pick + 1) % len(block_colors)
        set_block_pick(block_pick)
    if key == 'scroll down':
        block_pick = (block_pick - 1) % len(block_colors)
        set_block_pick(block_pick)

    # Handle block selection with number keys 1 through 8.
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
# Center the player in the middle of the world, above the ground.
player.set_position((world_size / 2, 5, world_size / 2))

sky = Sky()

# Start the game
app.run()
