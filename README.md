Culling Overhaul is an addon for UPBGE 0.5 that expands UPBGE's built-in Activity Culling system 
by adding Reversed Physics Culling and Reversed Logic Culling. Normally, UPBGE's Activity Culling 
disables physics or logic when an object gets too far away from an active camera. Culling Overhaul 
adds the opposite behavior: physics and/or logic can also be disabled when an object gets too close 
to the camera. Together, the two systems allow an object to remain active only within a specific 
distance range.

How It Works

This creates an activity zone between the reversed radius and UPBGE's normal Activity Culling radius.

For example:
Reverse Physics Radius: 20m
Native Physics Radius:  100m

when within the 20m or outer 100m it would be Culled, while being in between the two would be Active.

The same system can be used independently for both Physics and Logic.

Features

Reverse Physics Culling

When enabled, an object's physics are suspended while the object is inside the Reverse Physics Radius.
Once the object leaves that radius, its physics are restored. This can be combined with UPBGE's native 
Physics Activity Culling to create a minimum and maximum physics activity distance.

Reverse Logic Culling

Reverse Logic works the same way as Reverse Physics Culling, but controls the object's game logic.
Logic is suspended while the object is inside the Reverse Logic Radius and restored once it leaves 
the radius. Reverse Physics and Reverse Logic can be enabled independently and can use different radius.

Installation

Place the Culling Overhaul addon in your UPBGE addons directory and enable it from:

Edit - Preferences - Add-ons - Install From Disk

Once enabled, select a game object and open its Activity Culling settings.

The addon adds a new section:

Reversed Culling

[ ] Reverse Physics
    Reverse Physics Radius

[ ] Reverse Logic
    Reverse Logic Radius

Using Reverse Physics

Enable:

Reverse Physics

Then choose the desired:

Reverse Physics Radius

Example:

Reverse Physics Radius = 25m

The object's physics will be suspended whenever an Activity Culling camera comes within 25 meters.
When the camera moves beyond 25 meters, physics are restored.

If native Physics Activity Culling is also enabled:

Reverse Physics Radius = 25m
Native Physics Radius  = 150m

the object will only have active physics between:

25m – 150m

Using Reverse Logic

Enable:

Reverse Logic

Then choose:

Reverse Logic Radius

Example:

Reverse Logic Radius = 40m
Native Logic Radius  = 200m

The object's logic will only remain active between:

40m – 200m

Automatic Radius Protection

Culling Overhaul prevents the reversed radius from extending beyond the corresponding native 
Activity Culling radius.

For example, if:

Native Physics Radius = 100m

the Reverse Physics Radius cannot effectively exceed: 100m

This prevents invalid activity ranges where the reversed and native culling systems would conflict.
The same protection is applied to Logic Culling.

Why Use Reversed Culling?

Normal distance culling is useful for disabling objects that are too far away. Reversed culling makes 
it possible to disable systems that are unnecessary near the player/camera while keeping them active 
farther away.

More importantly, combining normal and reversed culling provides a general-purpose way to create 
controlled activity ranges:

Too Close    |     Desired Range       |    Too Far

  CULLED    |          ACTIVE          |     CULLED
------------|--------------------------|------------
            ^          ^
         Reverse     Native
         Radius      Radius

Physics and Logic can each have their own activity range.
This can be useful for large scenes and open-world projects where different systems only need 
to operate at particular distances.

Requirements

UPBGE 0.5

Python Components

Activity Culling cameras
