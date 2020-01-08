#include <algorithm>
#include <iostream>
#include <ostream>
#include <numeric>
#include <random>
#include <chrono>
#include <vector>
#include <math.h>

#include "Perlin.h"

using time_pt_t = std::chrono::steady_clock::time_point;

Perlin::Perlin(unsigned int seed){
    int i = 0;
    p.resize(256);


    std::iota(p.begin(), p.end(), 0);
    std::default_random_engine engine(seed);
    std::shuffle(p.begin(), p.end(), engine);
    p.insert(p.end(), p.begin(), p.end());
}

double Perlin::noise(double x, double y, double z){
    // Find the unit cube that contains the point
    int X = (int) floor(x) & 255;
    int Y = (int) floor(y) & 255;
    int Z = (int) floor(z) & 255;

    // Find relative x, y,z of point in cube
    x -= floor(x);
    y -= floor(y);
    z -= floor(z);

    // Compute fade curves for each of x, y, z
    double u = fade(x);
    double v = fade(y);
    double w = fade(z);

    // Hash coordinates of the 8 cube corners
    int A  = p[X]     + Y;
    int AA = p[A]     + Z;
    int AB = p[A + 1] + Z;
    int B  = p[X + 1] + Y;
    int BA = p[B]     + Z;
    int BB = p[B + 1] + Z;

    double res = 
                lerp(w, lerp(v, lerp(u, grad(p[AA], x, y, z), grad(p[BA], x-1, y, z)),
                lerp(u, grad(p[AB], x, y-1, z), grad(p[BB], x-1, y-1, z))),
                lerp(v, lerp(u, grad(p[AA+1], x, y, z-1), grad(p[BA+1], x-1, y, z-1)),
                lerp(u, grad(p[AB+1], x, y-1, z-1),	grad(p[BB+1], x-1, y-1, z-1))));
    return (res + 1.0) / 2.0;
}

double Perlin::fade(double t){
    return t * t * t * (t * (t * 6 - 15) + 10);
}

double Perlin::lerp(double x, double a, double b){
    return a + x * (b - a);
}

double Perlin::grad(int hash, double x, double y, double z){
    int h = hash & 15;
    double u = h < 8 ? x : y, v = h < 4 ? y : h == 12 || h == 14 ? x : z;
    return ((h & 1) == 0 ? u : -u) + ((h & 2) == 0 ? v : -v);
}
