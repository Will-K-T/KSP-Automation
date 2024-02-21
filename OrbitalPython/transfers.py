'''
Python functions for calculating orbital transfers
Date: 02/20/23
'''

import numpy as np

# Orbit 1 data
orbit1_elements = [] # h (ang mom), i (inclination), omega (right ascension of ascending node), e (eccentricity), w (argument of perigee), theta (true anomaly)

# Orbit 2 data
orbit2_elements = []

###################################################### Constants ######################################################

R_E = 6378
u_E = 398600
g_0 = -9.80665

###################################################### Helper functions ######################################################

'''
Calculates the percent of mass required to burn in oder to achieve the desired delta v.
'''
def mass_consumed(dv, g0, isp):
    return 1 - np.exp(dv / (g0 * isp))

'''
Calculates the eccentricity of an elliptical orbit with periapsis r_p and apoapsis r_ap.
'''
def eccentricity(r_p, r_ap):
    return (r_ap - r_p) / (r_p + r_ap)

'''
Calculates the distance from the central body to the orbital body.
'''
def orbit_formula(u, h, e, theta):
    return (h**2 / u) * (1 / (1 + e * np.cos(theta)))

'''
Calculates the period of an ellipse with semi-major axis a.
'''
def ellipse_period_a(u, a):
    return (2 * np.pi * np.power(a, 3/2)) / np.sqrt(u)

'''
Calculates the period of an ellipse with angular momentum h and eccentricity e.
'''
def ellipse_period_he(u, h, e):
    return ((2 * np.pi) / u**2) * np.power((h / np.sqrt(1 - e**2)), 3)

'''
Calculates the semi-major axis of an ellipse using r_p and r_ap.
'''
def ellipse_semi_major_axis(r_p, r_ap):
    return (r_p + r_ap) / 2

'''
Calculates the angular momentum of an ellipse given radii.
'''
def ellipse_angular_mom(u, r_p, r_ap):
    return np.sqrt(u * 2) * np.sqrt((r_p * r_ap) / (r_p + r_ap))

###################################################### Transfer functions ######################################################

'''
Returns the delta V needed to complete a hohmann transfer between two elliptical orbits.

@param the radii describing the two orbits with p = periapsis and ap = apoapsis
@param u is the gravitational parameter of the central body

@returns a tuple of the delta V for the two transfer orbits ((dv for transfer from peri to apoa), (dv for transfer from apoa to peri))
the individual tuples are in the form: (dv enter transfer, dv exit transfer, dv total)
'''
def hohmann_transfer_etoe(r1_p, r1_ap, r2_p, r2_ap, u):
    #usqrt = np.sqrt(2*u)

    # Orbit 1
    #h1 = usqrt * np.sqrt((r1_p * r1_ap) / (r1_p + r1_ap))
    h1 = ellipse_angular_mom(u, r1_p, r1_ap)
    vp_1 = h1 / r1_p
    vap_1 = h1 / r1_ap

    # Orbit 2
    #h2 = usqrt * np.sqrt((r2_p * r2_ap) / (r2_p + r2_ap))
    h2 = ellipse_angular_mom(u, r2_p, r2_ap)
    vp_2 = h2 / r2_p
    vap_2 = h2 / r2_ap

    # Transfer Orbit 1
    #h3 = usqrt * np.sqrt((r1_p * r2_ap) / (r1_p + r2_ap))
    h3 = ellipse_angular_mom(u, r1_p, r2_ap)
    v_enter_t1 = h3 / r1_p
    v_exit_t1 = h3 / r2_ap

    # Transfer Orbit 2
    #h4 = usqrt * np.sqrt((r1_ap * r2_p) / (r1_ap + r2_p))
    h4 = ellipse_angular_mom(u, r2_p, r1_ap)
    v_enter_t2 = h4 / r1_ap
    v_exit_t2 = h4 / r2_p

    # Delta V's

    # Transfer 1
    dv_enter_t1 = np.abs(v_enter_t1 - vp_1)
    dv_exit_t1 = np.abs(vap_2 - v_exit_t1)

    # Transfer 2
    dv_enter_t2 = np.abs(v_enter_t2 - vap_1)
    dv_exit_t2 = np.abs(vp_2 - v_exit_t2)

    # Delta V totals
    dv_tot_t1 = dv_enter_t1 + dv_exit_t1
    dv_tot_t2 = dv_enter_t2 + dv_exit_t2

    return ((dv_enter_t1, dv_exit_t1, dv_tot_t1), (dv_enter_t2, dv_exit_t2, dv_tot_t2))

