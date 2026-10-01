bl_info = {
    "name": "Culling Overhaul",
    "author": "Your Name",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "Object Properties",
    "description": "Adds reversed physics and logic activity culling.",
    "category": "Game Engine",
}

from . import culling


def register():
    culling.register()


def unregister():
    culling.unregister()


if __name__ == "__main__":
    register()