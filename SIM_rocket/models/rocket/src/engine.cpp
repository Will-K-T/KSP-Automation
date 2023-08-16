/********************************* TRICK HEADER *******************************
PURPOSE: (Represent the state and initial conditions of an engine)
*******************************************************************************/
#include "../include/engine.hh"
#include "../../astro_body/include/interpolate.hh"

#include "trick/vector_macros.h"

#define NUM_ELEMENTS 10

const double ALTITUDE_ARRAY[NUM_ELEMENTS] = 
{
    // TODO: Populate array using KSP data
};
const double THRUST_ARRAY[NUM_ELEMENTS] = 
{
    // TODO: Populate array using KSP data
};

Engine::Engine():
    thrustSampleAlts(ALTITUDE_ARRAY), thrustSampleValues(THRUST_ARRAY), thrustSampleCount(NUM_ELEMENTS),
    thrustLimiter(1.0)
{}

void Engine::calc_curr_thrust_force(double alt, double velUnitVec[3], double thrustVec[3])
{
    // double thrustMag = interpolate(alt, thrustSampleAlts, thrustSampleValues, thrustSampleCount);
    double thrustMag = 12000;
    V_SCALE(thrustVec, velUnitVec, thrustMag);
}