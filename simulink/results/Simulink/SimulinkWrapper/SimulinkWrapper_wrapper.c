#include "SimulinkWrapper_wrapper.h"

#include <stdlib.h>

void * SimulinkWrapper_wrapper_init( )
{
	controller_context * context;
	context = (controller_context *) calloc( 1, sizeof( controller_context ) );
	controller_init( context );  //Simulink
	
	return (void *) context;  
}

void SimulinkWrapper_wrapper_destroy( controller_context * ptr )
{
	if ( ptr != NULL )
		free( (controller_context *)ptr );
}

void SimulinkWrapper_wrapper_main( controller_context * context,double Desired_L_1,double measured_L_1, double *valve_Flowfraction_1)
{
	controller_context * tcontext = (controller_context *) context;
	controller_main( tcontext,Desired_L_1,measured_L_1,valve_Flowfraction_1);
}
