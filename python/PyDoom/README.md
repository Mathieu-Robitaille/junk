# DOOM comes to python!
(Except this has probably been done before and better)

This is my implementation of Doom in python.

I've tried to cram as much info into my commits as possible while also keeping them short
Normally a ticket would get filled with information detailing each commit, but building an externally
viewable system for one project would be cumbersome

Code is being commented as it becomes more permanent.
I've recently finished the render manager, There are a ton of helper functions that need to be
refactored and commented in that file to allow it to be actually human readable.


Future TODOs will reside here if they're more than a 5 minute fix
General game plan will reside here as well.

# DoomCAD

I need to move away from having map data as a string, time to build a tool to facilitate constructing levels.
DoomCAD will serve this purpose.

The core idea behind DoomCAD is to act as its name implies, similar to AutoCAD it should let me plop shapes together
easily and assign data to those shapes such as texture name, height, window info, etc...

Controls right now are

Left CTRL = Pan around
Left SHIFT = Rectangle

left click & Drag with no keys = Line
Right Click = Move line point

# Imports
As I work more on this project I'm discovering my imports are not so great...
I'll have to read up more on how larger projects handle passing data all over

# Structure
I've recently tried to re-work the structure of this project to follow the concepts in the following link

https://docs.python-guide.org/writing/structure/


# In depth explanation of concepts in use

-- Wall building --

Being able to pass a string, level width, and height makes building levels much easier.
We can easily parse this into collision using the following algorithm.
Start at the top left, moving the same way you would read a page.
At each cell as the following questions to decide if and where walls should be placed.

Is there a cell to the north of this one?
    if yes:
        is there a cell to the west of me?
            if yes: pass
            if no: does the north cell have a westward wall?
                if yes: extend that wall down to me
                if no: it must have a western neighbor so i need to create a west wall
        is there a cell the east of me?
            if yes: pass
            if no: doest the north cell have an eastward wall?
                if yes: extend that wall down to me
                if no: it must have a western neighbor so i need to create an east wall

Continue this line of questions for each of this cell's walls to eventually build "polygons" representing the walls
passed into the function.

Once we have this, we have line segments we can use for collision and rendering.

-- Renderer --

Initially I had constructed a ray marcher which would calculate the rough distance to a wall for each horizontal
pixel of the screen by stepping 0.1 units at a time until we're indexed into the level string at a pound sign.
This distance value would be used to calculate the height of the walls, where the player can/cannot move, the shade of
the wall, etc...
There were several problems with this implementation,
- It was computationally expensive (under 30 frames per second)
- The walls drawn were very jagged
- It didn't look good
Here is a photo of this

https://cdn.discordapp.com/attachments/622095211748786237/634129259840929831/wallheadon.gif


After realising ray marching is not an option moving forward I began to evaluate other methods of distance calculation
eventually coming to treating each horizontal slice of player vision as a line (starting poing, end point) to check
where that intersected with each wall via some linear algebra... after spending much too long re-learning linear I found
a solution to my problem. Unfortunately I took no video of this solution as it was rendering at ~0.7 frames per second.
A very... mild... performance hit. This was due to the calculation speed of the shapely library net being fast enough.
(horizontal width (1200) x number of walls (~30) x 0.0001s to run the calculation)
Eventually I hand wrote a solution to this which can be found in render_manager.py called line_intersection
This sped up render times drastically, allowing ~12 fps on fairly strong computer. pictured below.
Still far too slow, but better.

https://imgur.com/VjOvdhg

After spending a fair amount of time trying to find a way to simplify this I came to this realisation,
I do not need to calculate the distance for each pixel,
I can instead calculate the distance of each endpoint of each wall which would give me most of the information i need.
Then I can check how far that point is from the left side of the screen to get the x position to draw it at.

This would work, BUT it would also need a form of culling to save performance again.

Which led to my current implementation boasting 200+ fps for complex level geometry.

We "cast" a line to the left and right of player vision and check what intersects with those lines.
If there is an intersection with a wall, there must be a point in player vision so we create a new wall with p1 as
the intersection and p2 as the point of the wall in the triangle that is player vision.

This handles all walls touching the extremes of player vision.
All we need next is to find which walls have all points fully within player vision and create those as walls as well.
Now we have newly created wall objects for this frame containing the exact information we need to draw them.

We can then check "how far" each point is from the left fov extreme in radians,
normalize this value between 0-SCREEN_WIDTH for x.
we check what the angle fro, the left and right lines are to get the current max for the normalization.
Unfortunately this causes two problems, one when you're close to walls, one when you look down a hallway.
Namely fisheye for hallways, and improper geometry when you're really close to walls.
This should be fairly easily fixed however.

The renderer's current status is pictured below.

https://imgur.com/7e53wMF


$MANGLING
At the extremes of the camera walls would lose their shape and snap to the borders of the window.
This is intended but not in the method previously done as it made for very ugly corners and walls when parallel.

I've commented the get_x_coordinates function with my previous thoughts as to why it was broken and now what has fixed it.
Because the walls were not allowed to be represented as their true size, when very close to them they would deform. 

    Stripped out the ceiling if statement and it resolved
    This issue.
    self.ceiling_p2 = (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / (self.p2_d \
        if self.p2_d >= RENDER_WALL_SIZE else RENDER_WALL_SIZE)


# TODOs
Build a sprite loader with translating based on enemy angle


# Next big rewrites
Allow non rectangular level geometry. 
Allow walls to have windows.
Build a binary space partitioner for new level geometry, may walls = slow game if not handled properly
	A chunk manager could do well for this, I'm already ray casting for colliding walls, a ray to each chunk within the fov wouldnt be horrendous for speed


BONUS FEATURES:
Use maze builder to generate map
Build parser for generated map to level
Allow character to break walls? expanding map further?

BUGS (Ahem... Features)
Renderer currently draws walls out of order some times, Likely a simple fix.
