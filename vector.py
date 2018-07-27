import numpy as np


class Vector(np.ndarray):
    def __new__(cls, x, y, z=None):
        data = (x,y) if z is None else (x,y,z)
        obj = np.asarray(data).view(cls)
        return obj

    def __eq__(self, other):
        return bool(np.ndarray.__eq__(self, other).all())

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__repr__()

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, val):
        assert isinstance(val, (int, float))
        self[0] = val

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, val):
        assert isinstance(val, (int, float))
        self[1] = val

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, val):
        assert isinstance(val, (int, float))
        self[2] = val

    @classmethod
    def random(cls, width, height, depth=None, x0=0, y0=0, z0=0):
        coords = [
            np.random.randint(width) + x0,
            np.random.randint(height) + y0,
        ]
        if depth is not None:
            coords.append(np.random.randint(depth) + z0)
        return cls(*coords)
