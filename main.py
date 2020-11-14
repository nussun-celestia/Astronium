from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from math import *
from celestial_body import *
from orbits import *

class Core(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
 
        properties = WindowProperties()
        properties.set_size(1000, 750)
        properties.setTitle('Astronium')
        properties.setIconFilename('icon.ico')
        
        self.set_background_color(0, 0, 0)
        self.camera.set_pos(0, -10, 0)
        self.camera.look_at((0, 0, 0))
        self.win.request_properties(properties)
        self.disable_mouse()
 
        render.set_shader_auto()

        for object_ in solar_system:
            object_.spawn()

        self.taskMgr.add(self.evolve_sim)

    def evolve_sim(self, task):
        for object_ in solar_system:
            object_.evolve()
        #print(earth.x, earth.y, earth.z)
        return task.cont

sun = Star(
    name='Sun',
    RA=0,
    dec=0,
    distance=0,
    sptype='G2V',
    radius=695990,
    mass=1.9891e+30,
    absmag=4.83,
    texture='sun_placeholder.jpg'
)

mercury = Planet(
    name='Mercury',
    radius=2439.7,
    mass=3.3011e+23,
    star=sun,
    orbit=MercuryOrbit(T),
    texture='mercury_placeholder.jpg'
)

venus = Planet(
    name='Venus',
    radius=6051.8,
    mass=4.8675e+24,
    star=sun,
    orbit=VenusOrbit(T),
    texture='venus_placeholder.jpg'
)

earth = Planet(
    name='Earth',
    radius=6378.1,
    flattening=0.0033528,
    mass=5.97237e+24,
    star=sun,
    orbit=EarthOrbit(T),
    texture='earth_placeholder.jpg'
)

mars = Planet(
    name='Mars',
    radius=3396.2,
    flattening=0.00589,
    mass=6.4171e+23,
    star=sun,
    orbit=MarsOrbit(T),
    texture='mars_placeholder.jpg'
)

jupiter = Planet(
    name='Jupiter',
    radius=71492,
    flattening=0.06487,
    mass=1.8982e+27,
    star=sun,
    orbit=JupiterOrbit(T),
    texture='jupiter_placeholder.jpg'
)

saturn = Planet(
    name='Saturn',
    radius=60268,
    flattening=0.09796,
    mass=5.6834e+26,
    star=sun,
    orbit=SaturnOrbit(T),
    texture='saturn_placeholder.jpg'
)

uranus = Planet(
    name='Uranus',
    radius=25559,
    flattening=0.0229,
    mass=8.6810e+25,
    star=sun,
    orbit=UranusOrbit(T),
    texture='uranus_placeholder.jpg'
)

neptune = Planet(
    name='Neptune',
    radius=24764,
    flattening=0.0171,
    mass=1.02413e+26,
    star=sun,
    orbit=NeptuneOrbit(T),
    texture='neptune_placeholder.jpg'
)

pluto = Planet(
    name='Pluto',
    radius=1188.3,
    mass=1.303e+22,
    star=sun,
    orbit=PlutoOrbit(T),
    texture='pluto_placeholder.jpg'
)

solar_system = (sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto)

#print(Teph)
#print(earth.orbit.xecl, earth.orbit.yecl, earth.orbit.zecl)

core = Core()
core.run()
