/*
Copyright (C) 1991-2022 Free Software Foundation, Inc.
   This file is part of the GNU C Library.

   The GNU C Library is free software; you can redistribute it andor
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   The GNU C Library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with the GNU C Library; if not, see
   <https:www.gnu.org/licenses/>. 
*/
/*
This header is separate from features.h so that the compiler can
   include it implicitly at the start of every compilation.  It must
   not itself include <features.h> or any other header that includes
   <features.h> because the implicit include comes before any feature
   test macros that may be defined in a source file before it first
   explicitly includes a system header.  GCC knows the name of this
   header in order to preinclude it. 
*/
/*
glibc's intent is to support the IEC 559 math functionality, real
   and complex.  If the GCC (4.9 and later) predefined macros
   specifying compiler intent are available, use them to determine
   whether the overall intent is to support these features; otherwise,
   presume an older compiler has intent to support these features and
   define these macros by default. 
*/
/*
wchar_t uses Unicode 10.0.0.  Version 10.0 of the Unicode Standard is
   synchronized with ISOIEC 10646:2017, fifth edition, plus
   the following additions from Amendment 1 to the fifth edition:
   - 56 emoji characters
   - 285 hentaigana
   - 3 additional Zanabazar Square characters
*/
/*

 * This version is stamped on May 10, 2016
 *
 * Contact:
 *   Louis-Noel Pouchet <pouchet.ohio-state.edu>
 *   Tomofumi Yuki <tomofumi.yuki.fr>
 *
 * Web address: http:polybench.sourceforge.net

*/
/* gramschmidt.c: this file is part of PolyBenchC */
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
#include <omp.h>
/* Include polybench common header. */
#include "../../polybench.h"
/* Include benchmark-specific header. */
#include "../../gramschmidt.h"
/* Array initialization. */
static void init_array(int m, int n, double A[(2000+0)][(2600+0)], double R[(2600+0)][(2600+0)], double Q[(2000+0)][(2600+0)])
{
	int i, j;
	#pragma cetus private(i, j) 
	#pragma loop name init_array#0 
	#pragma cetus parallel 
	#pragma omp parallel for if((10000<((1L+(3L*m))+((4L*m)*n)))) private(i, j)
	for (i=0; i<m; i ++ )
	{
		#pragma cetus private(j) 
		#pragma loop name init_array#0#0 
		for (j=0; j<n; j ++ )
		{
			A[i][j]=(((((double)((i*j)%m))/m)*100)+10);
			Q[i][j]=0.0;
		}
	}
	#pragma cetus private(i, j) 
	#pragma loop name init_array#1 
	#pragma cetus parallel 
	#pragma omp parallel for if((10000<((1L+(3L*n))+((3L*n)*n)))) private(i, j)
	for (i=0; i<n; i ++ )
	{
		#pragma cetus private(j) 
		#pragma loop name init_array#1#0 
		for (j=0; j<n; j ++ )
		{
			R[i][j]=0.0;
		}
	}
}

/*
DCE code. Must scan the entire live-out data.
   Can be used also to check the correctness of the output.
*/
static void print_array(int m, int n, double A[(2000+0)][(2600+0)], double R[(2600+0)][(2600+0)], double Q[(2000+0)][(2600+0)])
{
	int i, j;
	fprintf(stderr, "==BEGIN DUMP_ARRAYS==\n");
	fprintf(stderr, "begin dump: %s", "R");
	#pragma cetus private(i, j) 
	#pragma loop name print_array#0 
	for (i=0; i<n; i ++ )
	{
		#pragma cetus private(j) 
		#pragma loop name print_array#0#0 
		for (j=0; j<n; j ++ )
		{
			if ((((i*n)+j)%20)==0)
			{
				fprintf(stderr, "\n");
			}
			fprintf(stderr, "%0.2lf ", R[i][j]);
		}
	}
	fprintf(stderr, "\nend   dump: %s\n", "R");
	fprintf(stderr, "begin dump: %s", "Q");
	#pragma cetus private(i, j) 
	#pragma loop name print_array#1 
	for (i=0; i<m; i ++ )
	{
		#pragma cetus private(j) 
		#pragma loop name print_array#1#0 
		for (j=0; j<n; j ++ )
		{
			if ((((i*n)+j)%20)==0)
			{
				fprintf(stderr, "\n");
			}
			fprintf(stderr, "%0.2lf ", Q[i][j]);
		}
	}
	fprintf(stderr, "\nend   dump: %s\n", "Q");
	fprintf(stderr, "==END   DUMP_ARRAYS==\n");
}

