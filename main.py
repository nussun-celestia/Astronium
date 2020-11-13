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

earth = Planet(
    name='Earth',
    radius=6378.1,
    mass=5.97237e+24,
    star=sun,
    orbit=EarthOrbit,
    texture='earth_placeholder.jpg'
)

solar_system = (sun, earth)

#print(earth.orbit.xecl, earth.orbit.yecl, earth.orbit.zecl)

core = Core()
core.run()
