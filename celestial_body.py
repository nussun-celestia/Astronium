from dataclasses import dataclass
from orbits import *

def rdd_to_xyz(RA, dec, dist):
    RA = radians(RA)
    dec = radians(dec)
    
    x = (dist * cos(dec)) * cos(RA)
    y = (dist * cos(dec)) * sin(RA)
    z = dist * sin(dec)

    return x, y, z

@dataclass
class CelestialBody:
    name: str
    radius: float
    mass: float
    texture: str

    def spawn(self):
        """
        Spawns a celestial body
        """
        self.object = loader.loadModel('sphere')
        
        if isinstance(self, Star):
            x, y, z = rdd_to_xyz(self.RA, self.dec, self.distance)

        elif isinstance(self, Planet):
            x, y, z = self.orbit.xecl, self.orbit.yecl, self.orbit.zecl

        self.object.set_pos(x*214.94255765169038, y*214.94255765169038, z*214.94255765169038)
        self.object.set_scale(self.radius/695990, self.radius/695990, self.radius/695990)

        if self.texture is not None:
            self.tex = loader.load_texture('./textures/' + self.texture)
            self.object.set_texture(self.tex)

        self.object.reparent_to(render)
            
        print('Spawned', self.name)

    def evolve(self):
        """
        Moves a celestial body along its orbit
        """

@dataclass
class Star(CelestialBody):
    """
    Stores info of stars.
    """
    RA: float
    dec: float
    distance: float
    sptype: str
    appmag: float = None
    absmag: float = None

@dataclass
class Planet(CelestialBody):
    """
    Stores info of planets.
    """
    star: Star
    orbit: EllipticalOrbit