/*
Main computational kernel. The whole function will be timed,
   including the call and return.
*/
/*
QR Decomposition with Modified Gram Schmidt:
 http:www.inf.ethz.chpersonal/gander
*/
static void kernel_gramschmidt(int m, int n, double A[(2000+0)][(2600+0)], double R[(2600+0)][(2600+0)], double Q[(2000+0)][(2600+0)])
{
	int i, j, k;
	double nrm;
	#pragma scop 
	int j_0;
	#pragma cetus firstprivate(R) 
	#pragma cetus private(i, j, j_0, k, nrm) 
	#pragma cetus lastprivate(R) 
	#pragma loop name kernel_gramschmidt#0 
	for (k=0; k<n; k ++ )
	{
		nrm=0.0;
		#pragma cetus private(i) 
		#pragma loop name kernel_gramschmidt#0#0 
		#pragma cetus reduction(+: nrm) 
		#pragma cetus parallel 
		#pragma omp parallel for if((10000<(1L+(3L*m)))) private(i) reduction(+: nrm)
		for (i=0; i<m; i ++ )
		{
			nrm+=(A[i][k]*A[i][k]);
		}
		R[k][k]=sqrt(nrm);
		#pragma cetus private(i) 
		#pragma loop name kernel_gramschmidt#0#1 
		#pragma cetus parallel 
		#pragma omp parallel for if((10000<(1L+(3L*m)))) private(i)
		for (i=0; i<m; i ++ )
		{
			Q[i][k]=(A[i][k]/R[k][k]);
		}
		/* Normalized Loop */
		#pragma cetus firstprivate(R) 
		#pragma cetus private(i) 
		#pragma cetus lastprivate(R, j_0) 
		#pragma loop name kernel_gramschmidt#0#2 
		#pragma cetus parallel 
		#pragma omp parallel for if((10000<(((((-4L+(-5L*k))+(-6L*m))+(5L*n))+((-6L*k)*m))+((6L*m)*n)))) private(i) firstprivate(R) lastprivate(R, j_0)
		for (j_0=0; j_0<=((-2+(-1*k))+n); j_0 ++ )
		{
			R[k][(1+j_0)+k]=0.0;
			#pragma cetus private(i) 
			#pragma loop name kernel_gramschmidt#0#2#0 
			/* #pragma cetus reduction(+: R[k][((1+j_0)+k)])  */
			for (i=0; i<m; i ++ )
			{
				R[k][(1+j_0)+k]+=(Q[i][k]*A[i][(1+j_0)+k]);
			}
			#pragma cetus private(i) 
			#pragma loop name kernel_gramschmidt#0#2#1 
			for (i=0; i<m; i ++ )
			{
				A[i][(1+j_0)+k]=(A[i][(1+j_0)+k]-(Q[i][k]*R[k][(1+j_0)+k]));
			}
		}
		j=((1+j_0)+k);
	}
	#pragma endscop 
}

int main(int argc, char * * argv)
{
	/* Retrieve problem size. */
	int m = 2000;
	int n = 2600;
	/* Variable declarationallocation. */
	double (* A)[(2000+0)][(2600+0)];
	double (* R)[(2600+0)][(2600+0)];
	double (* Q)[(2000+0)][(2600+0)];
	A=((double (* )[(2000+0)][(2600+0)])polybench_alloc_data((2000+0)*(2600+0), sizeof (double)));
	;
	R=((double (* )[(2600+0)][(2600+0)])polybench_alloc_data((2600+0)*(2600+0), sizeof (double)));
	;
	Q=((double (* )[(2000+0)][(2600+0)])polybench_alloc_data((2000+0)*(2600+0), sizeof (double)));
	;
	/* Initialize array(s). */
	init_array(m, n,  * A,  * R,  * Q);
	/* Start timer. */
	  /* Start timer. */
 	 polybench_start_instruments;
	/* Run kernel. */
	kernel_gramschmidt(m, n,  * A,  * R,  * Q);
	/* Stop and print timer. */
	/* Stop and print timer. */
	polybench_stop_instruments;
	polybench_print_instruments;
	;
	/*
	Prevent dead-code elimination. All live-out data must be printed
	     by the function call in argument.
	*/
	if ((argc>42)&&( ! strcmp(argv[0], "")))
	{
		print_array(m, n,  * A,  * R,  * Q);
	}
	/* Be clean. */
	free((void * )A);
	;
	free((void * )R);
	;
	free((void * )Q);
	;
	return 0;
}
