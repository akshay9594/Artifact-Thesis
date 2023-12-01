# Artifact Description for the Evaluation of Subscripted Subscript Analysis

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10223264.svg)](https://doi.org/10.5281/zenodo.10223264)

This README describes how to evaluate the artifact for Chapter 3 of the PhD thesis: 
"Compile-time Automatic Parallelization of Subscripted Subscripts using Recurrence Analysis".

## What is reproduced?
The Artifact reproduces major parts of the evaluation results of Experiment 1 and 
Experiment 2 mentioned in Section 3.9 of the thesis. More specifically, the following results are
reproduced:

### For Experiment 1:
The speedup graphs for benchmarks AMGmk, SDDMM, CHOLMOD Supernodal, UA(transf) shown in Figure 3.17. 
The scripts produce one graph per benchmark. The graphs plot the performance improvement of the
Cetus parallel codes (OpenMP parallelization) v/s the Serial baseline.

Note: 
- In the interest of time, for UA-NAS benchmark, CLASSES A, B, C are used.
- The results in Figure 3.16 of the thesis are NOT reproduced, but the source files are provided
  within the *Cetus-Output-WithoutSubSub* subdirectories.
- The scripts measure and plot the performance improvement for the maximum number of cores 
  available on the machine. The scripts cannot vary the number of available cores.

### For Experiment 2

The speedup graph shown in Figure 3.20 of the thesis. The graph compares the impact of the classical
automatic parallelization and that of the New technique (*Cetus+NewAlgo*) on the performance 
of 12 benchmarks listed in Table 3.1 of the thesis. The table also shows the inputs used for each benchmark. 
We used MATRIX2, dielFilterV2clx, spal_004 and CLASS A as input datasets for the AMGmk, SDDMM, 
CHOLMOD Supernodal and UA applications respectively in Experiment 2.

Note:
  The scripts measure and plot the performance improvement for the maximum number of cores 
  available on the machine. The scripts cannot vary the number of available cores.

## Prerequisities
### Software
 - Linux (OS tested with : CentOS v7.4, Ubuntu v22.04)
 - GNU C Compiler (GCC) v4.8.5 and above
 - Python v3.8.0 and above
 - OpenMP v4.0 and above
 - awk
 - bc (linux calculator)
 - gfortran

### Python packages required
- Non built-in packages:
1. matplotlib
 - Built-in packages:
2. subprocess
3. re
4. math
5. os
6. Numpy
7. shutil

### Hardware
 - Machine with x86-64 processors (preferably Sky Lake and beyond)
 - ~4GB of disk space
 - Atleast 8GB of Memory

## Obtaining the Codes
- The codes can be obtained from the Zenodo repository using the DOI above or from Github:
  https://github.com/akshay9594/Artifact-Thesis.git

- A zipped folder is downloaded. Unzip the folder.

## Code description
- The source code files for each experiment are placed in the directories -- *Experiment_1*
    and *Experiment_2*.
- For each benchmark, the Baseline and Optimized (Technique(s)_Applied) source files  
  are provided.
- The optimized files refer to the Cetus translated versions of the original source code.
- In *Experiment_1*, the source files are further arranged according to the inputs to a 
  benchmark if the benchmark uses internally generated (within the code) inputs. 
  E.g. for amgmk, the source files are arranged into directories *MATRIX1* through *MATRIX5* 
  as these matrices are internally generated. 
- In *Experiment_2*, the optimized source files are further arranged in the directory
  *New_Technique* (referring to the New Algorithm presented in the thesis).

## Installing the dependencies

### Installing awk, bc and gfortran

Following commands can be used to install awk, bc and gfortran using the apt package manager:

```
 sudo apt-get install -y gawk
 sudo apt-get install -y bc
 sudo apt-get install -y gfortran
```

### Installing the non built-in python packages
The non built-in packages have been mentioned in requirements.txt and can be installed 
using the python package manager : pip or pip3, using the command:
```
pip install -r requirements.txt
```

## Compiling and Running the Codes

Expected Completion time: ~1 hour for each experiment, total ~2 hrs.
Each benchmark is run 3 times.

### The master script:

- The master script to perform the evaluation is the python script : "master.py".
- The master script is an interactive script and uses user input to determine which 
  experiment to run -- *Experiment 1*, *Experiment 2* or both.
- The script automatically downloads external inputs required to run some benchmarks.
- Run the master script using the following command:

    ```
    python3 master.py
    ```
- The script compiles the benchmark files, executes the binaries and records the measurements. 

### Generated Results:

- The master script generates the following:

1. Execution time and Speedup Reports for each benchmark and each experiment
   - The result reports for each experiment are placed in the *Reports* directory.
   - The reports show the average execution times of the baseline and optimized codes
     and the calculated average speedups.

2. Graphs for each Experiment
   - The generated graphs for each experiment are placed in the *Graphs* directory,
     within the *Exp-1* and *Exp-2* subdirectories.
   - *Exp-1* stores the graphs of Experiment 1 and *Exp-2* stores the graphs of Experiment 2.

     
## Translating an input code through the Cetus executable (Optional):

- A Cetus executable has been provided which can be used to perform sanity checks, ensuring that
  Cetus with subscripted subscript analysis enabled, generates the expected optimized code.
- The Cetus executable can be found in the directory *Cetus-bin*.
- Instructions on how to use this executable can be found in this github repository - 
  [The-Cetus-Project-SubSubAnalysis](https://github.com/akshay9594/The-Cetus-Project/tree/SubSub_Analysis)
- Note that only Serial Baseline source codes can be translated.