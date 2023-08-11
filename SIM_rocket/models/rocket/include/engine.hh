/************************************************************************
PURPOSE: (Represent the state and initial conditions of a rocket)
LIBRARY DEPENDENCIES:
    ((rocket/src/rocket.cpp))
************************************************************************/
#ifndef ROCKET_HH
#define ROCKET_HH

class Rocket {
public:
    double exhaustSpeed;
    double 

private:
    double calc_curr_mass();
    double calc_curr_gravity_force(double rocketMass);
    double dist_to_astrobody();
};

#endif