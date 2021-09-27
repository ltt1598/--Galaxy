import taichi as ti
from celestial_objects import Star, Planet

if __name__ == "__main__":

    ti.init(arch=ti.cuda)

    # control
    paused = False
    export_images = False

    # stars and planets
    stars = Star(N=2, mass=1000)
    stars.initialize(0.5, 0.5, 0.2, 10)
    planets = Planet(N=1000, mass=1)
    planets.initialize(0.5, 0.5, 0.4, 10)

    # GUI
    my_gui = ti.GUI("Galaxy", (800, 800))
    h = 5e-5
    i = 0
    while my_gui.running:

        for e in my_gui.get_events(ti.GUI.PRESS):
            if e.key == ti.GUI.ESCAPE:
                exit()
            elif e.key == ti.GUI.SPACE:
                paused = not paused
                print("paused =", paused)
            elif e.key == 'r':
                stars.initialize(0.5, 0.5, 0.2, 10)
                planets.initialize(0.5, 0.5, 0.4, 10)
            elif e.key == 'i':
                export_images = not export_images

        if not paused:
            stars.computeForce()
            planets.computeForce(stars)
            for celestial_obj in (stars, planets):
                celestial_obj.update(h)
            i += 1

        stars.display(my_gui, radius=10, color=0xffd500)
        planets.display(my_gui)
        if export_images:
            my_gui.show(f"images\output_{i:05}.png")
        else:
            my_gui.show()