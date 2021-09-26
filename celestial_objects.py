import taichi as ti

@ti.data_oriented
class CelestialObject:
    def __init__(self, N, mass) -> None:
        # constants
        self.G = 1
        self.PI = 3.1415926

        # celestial object related fields
        self.n = N
        self.m = mass
        self.pos = ti.Vector.field(2, ti.f32, shape=self.n)
        self.vel = ti.Vector.field(2, ti.f32, shape=self.n)
        self.force = ti.Vector.field(2, ti.f32, shape=self.n)

    def display(self, gui, radius=2, color=0xffffff):
        gui.circles(self.pos.to_numpy(), radius=radius, color=color)

    @ti.func
    def clearForce(self):
        for i in self.force:
            self.force[i] = ti.Vector([0.0, 0.0])

    @ti.kernel
    def initialize(self, center_x: ti.f32, center_y: ti.f32, size: ti.f32, init_speed: ti.f32):
        for i in range(self.n):
            theta, r = self.generateThetaAndR(self.PI, i, self.n)
            offset_dir = ti.Vector([ti.cos(theta), ti.sin(theta)])
            center = ti.Vector([center_x, center_y])
            self.pos[i] = center + r * offset_dir * size
            self.vel[i] = ti.Vector([-offset_dir[1], offset_dir[0]]) * init_speed

    @ti.kernel
    def computeForce(self):
        self.clearForce()
        for i in range(self.n):
            p = self.pos[i]
            for j in range(self.n):
                if j != i:
                    diff = self.pos[j] - p
                    r = diff.norm(1e-2)
                    self.force[i] += self.G * self.m * self.m * diff / r**3

    @ti.kernel
    def update(self, h: ti.f32):
        for i in self.vel:
            self.vel[i] += h * self.force[i] / self.m
            self.pos[i] += h * self.vel[i]


@ti.data_oriented
class Star(CelestialObject):
    def __init__(self, N, mass) -> None:
        super().__init__(N, mass)
        pass

    @staticmethod
    @ti.func
    def generateThetaAndR(pi, i, n):
        theta = 2*pi*i/ti.cast(n, ti.f32)
        r = 1  
        return theta, r   


@ti.data_oriented
class Planet(CelestialObject):
    def __init__(self, N, mass) -> None:
        super().__init__(N, mass)
        pass

    @staticmethod
    @ti.func
    def generateThetaAndR(pi,i,n):
        theta = 2 * pi * ti.random()  # theta \in (0, 2PI)
        r = (ti.sqrt(ti.random()) * 0.4 + 0.6)  # r \in (0.6,1)    
        return theta, r   

    @ti.kernel
    def computeForce(self, stars: ti.template()):
        self.clearForce()
        G = 1.0
        for i in range(self.n):
            p = self.pos[i]

            for j in range(self.n):
                if i != j:
                    diff = self.pos[j] - p
                    r = diff.norm(1e-2)
                    self.force[i] += G * self.m * self.m * diff / r**3

            for j in range(stars.n):
                diff = stars.pos[j] - p
                r = diff.norm(1e-2)
                self.force[i] += G * self.m * stars.m * diff / r**3