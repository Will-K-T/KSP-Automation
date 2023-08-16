/************************************************************************
PURPOSE: (Represent the state and initial conditions of a astronomical body)
LIBRARY DEPENDENCIES:
    ((astro_body/src/astroBody.cpp))
************************************************************************/
#ifndef ASTRO_BODY_HH
#define ASTRO_BODY_HH

class AstroBody {
public:
    /* Constructors */

    AstroBody(double r, double m, double w);

    /* Operators */
    
    AstroBody& operator=(const AstroBody&);


    /* AstroBody API functions */

    void calc_curr_gravity_force(double pos[3], double acc[3]);
    double altitude(double pos[3]);

    // TODO: Should also contain an atmo and provide API
private:
    /* Class constants */

    const double radius;             /* m The radius of the object */
    const double radiusSquared;      /* m^2 The radius of the object squared */
    const double mass;               /* kg The mass of the object*/
    const double gravitationalParam; /* m^3/s^2 Equal to G * mass to save on computation */
    const double rotationalVel;      /* m/s The rotational speed of the object*/

    /* Static constants */
    
    static const double G;           /* N.m^2/kg^2 The gravitational constant */
};

#endif