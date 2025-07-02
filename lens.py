# Simple 2D ray tracing to visualize refraction through a thin lens
# Implementation uses basic Python and matplotlib for visualization.
# The script traces several parallel rays and shows how they refract
# when passing through a biconvex lens.

import math

try:
    import matplotlib.pyplot as plt
except ImportError:  # matplotlib might not be available in some environments
    plt = None


# ------------ Vector utilities ------------

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def norm(v):
    return math.sqrt(dot(v, v))


def normalize(v):
    n = norm(v)
    return (v[0] / n, v[1] / n)


# ------------ Geometry helpers ------------

def line_circle_intersection(origin, direction, center, radius):
    """Return the smallest positive intersection distance t or None."""
    # Solve |origin + t*dir - center|^2 = radius^2
    ox, oy = origin
    dx, dy = direction
    cx, cy = center
    a = dx * dx + dy * dy
    b = 2 * (dx * (ox - cx) + dy * (oy - cy))
    c = (ox - cx) ** 2 + (oy - cy) ** 2 - radius * radius
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)
    ts = [t for t in (t1, t2) if t > 1e-6]
    if not ts:
        return None
    return min(ts)


def refract(direction, normal, n1, n2):
    """Refract an incident vector using Snell's law."""
    d = normalize(direction)
    n = normalize(normal)
    cos_i = -dot(n, d)
    mu = n1 / n2
    sin2_t = mu * mu * (1.0 - cos_i * cos_i)
    if sin2_t > 1.0:
        return None  # Total internal reflection
    cos_t = math.sqrt(1.0 - sin2_t)
    rx = mu * d[0] + (mu * cos_i - cos_t) * n[0]
    ry = mu * d[1] + (mu * cos_i - cos_t) * n[1]
    return normalize((rx, ry))


# ------------ Lens definition ------------
class Lens:
    def __init__(self, radius1=40.0, radius2=-40.0, thickness=10.0, n=1.5, aperture=20.0):
        self.radius1 = radius1
        self.radius2 = radius2
        self.thickness = thickness
        self.n = n
        self.aperture = aperture
        # Circle centers for the two spherical surfaces
        self.center1 = (radius1, 0.0)
        self.center2 = (thickness + radius2, 0.0)


# ------------ Ray tracing ------------

def trace_ray(origin, direction, lens):
    path = [origin]
    dir1 = normalize(direction)

    # Intersect with first surface
    t = line_circle_intersection(origin, dir1, lens.center1, abs(lens.radius1))
    if t is None:
        return path
    p1 = (origin[0] + dir1[0] * t, origin[1] + dir1[1] * t)
    path.append(p1)
    n1 = (p1[0] - lens.center1[0], p1[1] - lens.center1[1])
    dir2 = refract(dir1, n1, 1.0, lens.n)
    if dir2 is None:
        return path

    # Intersect with second surface
    t = line_circle_intersection(p1, dir2, lens.center2, abs(lens.radius2))
    if t is None:
        return path
    p2 = (p1[0] + dir2[0] * t, p1[1] + dir2[1] * t)
    path.append(p2)
    n2 = (p2[0] - lens.center2[0], p2[1] - lens.center2[1])
    dir3 = refract(dir2, n2, lens.n, 1.0)
    if dir3 is None:
        return path

    # Propagate some distance after the lens
    far = lens.thickness + 50.0
    t = (far - p2[0]) / dir3[0]
    p3 = (p2[0] + dir3[0] * t, p2[1] + dir3[1] * t)
    path.append(p3)
    return path


# ------------ Visualization ------------

def plot_lens(ax, lens):
    ys = [i * 0.01 for i in range(int(-lens.aperture * 50), int(lens.aperture * 50))]
    x1 = []
    x2 = []
    for y in ys:
        dy1 = math.sqrt(max(lens.radius1 ** 2 - (y) ** 2, 0.0))
        dy2 = math.sqrt(max(lens.radius2 ** 2 - (y) ** 2, 0.0))
        x1.append(lens.center1[0] - dy1)
        x2.append(lens.center2[0] + dy2)
    ax.plot(x1, ys, color="blue")
    ax.plot(x2, ys, color="blue")


def main():
    lens = Lens()
    rays = []
    for y in [-8, -4, -2, 0, 2, 4, 8]:
        rays.append(trace_ray((-50.0, float(y)), (1.0, 0.0), lens))

    if plt is None:
        print("matplotlib is required for plotting")
        return

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    for path in rays:
        xs, ys = zip(*path)
        ax.plot(xs, ys, color="red")
    plot_lens(ax, lens)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Ray tracing through a lens")
    plt.show()


if __name__ == "__main__":
    main()
