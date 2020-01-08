#include <cmath>
#include "ppm.h"
#include "Perlin.h"

int main(int argc, char** argv){
    unsigned int width = 1200, height = 800;

    ppm image(width, height);

    unsigned int seed = atoi(argv[1]);
    Perlin pn(seed);

    unsigned int kk = 0;
    for(unsigned int i = 0; i < height; ++i){ // y
        for(unsigned int j = 0; j < width; ++j){ // x
            double x = (double)j/(double)width;
            double y = (double)i/(double)height;

            // Wood like structure
            double n = 10 * pn.noise(x, y, 0.8);
            n = n - floor(n);

            image.r[kk] = floor(255 * n);
            image.g[kk] = floor(255 * n);
            image.b[kk] = floor(255 * n);
            kk++;
        }
    }
    image.write("result.ppm");
    return 0;
}
