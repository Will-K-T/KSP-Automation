/********************************* TRICK HEADER *******************************
PURPOSE: (Represent the state and initial conditions of a rocket)
*******************************************************************************/
#include "../include/rocket.hh"

#include "trick/exec_proto.h"
#include "trick/integrator_c_intf.h"
#include <math.h>
#include <iostream>

// Variables used to emulate the body that the rocket is launching from
const double astroBodyRadius = 6366707.0195; // m
const double astroBodyRadius2 = astroBodyRadius * astroBodyRadius; // m
// const double G = 6.67430E-11; // (N * m^2) / kg
const double astroBodyMass = 5.97219E24; // kg
const double gravitationalParam = 3.986004418E14; // G * astroBodyMass
const double astroBodyRotationalVel = 460; // m/s


/* TODO: (MOVE to util file?) Local Functions */
double magnitude(double vec[3]) {
    return sqrt(vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2]);
}

void normalize(double vec[3], double mag, double norm[3]) {
    norm[0] = vec[0] / mag;
    norm[1] = vec[1] / mag;
    norm[2] = vec[2] / mag;
}

void scalarVectorMult(double vec[3], double scalar, double result[3]) {
    result[0] = vec[0] * scalar;
    result[1] = vec[1] * scalar;
    result[2] = vec[2] * scalar;
}

int Rocket::default_data() {
    acc[0] = acc[1] = acc[2] = 0.0;
    vel[0] = vel[1] = vel[2] = 0.0;
    pos[0] = pos[1] = pos[2] = 0.0;

    mass = 1000; // 1 kg

    hasCrashed = false;
    return 0;
}

int Rocket::state_init() {
    return 0;
}

int Rocket::state_deriv() {
    //std::cout << "deriv start" << std::endl;
    acc[0] = 0.0;
    acc[1] = 0.0;
    acc[2] = 0.0;

    double curr_mass = calc_curr_mass();
    calc_curr_gravity_force();

    //std::cout << "deriv end" << std::endl;
    return 0;
}

int Rocket::state_integ() {
    //std::cout << "integ start" << std::endl;
    int integration_step;

    load_state (&pos[0],
                &pos[1],
                &vel[0],
                &vel[1], 
                (double*)0);

    load_deriv (&vel[0],
                &vel[1],
                &acc[0],
                &acc[1],
                (double*)0);

    integration_step = integrate();

    unload_state(&pos[0],
                 &pos[1],
                 &vel[0],
                 &vel[1],
                 (double*)0);

    //std::cout << "integ end" << std::endl;
    return(integration_step);
}

double Rocket::calc_curr_mass() {
    return mass;
}

void Rocket::calc_curr_gravity_force() {
    // F = m_r * g = (G * m_r * m_b) / r^2

    // Calculate the radius
    double radius_mag = magnitude(pos);
    double radius_squared = radius_mag * radius_mag;
    double posUnitVec[3];
    normalize(pos, radius_mag, posUnitVec);

    // Calculate the force of gravity
    double accGravityMag = -gravitationalParam / radius_squared;
    double accGravityVec[3];
    scalarVectorMult(posUnitVec, accGravityMag, accGravityVec);

    // Add the accelerations
    acc[0] += accGravityVec[0];
    acc[1] += accGravityVec[1];
    acc[2] += accGravityVec[2];

    // double radius = dist_to_astrobody();
    // return -(gravitationalParam * rocketMass) / (radius * radius);
}

double Rocket::dist_to_astrobody() {
    return sqrt(pos[0]*pos[0] + pos[1]*pos[1] + pos[2]*pos[2]);
}

int Rocket::shutdown() {
    double t = exec_get_sim_time();
    printf( "========================================\n");
    printf( "      Rocket State at Shutdown     \n");
    printf( "t = %g\n", t);
    printf( "pos = [%.9f, %.9f, %.9f]\n", pos[0], pos[1], pos[2]);
    printf( "vel = [%.9f, %.9f, %.9f]\n", vel[0], vel[1], vel[2]);
    printf( "radius = %.9f\n", sqrt(pos[0]*pos[0] + pos[1]*pos[1] + pos[2]*pos[2]));
    printf( "========================================\n");
    return 0 ;
}

double Rocket::impact() {
    double tgo ; /* time-to-go */
    double now ; /* current integration time. */
    
    rf.error = dist_to_astrobody() - astroBodyRadius;
    now = get_integ_time();
    tgo = regula_falsi(now, &rf);
    if (tgo == 0.0) {
        now = get_integ_time();
        reset_regula_falsi(now, &rf); 
        hasCrashed = true;
        vel[0] = 0.0; vel[1] = 0.0;
        acc[0] = 0.0; acc[1] = 0.0;
    }
    return (tgo) ;
}
