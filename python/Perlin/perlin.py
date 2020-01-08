from __future__ import division
import math
import numpy as np
from random import randint



p = [randint(0, 255) for i in range(512)]

repeat = 1

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def inc(n):
    n += 1
    if repeat > 0:
        n %= repeat
    return n


def grad(ha, x, y, z):
    h = ha & 15
    u = x if h < 8 else y
    v = 0
    if h < 4:
        v = y
    elif h == 12 or h == 14:
        v = x
    else:
        v = z
    return (u if h & 1 == 0 else -u) + (v if h & 2 else -v)


def lerp(a, b, x):
    return a + x * (b - a)


def perlin(x, y, z):
    xi = int(x)
    yi = int(y)
    zi = int(z)
    xf = x - xi
    yf = y - yi
    zf = z - zi

    u = fade(xf)
    v = fade(yf)
    w = fade(zf)

    aaa = p[p[p[    xi ] +     yi ] +     zi ]
    aba = p[p[p[    xi ] + inc(yi)] +     zi ]
    aab = p[p[p[    xi ] +     yi ] + inc(zi)]
    abb = p[p[p[    xi ] + inc(yi)] + inc(zi)]
    baa = p[p[p[inc(xi)] +     yi ] +     zi ]
    bba = p[p[p[inc(xi)] + inc(yi)] +     zi ]
    bab = p[p[p[inc(xi)] +     yi ] + inc(zi)]
    bbb = p[p[p[inc(xi)] + inc(yi)] + inc(zi)]

    x1 = lerp(grad(aaa, xf,     yf,     zf),
              grad(baa, xf - 1, yf,     zf),
              u)
    x2 = lerp(grad(aba, xf,     yf - 1, zf),
              grad(bba, xf - 1, yf - 1, zf),
              u)
    y1 = lerp(x1, x2, v)

    x1 = lerp(grad(aab, xf,     yf,     zf - 1),
              grad(bab, xf - 1, yf,     zf - 1),
              u)
    x2 = lerp(grad(abb, xf,     yf - 1, zf - 1),
              grad(bbb, xf - 1, yf - 1, zf - 1),
              u)

    y2 = lerp(x1, x2, v)

    return (lerp(y1, y2, w) + 1) / 2


def perlinoctave(x, y, z, oc, pe):
    total = 0
    freq = 1
    ampl = 1
    maxval = 0
    for i in range(oc):
        total += perlin(x * freq, y * freq, z * freq) * ampl
        maxval += ampl
        ampl *= pe
        freq *= 2
    return total/maxval


