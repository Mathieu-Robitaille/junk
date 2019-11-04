DOOM comes to python!
(Except this has probably been done before and better)

This is my implementation of Doom in python.

Future TODOs will reside here if they're more than a 5 minute fix
General game plan will reside here as well.




# TODOs
Build a sprite loader



BONUS FEATURES:
Use maze builder to generate map
Build parser for generated map to level
Allow character to break walls? expanding map further?




Ideas:

# Problem 1:
    Rendering takes far too long calculating the point of intersection for each pixel of the screen.TODOs

# Possible solutions:
    $ Solution 1:
        Drop horizontal pixel by pixel calculation in favor of calculating which walls are visible
        then adding these walls to a "Z buffer" ordered by distance to the player representing
        the order in which to draw objects.

        To do this I'll need to do the following.
        Calculate the point of intersection for all walls and the extreemes of player vision by sending a ray
        out in the exact same manner i've done it for the minimap view cone.intersection

        Once we know what walls intersect with the extreemes of the player's vision we can create new walls
        and check the distance to them, allowing us to store them ordered by that distance.

        Once we have which walls intersect with our vision we can then focus on walls that are within our vision.
        To figure out which walls are within our vision we can just check if the relative angle to the player is within
        the players view angle.

        After all the positions of walls have been calculated we then calculate the height of each start and end point
        in the same way we do now (ceiling and floor calc) as the height of that part of the wall,
        then use pg.draw.polygon to plop a wall down.

        Problem with this solution is im not sure how to draw it as a gradient, meaning the whole wall will be the
        same color even if it is very far.

    $ Solution 2:
        Extend python with C++ to do the calculations instead.
        "graphics" and "graphics.cpp" are files in the cpp directory which are a prototype of this concept.
        With wall data and player values passed in via stdin we can build the data required to find the exact
        point of intersection for each pixel. The test implementation is not fully functional and main code has
        not been changed to accept this new idea. However, a scratch file and temp files have been created
        to test this idea and 60 fps seems attainable as the calculation time for one frame is
        C++ Calculation time : 0.00969613 sec
        Python subprocess time : 0.01189376 sec

        with python subprocessing the c++ binary it would take 0.659... sec

        I'm not sure how I feel about this solution. I feel as it is just covering up bad design with a bandaid. As it
        stands $ Solution 1 is the better contender as once we get to thousands of walls or a higher resolution
        this solution will again pose an issue
        Speed calculation would be (SCREEN_WIDTH x WALL_COUNT x 60 )