'''
Returns the delta V needed to complete a hohmann transfer from a hyperbolic orbit to an elliptical orbit.

@param r_apr is the radius of the closest approach of hyperbolic orbit
@param v_apr is the velocity at r_apr
@param the radii describing the destination orbit with p = periapsis and ap = apoapsis
@param u is the gravitational parameter of the central body

@returns a tuple containing the delta V (dv enter transfer, dv exit transfer, dv total)
'''
def hohmann_transfer_htoe(r_apr, v_apr, r_p, r_ap, u):
    # Inner Orbit
    h1 = ellipse_angular_mom(u, r_p, r_ap)
    vp = h1 / r_p

    # Transfer Orbit
    h2 = ellipse_angular_mom(u, r_p, r_apr)
    v_enter_t = h2 / r_p
    v_exit_t = h2 / r_apr

    # Delta V's

    # Enter Transfer
    dv_enter_t = np.abs(v_enter_t - vp)

    # Exit Transfer
    dv_exit_t = np.abs(v_apr - v_exit_t)

    # Delta V Total
    dv_tot_t = dv_enter_t + dv_exit_t

    return (dv_enter_t, dv_exit_t, dv_tot_t)

'''
Returns the delta V needed to complete a bielliptic hohmann transfer between two circular orbits.

@param r_0 is the radius of the smaller starting orbit
@param r_f is the radius of the larger final orbit
@param r_b is the radius to the much further point at point b
@param u is the gravitational parameter of the central body

@returns a tuple containing the delta V (dv enter transfer 1, dv enter transfer 2, dv exit transfer 2 dv total)
'''
def hohmann_bielliptic_ctoc(r_0, r_f, r_b, u):
    # Inner Orbit
    h1 = ellipse_angular_mom(u, r_0, r_0)
    v_i = h1 / r_0

    # Outer Orbit
    h2 = ellipse_angular_mom(u, r_f, r_f)
    v_f = h2 / r_f

    # Transfer Orbit 1 to point at r_b
    h3 = ellipse_angular_mom(u, r_0, r_b)
    v_enter_t1 = h3 / r_0
    v_exit_t1 = h3 / r_b

    # Transfer Orbit 2 from point r_b to destination orbit
    h4 = ellipse_angular_mom(u, r_f, r_b)
    v_enter_t2 = h4 / r_b
    v_exit_t2 = h4 / r_f

    # Delta V's

    # Enter Transfer 1
    dv_enter_t1 = np.abs(v_enter_t1 - v_i)

    # Enter Transfer 2
    dv_enter_t2 = np.abs(v_enter_t2 - v_exit_t1)

    # Exit Transfer 2
    dv_exit_t2 = np.abs(v_f - v_exit_t2)

    # Delta V Total
    dv_tot_t = dv_enter_t1 + dv_enter_t2 + dv_exit_t2

    return (dv_enter_t1, dv_enter_t2, dv_exit_t2, dv_tot_t)

hohmann_dv = hohmann_transfer_htoe(5000 + R_E, 10, 500 + R_E, 500 + R_E, u_E)

print('Delta V total: {}\nPercent mass cons: {}%'.format(hohmann_dv[2], mass_consumed(hohmann_dv[2], g_0/1000, 250)))

hohmann_dv = hohmann_transfer_etoe(480 + R_E, 800 + R_E, 22378, 22378, u_E)

print('Delta V tot1: {}\nDelta V tot2: {}'.format(hohmann_dv[0][2], hohmann_dv[1][2]))

hohmann_dv = hohmann_bielliptic_ctoc(7000, 105000, 210000, u_E)

print('Delta V total (bielliptic): {}\nFlight time: {}s'.format(hohmann_dv[3], ellipse_period_a(u_E, 56000) / 2))