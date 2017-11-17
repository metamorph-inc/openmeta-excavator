// Wrapper files

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _MSC_VER
#ifndef EXTERNAL_FUNCTION_EXPORT
#	define EXTLIB2_EXPORT __declspec( dllexport )
#else
#	define EXTLIB2_EXPORT __declspec( dllimport )
#endif
#endif

#include "SimulinkWrapper/controller_sl.h"

EXTLIB2_EXPORT void * SimulinkWrapper_wrapper_init( );
EXTLIB2_EXPORT void SimulinkWrapper_wrapper_destroy( controller_context * ptr );
EXTLIB2_EXPORT void SimulinkWrapper_wrapper_main(controller_context * context,double Desired_L_1,double measured_L_1, double *valve_Flowfraction_1 );

#ifdef __cplusplus
}
#endif
