#include <iostream>
#include <ostream>
#include <chrono>
#include <vector>
#include <math.h>

using time_pt_t = std::chrono::steady_clock::time_point;

struct Point {
    float x;
    float y;
} ;

struct Line {
    Point p1;
    Point p2;
} ;

struct DistWall {
    float d; // Distance to the wall
    Point p; // Point of intersection
    Line  w; // Wall collided with
};


Point create_point(float x, float y){
    Point point;
    point.x = x;
    point.y = y;
    return point;
}

Line create_line(Point p1, Point p2){
    Line line;
    line.p1 = p1;
    line.p2 = p2;
    return line;
}

DistWall create_distwall(float d, Point p, Line w){
    DistWall distwall;
    distwall.d = d;
    distwall.p = p;
    distwall.w = w;
    return distwall;
}

Point line_intersection(Line l1, Line l2){
    float d = (l2.p2.y - l2.p1.y) * (l1.p2.x - l1.p1.x) - (l2.p2.x - l2.p1.x) * (l1.p2.y - l1.p1.y);
    if(d == 0){
        return create_point(-1, -1);
    }
    float a = (l2.p2.x - l2.p1.x) * (l1.p1.y - l2.p1.y) - (l2.p2.y - l2.p1.y) * (l1.p1.x - l2.p1.x);
    float b = (l1.p2.x - l1.p1.x) * (l1.p1.y - l2.p1.y) - (l1.p2.y - l1.p1.y) * (l1.p1.x - l2.p1.x);

    float ra = a / d;
    float rb = b / d;

    if (0 <= ra <= 1 && 0<= rb <= 1){
        float x = l1.p1.x + (ra * (l1.p2.x - l1.p1.x));
        float y = l1.p1.y + (ra * (l1.p2.y - l1.p1.y));
        return create_point(x, y);
    } else {
        return create_point(-1, -1);
    }
}

std::vector<Line> get_walls(int argc, char** argv){
    std::vector<Line> walls;

    for (int i = 4; i < argc - 4; i+=4) {
        Point start = create_point(atof(argv[i]), atof(argv[i+1]));
        Point end = create_point(atof(argv[i+2]), atof(argv[i+3]));
        walls.push_back(create_line(start, end));
    }
}
float distance_to_point(Point p1, Point p2){

}

std::vector<DistWall> get_intersections(Point player_pos, float player_angle, float player_fov, int iterations, std::vector<Line> walls){
    std::vector<DistWall> intersections;
    for(int i = 0; i == iterations; i++){
        float ray_angle = (player_angle - player_fov / 2) + i / iterations * player_fov;
        float x = player_pos.x + sin(ray_angle) * 100;
        float y = player_pos.y + cos(ray_angle) * 100;
        Point player_end = create_point(x, y);
        Line player_line = create_line(player_pos, player_end);
        std::vector<DistWall> distances;
        
        for(std::vector<int>::size_type j = 0; j != walls.size(); j++) {
            Point intersect = line_intersection(player_line, walls[j]);
            if (intersect.x != -1 && intersect.y != -1){
                float dist = distance_to_point(player_pos, intersect);
                DistWall val = create_distwall(dist, intersect, walls[j]);
                distances.push_back(val);
            }
            
        }
    }
}

int main(int argc, char** argv){

    //
    // The order of data being entered should be (filename, player_pos_x, player_pos_y, player_angle, player_fov, iterations(SCREEN_WIDTH), *wall_info)
    //
    Point player_pos   = create_point(atof(argv[1]), atof(argv[2]));
    float player_angle = atof(argv[3]);
    float player_fov   = atof(argv[4]);
    int iterations     = atof(argv[5]);
    std::vector<Line> walls = get_walls(argc, argv);

    time_pt_t start_time = std::chrono::steady_clock::now();

    std::vector<DistWall> intersections = get_intersections(player_pos, player_angle, player_fov, iterations, walls);

    time_pt_t end_time = std::chrono::steady_clock::now();

    std::cout << "X: " << intersect.x << " | Y: " << intersect.y << std::endl;

    std::chrono::duration<double> et =
        std::chrono::duration_cast<std::chrono::duration<double>>(end_time - start_time);
    std::cout << "Checking took: " << et.count() << " sec" << std::endl;

}