from dataclasses import dataclass
from orbits import *

ly_rsol = 13593198.857139902
au_rsol = 214.94255765169038

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
            self.x, self.y, self.z = rdd_to_xyz(self.RA, self.dec, self.distance)
            self.object.set_pos(self.x*ly_rsol, self.y*ly_rsol, self.z*ly_rsol)
            self.object.set_scale(self.radius/695990, self.radius/695990, self.radius/695990)

        elif isinstance(self, Planet):
            self.x, self.y, self.z = self.orbit.xecl - self.star.x, self.orbit.yecl - self.star.y, self.orbit.zecl - self.star.z
            self.object.set_pos(self.x*au_rsol, self.y*au_rsol, self.z*au_rsol)
            self.object.set_scale(self.radius/695990, self.radius/695990, self.radius/695990 - self.flattening)

        if self.texture is not None:
            self.tex = loader.load_texture('./textures/' + self.texture)
            self.object.set_texture(self.tex)

        self.object.reparent_to(render)
            
        print('Spawned', self.name)

    def evolve(self):
        """
        Moves a celestial body along its orbit
        """
        if isinstance(self, Planet):
            Teph = get_current_JD()
            T = (Teph - 2451545)/36525

            if self.name == 'Mercury':
                self.orbit = MercuryOrbit(T)
                
            elif self.name == 'Venus':
                self.orbit = VenusOrbit(T)
                
            elif self.name == 'Earth':
                self.orbit = EarthOrbit(T)
                
            elif self.name == 'Mars':
                self.orbit = MarsOrbit(T)
                
            elif self.name == 'Jupiter':
                self.orbit = JupiterOrbit(T)

            elif self.name == 'Saturn':
                self.orbit = SaturnOrbit(T)
                
            elif self.name == 'Uranus':
                self.orbit = UranusOrbit(T)
                
            elif self.name == 'Neptune':
                self.orbit = NeptuneOrbit(T)
                
            elif self.name == 'Pluto':
                self.orbit = PlutoOrbit(T)
                
            self.x, self.y, self.z = self.orbit.xecl - self.star.x, self.orbit.yecl - self.star.y, self.orbit.zecl - self.star.z

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
    flattening: float = 0
