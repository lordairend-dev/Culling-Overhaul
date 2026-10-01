import bge
from collections import OrderedDict


class Component(bge.types.KX_PythonComponent):

    args = OrderedDict([
        ("reverse_physics", False),
        ("physics_radius", 10.0),
        ("reverse_logic", False),
        ("logic_radius", 10.0),
    ])

    def start(self, args):

 
        # Reverse Physics ----------------------------------

        self.reverse_physics = args["reverse_physics"]
        self.physics_radius = args["physics_radius"]

        self.reverse_physics_suspended = False
        self.native_physics_culling_was_enabled = False

        self.physics_radius_squared = (
            self.physics_radius * self.physics_radius
        )

        # Reverse Logic ------------------------------------

        self.reverse_logic = args["reverse_logic"]
        self.logic_radius = args["logic_radius"]

        self.reverse_logic_suspended = False
        self.native_logic_culling_was_enabled = False

        self.logic_radius_squared = (
            self.logic_radius * self.logic_radius
        )


    def update(self):

        # Nothing to do if both systems are disabled.
        if not self.reverse_physics and not self.reverse_logic:
            return

        scene = self.object.scene
        object_position = self.object.worldPosition

        minimum_distance_squared = float("inf")

        # Find closest activity-culling camera -------------

        for camera in scene.cameras:

            if not camera.activityCulling:
                continue

            camera_position = camera.worldPosition

            dx = object_position.x - camera_position.x
            dy = object_position.y - camera_position.y
            dz = object_position.z - camera_position.z

            distance_squared = (
                dx * dx +
                dy * dy +
                dz * dz
            )

            if distance_squared < minimum_distance_squared:
                minimum_distance_squared = distance_squared


        # No camera is using activity culling.
        if minimum_distance_squared == float("inf"):
            return


        if self.reverse_physics:

            if minimum_distance_squared < self.physics_radius_squared:

                if not self.reverse_physics_suspended:

                    self.native_physics_culling_was_enabled = (
                        self.object.physicsCulling
                    )

                    # Disable native culling while we control it.
                    self.object.physicsCulling = False

                    self.object.suspendPhysics()

                    self.reverse_physics_suspended = True

            else:

                if self.reverse_physics_suspended:

                    self.object.restorePhysics()

                    # Restore original native culling state.
                    self.object.physicsCulling = (
                        self.native_physics_culling_was_enabled
                    )

                    self.reverse_physics_suspended = False


        if self.reverse_logic:

            if minimum_distance_squared < self.logic_radius_squared:

                if not self.reverse_logic_suspended:

                    self.native_logic_culling_was_enabled = (
                        self.object.logicCulling
                    )

                    # Disable native culling while we control it.
                    self.object.logicCulling = False

                    self.object.suspendLogic()

                    self.reverse_logic_suspended = True

            else:

                if self.reverse_logic_suspended:

                    self.object.restoreLogic()

                    # Restore original native culling state.
                    self.object.logicCulling = (
                        self.native_logic_culling_was_enabled
                    )

                    self.reverse_logic_suspended = False