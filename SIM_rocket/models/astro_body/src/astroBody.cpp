/********************************* TRICK HEADER *******************************
PURPOSE: (Represent the state and initial conditions of a astronomical body)
*******************************************************************************/
#include "../include/astroBody.hh"

#include "trick/trick_math.h"

/* ------------------------------------ Class Constants ------------------------------------ */

const double AstroBody::G = 6.674E-11;

/* ------------------------------------ Class Constructors --------------------------------- */

AstroBody::AstroBody(double r, double m, double w):
    radius(r), radiusSquared(r*r), mass(m), gravitationalParam(G * m), rotationalVel(w) {}

/* ------------------------------------ Class Operators ------------------------------------ */

AstroBody& AstroBody::operator=(const AstroBody& other)
{
    if (this != &other)
    {
        // Nothing to copy
    }
    return *this;
}

/* ------------------------------------ Class Functions ------------------------------------ */

/** 
 * @brief Calculates the acceleration of gravity acting on the object
 * 
 * @related
 * Equations Used:
 * F = m_rocket * g = (G * m_rocket * m_body) / r^2 = (gravitational_param * m_body) / r^2
 * 
 * @param [in]:  pos The position of the object
 * @param [out]: acc The acceleration of the object to be updated
 * 
*/
void AstroBody::calc_curr_gravity_force(double pos[3], double acc[3])
{

    // Calcualte a unit vector for the position of the object
    double posMagnitude = dv_mag(&pos[0]);
    double posUnitVec[3] = {pos[0] / posMagnitude, pos[1] / posMagnitude, pos[2] / posMagnitude};

    // Calculate the force of gravity
    double posMagnitudeSquared = posMagnitude * posMagnitude;
    double accGravityMag = -gravitationalParam / posMagnitudeSquared;
    double accGravityVec[3];
    dv_scale(accGravityVec, posUnitVec, accGravityMag);

    // Add the acceleration of gravity to the object
    acc[0] += accGravityVec[0];
    acc[1] += accGravityVec[1];
    acc[2] += accGravityVec[2];
}

/** 
 * @brief Calculates how high an object is above the body's surface
 * 
 * @param [in]: pos The position of the object
 * 
 * @returns The altitude of the object in meters
 * 
*/
double AstroBody::altitude(double pos[3])
{
    double posMag = dv_mag(&pos[0]);
    return posMag - radius;
}