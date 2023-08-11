/************************************************************************
PURPOSE: (Represent the state and initial conditions of a rocket)
LIBRARY DEPENDENCIES:
    ((rocket/src/rocket.cpp))
************************************************************************/
#ifndef ROCKET_HH
#define ROCKET_HH

#include "trick/regula_falsi.h"

class Rocket {
public:
    double acc[3];
    double vel[3];
    double pos[3];
    double mass;
    bool hasCrashed;
    REGULA_FALSI rf;

    int default_data();
    int state_init();
    int state_deriv();
    int state_integ();
    int shutdown();
    double impact();

private:
    double calc_curr_mass();
    void calc_curr_gravity_force();
    double dist_to_astrobody();
};

#endif