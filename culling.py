import bpy


_MSG_OWNER = object()

_RUNTIME_MODULE = "Culling Overhaul.runtime"
_RUNTIME_COMPONENT = "Culling Overhaul.runtime.Component"


def find_runtime_component(obj):
    if obj is None:
        return None

    try:
        for component in obj.game.components:
            if component.module == _RUNTIME_MODULE:
                return component
    except (AttributeError, ReferenceError):
        return None

    return None


def ensure_runtime_component(obj):
    if obj is None:
        return None

    component = find_runtime_component(obj)

    if component is not None:
        return component

    try:
        bpy.context.view_layer.objects.active = obj

        for selected in bpy.context.selected_objects:
            selected.select_set(False)

        obj.select_set(True)

        bpy.ops.logic.python_component_register(
            component_name=_RUNTIME_COMPONENT
        )

    except (AttributeError, RuntimeError):
        return None

    return find_runtime_component(obj)


def sync_runtime_component(obj):
    if obj is None:
        return

    component = ensure_runtime_component(obj)

    if component is None:
        return

    reverse = obj.reverse_culling

    try:
        for prop in component.properties:
            if prop.name == "reverse_physics":
                prop.value = reverse.physics_enabled

            elif prop.name == "physics_radius":
                prop.value = reverse.physics_radius

            elif prop.name == "reverse_logic":
                prop.value = reverse.logic_enabled

            elif prop.name == "logic_radius":
                prop.value = reverse.logic_radius

    except (AttributeError, ReferenceError, TypeError, ValueError):
        return


def clamp_reverse_physics(obj):
    activity = obj.game.activity_culling
    reverse = obj.reverse_culling

    if activity.use_physics and reverse.physics_enabled:
        if reverse.physics_radius > activity.physics_radius:
            reverse.physics_radius = activity.physics_radius


def clamp_native_physics(obj):
    activity = obj.game.activity_culling
    reverse = obj.reverse_culling

    if activity.use_physics and reverse.physics_enabled:
        if activity.physics_radius < reverse.physics_radius:
            activity.physics_radius = reverse.physics_radius


def clamp_reverse_logic(obj):
    activity = obj.game.activity_culling
    reverse = obj.reverse_culling

    if activity.use_logic and reverse.logic_enabled:
        if reverse.logic_radius > activity.logic_radius:
            reverse.logic_radius = activity.logic_radius


def clamp_native_logic(obj):
    activity = obj.game.activity_culling
    reverse = obj.reverse_culling

    if activity.use_logic and reverse.logic_enabled:
        if reverse.logic_radius > activity.logic_radius:
            activity.logic_radius = reverse.logic_radius


def update_physics_enabled(self, context):
    obj = context.object

    if obj is None:
        return

    clamp_reverse_physics(obj)
    sync_runtime_component(obj)


def update_physics_radius(self, context):
    obj = context.object

    if obj is None:
        return

    clamp_reverse_physics(obj)
    sync_runtime_component(obj)


def update_logic_enabled(self, context):
    obj = context.object

    if obj is None:
        return

    clamp_reverse_logic(obj)
    sync_runtime_component(obj)


def update_logic_radius(self, context):
    obj = context.object

    if obj is None:
        return

    clamp_reverse_logic(obj)
    sync_runtime_component(obj)


def native_culling_changed(obj_ref, property_name):
    try:
        if isinstance(obj_ref, str):
            obj = bpy.data.objects.get(obj_ref)

            if obj is None:
                return
        else:
            obj = obj_ref

            if obj is None:
                return

            obj_name = obj.name
            obj = bpy.data.objects.get(obj_name)

            if obj is None:
                return

    except (ReferenceError, KeyError, TypeError):
        return

    if not hasattr(obj, "reverse_culling"):
        return

    if property_name == "physics_radius":
        clamp_native_physics(obj)

    elif property_name == "logic_radius":
        clamp_native_logic(obj)

    elif property_name == "use_physics":
        clamp_native_physics(obj)

    elif property_name == "use_logic":
        clamp_native_logic(obj)


def subscribe_object(obj):
    if obj is None:
        return

    if obj.type == 'CAMERA':
        return

    activity = obj.game.activity_culling

    try:
        bpy.msgbus.subscribe_rna(
            key=(type(activity), "physics_radius"),
            owner=_MSG_OWNER,
            args=(obj.name, "physics_radius"),
            notify=native_culling_changed,
        )

        bpy.msgbus.subscribe_rna(
            key=(type(activity), "use_physics"),
            owner=_MSG_OWNER,
            args=(obj, "use_physics"),
            notify=native_culling_changed,
        )

        bpy.msgbus.subscribe_rna(
            key=(type(activity), "logic_radius"),
            owner=_MSG_OWNER,
            args=(obj.name, "logic_radius"),
            notify=native_culling_changed,
        )

        bpy.msgbus.subscribe_rna(
            key=(type(activity), "use_logic"),
            owner=_MSG_OWNER,
            args=(obj, "use_logic"),
            notify=native_culling_changed,
        )

    except (AttributeError, TypeError, ValueError):
        pass


def draw_reversed_culling(self, context):
    layout = self.layout
    settings = context.object.reverse_culling

    subscribe_object(context.object)

    layout.separator()

    layout.label(text="Reversed Culling")

    split = layout.split()

    col = split.column()
    col.prop(
        settings,
        "physics_enabled",
        text="Reverse Physics"
    )

    sub = col.column()
    sub.active = settings.physics_enabled
    sub.prop(
        settings,
        "physics_radius"
    )

    col = split.column()
    col.prop(
        settings,
        "logic_enabled",
        text="Reverse Logic"
    )

    sub = col.column()
    sub.active = settings.logic_enabled
    sub.prop(
        settings,
        "logic_radius"
    )


class ReverseCullingSettings(bpy.types.PropertyGroup):

    physics_enabled: bpy.props.BoolProperty(
        name="Reverse Physics",
        description="Enable reversed physics activity culling",
        default=False,
        update=update_physics_enabled,
    )

    physics_radius: bpy.props.FloatProperty(
        name="Reverse Physics Radius",
        description="Distance for reversed physics activity culling",
        default=0.0,
        min=0.0,
        subtype="DISTANCE",
        update=update_physics_radius,
    )

    logic_enabled: bpy.props.BoolProperty(
        name="Reverse Logic",
        description="Enable reversed logic activity culling",
        default=False,
        update=update_logic_enabled,
    )

    logic_radius: bpy.props.FloatProperty(
        name="Reverse Logic Radius",
        description="Distance for reversed logic activity culling",
        default=0.0,
        min=0.0,
        subtype="DISTANCE",
        update=update_logic_radius,
    )


classes = (
    ReverseCullingSettings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.reverse_culling = bpy.props.PointerProperty(
        type=ReverseCullingSettings
    )

    from bl_ui.properties_game import OBJECT_PT_activity_culling

    OBJECT_PT_activity_culling.append(draw_reversed_culling)


def unregister():
    from bl_ui.properties_game import OBJECT_PT_activity_culling

    OBJECT_PT_activity_culling.remove(draw_reversed_culling)

    bpy.msgbus.clear_by_owner(_MSG_OWNER)

    del bpy.types.Object.reverse_culling

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)