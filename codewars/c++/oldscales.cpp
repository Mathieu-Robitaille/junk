unsigned int findBall(Scales scales) {
  switch(scales.getWeight({0, 1, 2}, {3, 4, 5})){
      case -1:
        switch(scales.getWeight({0}, {1})){
          case -1: return 0;
          case  1: return 1;
          case  0: return 2;
    }
      case 0:
        switch(scales.getWeight({6}, {7})){
          case -1: return 6;
          case  0: return 0;
          case  1: return 7;
    }
      case 1:
        switch(scales.getWeight({3}, {4})){
          case -1: return 3;
          case  1: return 4;
          case  0: return 5;
    }
  }
}