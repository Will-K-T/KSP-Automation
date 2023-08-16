/********************************* TRICK HEADER *******************************
PURPOSE: (Represent the state and initial conditions of an engine)
*******************************************************************************/
#include "../include/stage.hh"

Stage::Stage(double dryMass, double wetMass, double Cd, double A):
    DRY_MASS(dryMass), WET_MASS(wetMass), DRAG_COEFF(Cd), AREA(A), engine()
{}

void Stage::calc_curr_thrust_force(double alt, double velUnitVec[3], double thrustVec[3])
{
    if (currMass - DRY_MASS > 0.0001)
    {
        engine.calc_curr_thrust_force(alt, velUnitVec, thrustVec);
    }
    else
    {
        thrustVec[0] = thrustVec[1] = thrustVec[2] = 0.0; 
    }
}