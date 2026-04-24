from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Weapon Data
weapons = {
    "fists": {
        "unlocked": True,
        "damage": 10, 
        "range": 2, 
        "texture": "fists_texture"
    },
    "pistol": {
        "unlocked": True,
        "damage": 20,
        "range": 50, 
        "texture": "pistol_texture"
    },
    "chaingun": {
        "unlocked": True,
        "damage": 20,
        "range": 150,
        "texture": "chaingun_texture"
    },
    "shotgun": {
        "unlocked": False,
        "damage": 100, #High damage, short range
        "range": 15,
        "texture": "shotgun_texture"
    },
    "chainsaw": {
        "unlocked": False,
        "damage": 15,
        "range": 3,
        "texture": "chainsaw_texture"
    },
    "plasma_rifle": {
        "unlocked": False,
        "damage": 50,
        "range": 100,
        "texture": "plasma_texture"
    },
    "goybeam": {
        "unlocked": False,
        "damage": 9999, # Insta-kill
        "range": 200,
        "texture": "vaporizer_texture"
    }
}

current_weapon = "fists"
shoot_cooldown = 0

# --- World Setup ---
# The Island
ground = Entity(
    model='plane', 
    collider='box', 
    scale=100,
    color=color.green, 
    texture='grass', 
    texture_scale=(10,10) 
)

# The Water (a bit lower than the ground)
water = Entity(
    model='plane',
    position=(0, -1, 0),
    scale=1000,
    color=color.blue,
    texture='water'
)

# Create some "2.5D" walls
# In a Doom-style game, walls are just flat planes positioned in 3D space
class TemplePillar(Entity):
    def __init__(self, pos):
      super().__init__(
          model='cube',
          collider='box',
          position=pos,
          scale=(1, 6, 1),
          color=color.light_gray,
          texture='white_cube'
      )

TemplePillar(pos=(5, 3, 5))
TemplePillar(pos=(-5, 3, 5))
TemplePillar(pos=(5, 3, -5))
TemplePillar(pos=(-5, 3, -5))

wall_back = Entity(
    model='cube', 
    collider='box', 
    position=(0, 3, 5), 
    scale=(10, 6, 0.2), 
    texture='brick', 
    color=color.dark_gray
)

wall_front = Entity(
    model='cube',
    collider='box',
    position=(0, 3, -5),
    scale=(10, 6, 0.2),
    texture='brick',
    color=color.dark_gray
    )

wall_left = Entity(
    model='cube',
    collider='box',
    position=(-5, 3, 0),
    scale=(0.2, 6, 10),
    texture='brick',
    color=color.dark_gray
    )

wall_right = Entity(
    model='cube',
    collider='box',
    position=(5, 3, 0),
    scale=(0.2, 6, 10),
    texture='brick',
    color=color.dark_gray
    )

dome = Entity(
    model='sphere',
    color=color.gold,
    position=(0, 6, 0),
    scale=12,
    texture='white_cube'
)

# --- Player Setup ---
player = FirstPersonController()
player.cursor.color = color.red  # Your crosshair

# --- Enemy/Sprite Setup ---
# This is a 3D sprite: a 2D quad that always faces you
enemy = Entity(
    model='quad',
    texture='vertical_gradient', # Replace with your enemy image later
    position=(5, 1, 10),
    scale=(1, 2),
    billboard=True,
    collider='box'
)

def input(key):
    if key == 'left mouse down':
        # Play a sound here later!
        print("Bang!")
        
        # Check if we hit the enemy
        if mouse.hovered_entity == enemy:
            print("Direct hit!")
            destroy(enemy)

def shoot():
    # Logic for checking hits
    hit_info = raycast(camera.world_position, camera.forward, distance=weapons[current_weapon]["range"])
    if hit_info.hit:
        # Check if the thing we hit is an enemy
        # destroy(hit_info.entity)
        pass

def update():
    global shoot_cooldown

    #Reduce the cooldown timer over time
    if shoot_cooldown > 0:
        shoot_cooldown -= time.dt

    # Check if the left mouse button is HELD DOWN
    if mouse.left and shoot_cooldown <= 0:
        if current_weapon == "chaingun":
            shoot()
            shoot_cooldown = 0.1 # This means if fires 10 times per second
        elif current_weapon == "plasma_rifle":
            shoot()
            shoot_cooldown = 0.2 # Slightly slower fire rate

app.run()