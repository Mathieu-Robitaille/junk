For non-rectangular geometry I'll need an easy way to plot map lines with extra data
At the start my thoughts are to use PyQT? as a window manager and pack the data via JSON

Nice to haves for this project
    
    A camera rendering the level as the game would 


Data I need as of now

Wall data {
    
    Wall start/end = (x1, y1), (x2, y2), (z1, z2) z1 and z2 are the floor and ceiling height if i can figure that out

    Window?        = Bool

    Window pos     = (x1, y1), (x2, y2) (z1, z2) z1 and z2 represent the area in the wall that is a window. probably going to be a percentage

    Wall texture   = file to get the texture from
}

General map data {

    Skybox file
    
    

}

Area map data {
    
    Floor texture
    
    Ceiling texture
    
}


