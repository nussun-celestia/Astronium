from math import *
from datetime import datetime
from astropy.time import Time
import numpy as np

def get_current_JD():
    """
    Gets the current Julian date.
    """
    date = datetime.now().isoformat()
    t = Time(date, format='isot', scale='utc')
    jd = t.jd
    return jd


def M_to_E(M, e):
    """
    Converts mean anomaly to eccentric anomaly.
    """
    E = M
    deltaE = 1
    while deltaE != 0:
        prevE = E
        E = M + e*sin(E)
        deltaE = E - prevE
    return E


def rotation_matrix(axis, theta):
    """
    Returns the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / sqrt(np.dot(axis, axis))
    a = cos(theta / 2.0)
    b, c, d = -axis * sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


class EllipticalOrbit():
    def __init__(self,
                 semimajor_axis,
                 eccentricity,
                 inclination,
                 mean_longitude,
                 longitude_of_periapsis,
                 longitude_of_ascending_node,
                 argument_of_periapsis=None,
                 mean_anomaly=None,
                 extra_values=0):

        a = semimajor_axis
        e = eccentricity
        I = inclination
        L = mean_longitude
        
        if argument_of_periapsis is None:
            argument_of_periapsis = longitude_of_periapsis - longitude_of_ascending_node

        if mean_anomaly is None:
            mean_anomaly = L - longitude_of_periapsis + extra_values

        M = mean_anomaly
        E = M_to_E(M, e)

        b = a*sqrt(1 - e**2)

        E = radians(E)
        argument_of_periapsis = radians(argument_of_periapsis)
        longitude_of_ascending_node = radians(longitude_of_ascending_node)
        I = radians(I)

        self.x = a*(cos(E) - e)
        self.y = b*sin(E)
        self.z = 0
        
        sin_aop = sin(argument_of_periapsis)
        cos_aop = cos(argument_of_periapsis)
        sin_loa = sin(longitude_of_ascending_node)
        cos_loa = cos(longitude_of_ascending_node)
            
        self.xecl = (cos_aop*cos_loa - (sin_aop*sin_loa*cos(I)))*self.x + (
                    (-sin_aop*cos_loa) - (cos_aop*sin_loa*cos(I)))*self.y

        self.yecl = (cos_aop*sin_loa + (sin_aop*cos_loa*cos(I)))*self.x + (
                    (-sin_aop*sin_loa) + (cos_aop*cos_loa*cos(I)))*self.y

        self.zecl = (sin_aop*sin(I))*self.x + (
                    (cos_aop*sin(I)))*self.y


Teph = get_current_JD()
T = (Teph - 2451545)/36525


MercuryOrbit = EllipticalOrbit(
                0.38709843,
                0.20563661 + 0.00002123*T,
                7.00559432 + -0.00590158*T,
                (252.25166724 + 149472.67486623*T) % 360,
                77.45771895 + 0.15940013*T,
                48.33961819 + -0.12214182*T
                )

VenusOrbit = EllipticalOrbit(
                0.72332102 + -0.00000026*T,
                0.00676399 + -0.00005107*T,
                3.39777545 + 0.00043494*T,
                (181.97970850 + 58517.81560260*T) % 360,
                131.76755713 + 0.05679648*T,
                76.67261496 + -0.27274174*T
                )

EarthOrbit = EllipticalOrbit(
                1.00000018 + -0.00000003*T,
                0.01673163 + -0.00003661*T,
                -0.00054346 + -0.01337178*T,
                (100.46691572 + 35999.37306329*T) % 360,
                102.93005885 + 0.31795260*T,
                -5.11260389 + -0.24123856*T
                )

MarsOrbit = EllipticalOrbit(
                1.52371243 + 0.00000097*T,
                0.09336511 + 0.00009149*T,
                1.85181869 + -0.00724757*T,
                (-4.56813164 + 19140.29934243*T) % 360,
                -23.91744784 + 0.45223625*T,
                49.71320984 + -0.26852431*T
                )
                

JupiterOrbit = EllipticalOrbit(
                5.20248019 + -0.00002864*T,
                0.04853590 + 0.00018026*T,
                1.29861416 + -0.00322699*T,
                (34.33479152 + 3034.90371757*T) % 360,
                14.27495244 + 0.18199196*T,
                100.29282654 + 0.13024619*T,
                extra_values=-0.00012452*T**2 + 0.06064060*cos(38.35125000*T) + -0.35635438*sin(38.35125000*T)
                )

SaturnOrbit = EllipticalOrbit(
                9.54149883 + -0.00003065*T,
                0.05550825 + -0.00032044*T,
                2.49424102 + 0.00451969*T,
                (50.07571329 + 1222.11494724*T) % 360,
                92.86136063 + 0.54179478*T,
                113.63998702 + -0.25015002*T,
                extra_values=0.00025899*T**2 + -0.13434469*cos(38.35125000*T) + 0.87320147*sin(38.35125000*T)
                )

UranusOrbit = EllipticalOrbit(
                19.18797948 + -0.00020455*T,
                0.04685740 + -0.00001550*T,
                0.77298127 + -0.00180155*T,
                (314.20276625 + 428.49512595*T) % 360,
                172.43404441 + 0.09266985*T,
                73.96250215 + 0.05739699*T,
                extra_values=0.00058331*T**2 + -0.97731848*cos(7.67025000*T) + 0.17689245*sin(7.67025000*T)
                )

NeptuneOrbit = EllipticalOrbit(
                30.06952752 + 0.00006447*T,
                0.00895439 + 0.00000818*T,
                1.77005520 + 0.00022400*T,
                (304.22289287 + 218.46515314*T) % 360,
                46.68158724 + 0.01009938*T,
                131.78635853 + -0.00606302*T,
                extra_values=-0.00041348*T**2 + 0.68346318*cos(7.67025000*T) + -0.10162547*sin(7.67025000*T)
                )

PlutoOrbit = EllipticalOrbit(
                39.48686035 + 0.00449751*T,
                0.24885238 + 0.00006016*T,
                17.14104260 + 0.00000501*T,
                (238.96535011 + 145.18042903*T) % 360,
                224.09702598 + -0.00968827*T,
                110.30167986 + -0.00809981*T,
                extra_values=-0.01262724*T**2
                )

##print(MercuryOrbit.xecl, MercuryOrbit.yecl, MercuryOrbit.zecl)
##print(VenusOrbit.xecl, VenusOrbit.yecl, VenusOrbit.zecl)
##print(EarthOrbit.xecl, EarthOrbit.yecl, EarthOrbit.zecl)
##print(MarsOrbit.xecl, MarsOrbit.yecl, MarsOrbit.zecl)
##print(JupiterOrbit.xecl, JupiterOrbit.yecl, JupiterOrbit.zecl)
##print(SaturnOrbit.xecl, SaturnOrbit.yecl, SaturnOrbit.zecl)
##print(UranusOrbit.xecl, UranusOrbit.yecl, UranusOrbit.zecl)
##print(NeptuneOrbit.xecl, NeptuneOrbit.yecl, NeptuneOrbit.zecl)
##print(PlutoOrbit.xecl, PlutoOrbit.yecl, PlutoOrbit.zecl)
