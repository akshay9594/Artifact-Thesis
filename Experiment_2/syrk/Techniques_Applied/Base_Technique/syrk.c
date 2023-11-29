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
/* syrk.c: this file is part of PolyBenchC */
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
#include <omp.h>
/* Include polybench common header. */
#include "../../polybench.h"
/* Include benchmark-specific header. */
#include "../../syrk.h"
/* Array initialization. */
static void init_array(int n, int m, double * alpha, double * beta, double C[(2600+0)][(2600+0)], double A[(2600+0)][(2000+0)])
{
	int i, j;
	( * alpha)=1.5;
	( * beta)=1.2;
	#pragma cetus private(i, j) 
	#pragma loop name init_array#0 
	#pragma cetus parallel 
	#pragma omp parallel for if((10000<((1L+(3L*n))+((3L*m)*n)))) private(i, j)
	for (i=0; i<n; i ++ )
	{
		#pragma cetus private(j) 
		#pragma loop name init_array#0#0 
		for (j=0; j<m; j ++ )
		{
			A[i][j]=(((double)(((i*j)+1)%n))/n);
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
			C[i][j]=(((double)(((i*j)+2)%m))/m);
		}
	}
}

/*
DCE code. Must scan the entire live-out data.
   Can be used also to check the correctness of the output.
*/
static void print_array(int n, double C[(2600+0)][(2600+0)])
{
	int i, j;
	fprintf(stderr, "==BEGIN DUMP_ARRAYS==\n");
	fprintf(stderr, "begin dump: %s", "C");
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
			fprintf(stderr, "%0.2lf ", C[i][j]);
		}
	}
	fprintf(stderr, "\nend   dump: %s\n", "C");
	fprintf(stderr, "==END   DUMP_ARRAYS==\n");
}

/*
Main computational kernel. The whole function will be timed,
   including the call and return.
*/
static void kernel_syrk(int n, int m, double alpha, double beta, double C[(2600+0)][(2600+0)], double A[(2600+0)][(2000+0)])
{
	int i, j, k;
	/* BLAS PARAMS */
	/* TRANS = 'N' */
	/* UPLO  = 'L' */
	/* =>  Form  C := alphaA*A**T + beta*C. */
	/* A is NxM */
	/* C is NxN */
	#pragma scop 
	#pragma cetus private(i, j, k) 
	#pragma loop name kernel_syrk#0 
	#pragma cetus parallel 
	#pragma omp parallel for private(i, j, k)
	for (i=0; i<n; i ++ )
	{
		#pragma cetus private(j) 
		#pragma loop name kernel_syrk#0#0 
		for (j=0; j<=i; j ++ )
		{
			C[i][j]*=beta;
		}
		#pragma cetus private(j, k) 
		#pragma loop name kernel_syrk#0#1 
		/* #pragma cetus reduction(+: C[i][j])  */
		for (k=0; k<m; k ++ )
		{
			#pragma cetus private(j) 
			#pragma loop name kernel_syrk#0#1#0 
			for (j=0; j<=i; j ++ )
			{
				C[i][j]+=((alpha*A[i][k])*A[j][k]);
			}
		}
	}
	#pragma endscop 
}

int main(int argc, char * * argv)
{
	/* Retrieve problem size. */
	int n = 2600;
	int m = 2000;
	/* Variable declarationallocation. */
	double alpha;
	double beta;
	double (* C)[(2600+0)][(2600+0)];
	double (* A)[(2600+0)][(2000+0)];
	C=((double (* )[(2600+0)][(2600+0)])polybench_alloc_data((2600+0)*(2600+0), sizeof (double)));
	;
	A=((double (* )[(2600+0)][(2000+0)])polybench_alloc_data((2600+0)*(2000+0), sizeof (double)));
	;
	/* Initialize array(s). */
	init_array(n, m,  & alpha,  & beta,  * C,  * A);
	/* Start timer. */
	/* Start timer. */
  	polybench_start_instruments;
	/* Run kernel. */
	kernel_syrk(n, m, alpha, beta,  * C,  * A);
	/* Stop and print timer. */
	/* Stop and print timer. */
	polybench_stop_instruments;
	polybench_print_instruments;
	/*
	Prevent dead-code elimination. All live-out data must be printed
	     by the function call in argument.
	*/
	if ((argc>42)&&( ! strcmp(argv[0], "")))
	{
		print_array(n,  * C);
	}
	/* Be clean. */
	free((void * )C);
	;
	free((void * )A);
	;
	return 0;
}
