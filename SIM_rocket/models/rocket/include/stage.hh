/************************************************************************
PURPOSE: (Represent the state and initial conditions of a single stage)
LIBRARY DEPENDENCIES:
    ((rocket/src/stage.cpp))
************************************************************************/
#pragma once

#include "engine.hh"

class Stage {
public:
    /* Constructors */

    Stage(double dryMass, double wetMass, double Cd, double A);

    /* Operators */
    
    // AstroBody& operator=(const AstroBody&);

    /* Class constants */

    const double DRY_MASS;   /* kg The mass of the stage without fuel */
    const double WET_MASS;   /* kg The mass of the stage with fuel */
    const double DRAG_COEFF; /* -- The coefficient of drag for the stage */
    const double AREA;       /* m^2 The cross sectional aread of the stage */

    /* State variables */
    double currMass;         /* kg The current mass of the stage */
    Engine engine;           /* ** The engine that provides the thrust for the stage */

    /* Stage API functions */

    void calc_curr_thrust_force(double alt, double velUnitVec[3], double thrustVec[3]);
private:
};