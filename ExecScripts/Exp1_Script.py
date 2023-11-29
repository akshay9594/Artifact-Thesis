
import matplotlib.pylab as plt

from subprocess import Popen,PIPE

import re,os,sys

import utils

#Executing the AMGmk application
def execute_amgmk(iters):
    app_times = []

    threads = 0
    for i in range(0,iters):
        exec_result = Popen('./AMGMk',stdout=PIPE,stderr=PIPE)
        output, err_val = exec_result.communicate()
                
        output = str(output,'UTF-8')
        error = str(err_val, 'UTF-8')
        if(isinstance(output,str)):
            search = re.search('Wall time =(.*)seconds.', output)
            wall_time = [float(i) for i in re.findall("\d+\.\d+", search.group(1))]
            app_times.append(wall_time.pop())


            if(i == 0):
                search = re.search('max_num_threads =(.*)', output)
                threads = [int(s) for s in re.findall(r'\b\d+\b', search.group(1))].pop()
            
    app_time_sum = 0.0
    for i in range(0,len(app_times)):
        app_time_sum += app_times[i]

    app_time_avg = app_time_sum/iters

    percent_app_time_var = utils.calculate_variation(app_times,app_time_avg)

    return (app_time_avg,percent_app_time_var,threads)


#Executing the UA application
def execute_UA(exec_path,input_class,iters):
    transf_times = []
    os.chdir(exec_path)

    exec_command = './' + 'ua.'+input_class+'.x'
    threads = 0
    for i in range(0,iters):
        exec_result = Popen(exec_command,stdout=PIPE,stderr=PIPE)
        output, err_val = exec_result.communicate()
                
        output = str(output,'UTF-8')
       
        if(isinstance(output,str)):
            search = re.search('Transf total Time=(.*)seconds', output)
            wall_time = [float(i) for i in re.findall("\d+\.\d+", search.group(1))]
            transf_times.append(wall_time.pop())

            if(i == 0):
                search = re.search('max_num_threads =(.*)', output)
                threads = [int(s) for s in re.findall(r'\b\d+\b', search.group(1))].pop()
            
    transf_time_sum = 0.0
    for i in range(0,len(transf_times)):
        transf_time_sum += transf_times[i]
   
    mean = transf_time_sum/iters

    percent_var = utils.calculate_variation(transf_times,mean)

    return (mean,percent_var,threads)


#Executing the SDDMM benchmark
def execute_Other_Benchmark(executable_path,input_path,iters,executable):
    app_times = []

    executable_path = executable_path + './' + executable

    exec_command = ''
    if(input_path == ''):
        exec_command = executable_path
    else:
        exec_command = [executable_path,input_path]

    #print(exec_command)
    for i in range(0,iters):
        exec_result = Popen(exec_command,stdout=PIPE,stderr=PIPE)
        output, err_val = exec_result.communicate()
                
        output = str(output,'UTF-8')
        error = str(err_val, 'UTF-8')
        #print(output)
        if(isinstance(output,str)):
            search = re.search('kernel=(.*) s', output)
            wall_time = [float(i) for i in re.findall("\d+\.\d+", search.group(1))]
            app_times.append(wall_time.pop())


            # if(i == 0):
            #     search = re.search('max_num_threads =(.*)', output)
            #     threads = [int(s) for s in re.findall(r'\b\d+\b', search.group(1))].pop()
            
    app_time_sum = 0.0
    for i in range(0,len(app_times)):
        app_time_sum += app_times[i]

    app_time_avg = app_time_sum/iters

    percent_app_time_var = utils.calculate_variation(app_times,app_time_avg)

    return (app_time_avg,percent_app_time_var)



#Compile the AMGmk benchmark
def compile_amgmk(base_path):
    os.chdir(base_path)
    make_result = Popen('make',stdout=PIPE,stderr=PIPE)
    output, err = make_result.communicate()
    output = str(output, 'UTF-8')
    error = str(err, 'UTF-8')

    if(('error:' in output) or ('error:' in error)):
        print("Compilation failed...")
        exit()
    return

#Compile the UA benchmark
def compile_UA(code_type,base_path,input_class):
    os.chdir(base_path)

    make_result = ''
   
    if(code_type == 'baseline'):
        make_result = Popen(['make','UA','CLASS='+input_class],stdout=PIPE,stderr=PIPE)
    elif(code_type == 'opt'):
        make_result = Popen('make',stdout=PIPE,stderr=PIPE)
    else:
        make_result = Popen('make',stdout=PIPE,stderr=PIPE)
    
    output, err = make_result.communicate()
    output = str(output, 'UTF-8')
    error = str(err, 'UTF-8')

    if(('error:' in output) or ('error:' in error)):
        print("Compilation failed...")
        print(output)
        print(error)
        exit()
    return



#Compile the SDDMM benchmark
def compile_CHOLDMOD_OR_SDDMM(base_path):
    os.chdir(base_path)
    make_result = Popen('make',stdout=PIPE,stderr=PIPE)
    output, err = make_result.communicate()
    output = str(output, 'UTF-8')
    error = str(err, 'UTF-8')

    if(('error:' in output) or ('error:' in error)):
        print("Compilation failed...")
        exit()
    return


#Special routine to compile and execute CHOLMOD (SuiteSparse)
def Compile_And_Execute_CHOLMOD(base_path,Supernodal_path,file_direc,file,path_to_input,iters,executable):

    #Path to the executable
    path_to_executable = base_path + 'Demo/'

     #Move the file into the playground
    utils.move_file(file_direc+file,Supernodal_path)

    #Compile the benchmark
    compile_CHOLDMOD_OR_SDDMM(base_path)

    #Execute the benchmark and record the time
    app_time,percent_var = execute_Other_Benchmark(path_to_executable,path_to_input,iters,executable)

    #Move the file back to its original location
    utils.move_file(Supernodal_path+file,file_direc)

    return app_time,percent_var



#Running the experiment with amgmk benchmark
def run_exp_amgmk(Exp1_directory,iters,path_to_reports_dir):

    #If the user wants to run the experiment for all the input files

    head_String = "\n===============Timing Results for the AMGmk benchmark(Average of "+ str(iters)+" runs)===============\n\n"

    with open(path_to_reports_dir+'/AMGmk.txt', 'w') as f:
        f.write(head_String)
        f.write("(a) Baseline Code : Serial Code\n")
        f.write("(b) Optimized Code : Cetus Parallel Code (with technique applied)\n")

        f.write("\n--------------------------------------------------------------------------\n")

        speedup_dict = {}
        for i in range(1,6):
            input_matrix = 'MATRIX'+ str(i)
            #Set the path of the baseline codes
            base_path = Exp1_directory +'/amgmk-v1.0/Baselines/Serial/' + input_matrix

            #Set the path of the optimized codes
            opt_code_path = Exp1_directory+'/amgmk-v1.0/Technique_Applied/' + input_matrix

            f.write(str(i) + ". Input Matrix: " + input_matrix + "\n")

            #Compile the baseline code
            compile_amgmk(base_path)
            #Execute the baseline code
            app_time,app_time_var,threads = execute_amgmk(iters)
            
            #Compile the optimized code
            compile_amgmk(opt_code_path)
            # #Execute the optimized code
            opt_app_time,opt_app_time_var,threads = execute_amgmk(iters)

            f.write("->Baseline execution time="+ str(app_time)+" s " + "(" + str(app_time_var)+" % variation)\n")
           
            f.write("->Optimized Code execution time ="+ str(opt_app_time)+" s " + "(" + str(opt_app_time_var)+" % variation)\n")

            app_speedup = app_time/opt_app_time
            f.write("->Speedup="+str(app_speedup)+"\n")

            speedup_dict[input_matrix] = app_speedup

            #Clean the object files
            os.chdir(base_path)
            Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

            os.chdir(opt_code_path)
            Popen(['make','clean'],stdout=PIPE,stderr=PIPE)


            f.write("\n-------------------------------------------------------------------------------\n")

    return speedup_dict



#Running the experiment with the UA benchmark
def run_exp_UA(Exp1_directory,iters,path_to_reports_dir):

    #If the user wants to run the experiment for all the input files

    head_String = "\n===============Timing Results for the Kernel transf NAS-UA benchmark(Average of "+ str(iters)+" runs)===============\n\n"

    input_classes = ['A', 'B', 'C'] 

    speedup_dict = {}

    with open(path_to_reports_dir+'/NAS-UA.txt', 'w') as f:
        f.write(head_String)
        f.write("(a) Baseline Code : Serial transf kernel\n")
        f.write("(b) Optimized Code : Cetus Parallel transf kernel (with technique applied)\n")

        f.write("\n--------------------------------------------------------------------------\n")


        for i in range(0,len(input_classes)):
            cl = input_classes[i]
            f.write(str(i+1)+". Input Class: "+cl+"\n")

            #Set the path of the baseline codes
            base_path = Exp1_directory +'/UA-NAS/Baselines/Serial/'

            #Compile the baseline code
            compile_UA('baseline',base_path,cl)

            #Clean the object files
            os.chdir(base_path)
            Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

            #Execute the baseline code
            exec_path = base_path + 'bin/'
            app_time, app_time_var, threads = execute_UA(exec_path,cl,iters)

            f.write("->Baseline execution time ="+ str(app_time)+" s " + "(" + str(app_time_var)+" % variation)\n")
           

            #Set the path of the optimized codes
            opt_code_path = Exp1_directory+'/UA-NAS/Technique_Applied/CLASS-' + cl

            #Compile and execute the optimized code
            compile_UA('opt',opt_code_path,cl)
            opt_app_time, opt_time_var, threads = execute_UA(opt_code_path,cl,iters)

            f.write("->Optimized Code execution time ="+ str(opt_app_time)+" s " + "(" + str(opt_time_var)+" % variation)\n")

            app_speedup = app_time/opt_app_time
            f.write("->Speedup="+str(app_speedup)+"\n")

            speedup_dict['CLASS-'+cl] = app_speedup
            #Clean the object files
            os.chdir(base_path)
            Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

            os.chdir(opt_code_path)
            Popen(['make','clean'],stdout=PIPE,stderr=PIPE)


            f.write("\n-------------------------------------------------------------------------------\n")

    return speedup_dict



#Running the experiment with the SDDMM benchmark
def run_exp_SDDMM(Exp1_directory,iters,path_to_reports_dir):

    #If the user wants to run the experiment for all the input files

    head_String = "\n===============Timing Results for the SDDMM benchmark(Average of "+ str(iters)+" runs)===============\n\n"

    #Set the path of the baseline codes
    base_path = Exp1_directory +'SDDMM/Baselines/Serial/'

    #Set the path of the optimized codes
    opt_code_path = Exp1_directory+'SDDMM/Technique_Applied/'

    input_directory = os.getcwd() +'/input_matrices/'


    #Compile the baseline code
    compile_CHOLDMOD_OR_SDDMM(base_path)

    #Compile the optimized code
    compile_CHOLDMOD_OR_SDDMM(opt_code_path)

    os.chdir(base_path)

    #List of input matrices
    input_matrices = ['gsm_106857', 'dielFilterV2clx','af_shell1','inline_1']

    # input_matrices = ['af_shell1'] 
    speedup_dict = {} 

    executable = 'sddmm'

    with open(path_to_reports_dir+'/SDDMM.txt', 'w') as f:
        f.write(head_String)
        f.write("(a) Baseline Code : Serial code\n")
        f.write("(b) Optimized Code : Cetus Parallel code (with technique applied)\n")

        f.write("\n--------------------------------------------------------------------------\n")

        # For each matrix,execute the baseline code and optimized code and calculate the speedup
        for i in range(0,len(input_matrices)):

            matrix = input_matrices[i]

            f.write(str(i+1)+". For matrix: "+ matrix+"\n")

            #Path to the input matrix
            input_path = input_directory + matrix + "/" + matrix + ".mtx"
            
            #Execute the Baseline code
            app_time, app_time_var = execute_Other_Benchmark(base_path,input_path,iters,executable)
            #Write the execution times to the output file
            f.write("->Baseline execution time ="+ str(app_time)+" s " + "(" + str(app_time_var)+" % variation)" +"\n")
            #Execute the optimized code
            opt_app_time, opt_time_var = execute_Other_Benchmark(opt_code_path,input_path,iters,executable)
            #Writ the execution time to the output file
            f.write("->Optimized Code execution time ="+ str(opt_app_time)+" s " + "(" + str(opt_time_var)+" % variation)"+"\n")
            #Calculate the speedup
            app_speedup = app_time/opt_app_time
            f.write("->Speedup="+str(app_speedup)+"\n")

            speedup_dict[matrix] = app_speedup

            f.write("\n-------------------------------------------------------------------------------\n")

        #Clean the object files
        os.chdir(base_path)
        Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

        os.chdir(opt_code_path)
        Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

    
    return speedup_dict




#CHOLMOD Supernodal within SuiteSparse handled separately
def run_SuiteSparse(benchmark,Exp1_directory,root_directory,iters,path_to_reports_dir):

    #If the user wants to run the experiment for all the input files

    head_String = "\n===============Timing Results for the "+ benchmark +" benchmark(Average of "+ str(iters)+" runs)===============\n\n"

    # Compile dependendent packages 
    SuiteSparse_path = Exp1_directory + benchmark

    #Package dependencies
    dependent_packages = ['/SuiteSparse_config/','/AMD/','/CAMD/','/COLAMD/']

    for package in dependent_packages:
        compile_CHOLDMOD_OR_SDDMM(SuiteSparse_path + package)


    #Set the path of the baseline codes
    base_path = SuiteSparse_path + '/CHOLMOD/'

    Supernodal_path = base_path + '/Supernodal/'

    file = 'cholmod_super_numeric.c'
    #Path to baselin and optimized cholmod_super_numeric files
    Baseline_file_direc = Supernodal_path + 'Baseline/'
    NewTech_CetusOut_file_direc = Supernodal_path + 'NewTech/'

    #List of input matrices
    input_matrices = ['spal_004', '12month1','TSOPF_RS_b2052_c1','TSOPF_RS_b678_c2']

    executable = 'cholmod_demo'
    benchmark_name = 'CHOLMOD\nSupernodal'
    speedup_dict = {}

    #Compile and run the baseline code
    with open(path_to_reports_dir+'/'+benchmark+'.txt', 'w') as f:
        f.write(head_String)
        f.write("(a) Baseline Code : Serial code\n")
        f.write("(b) Optimized Code : Cetus Parallel code (with the base technique applied)\n")
        f.write("                   : Cetus Parallel code (with the new technique applied)\n")

        f.write("\n--------------------------------------------------------------------------\n")

        for i in range(0,len(input_matrices)):

            input_mat = input_matrices[i]

            f.write(str(i+1)+". For matrix: "+ input_mat+"\n")

            path_to_input = root_directory + '/input_matrices/' + input_mat + '/' + input_mat + '.mtx'

            time_baseline,percent_var = Compile_And_Execute_CHOLMOD(base_path,Supernodal_path,Baseline_file_direc,  
                                                                file,path_to_input,iters,executable)

            f.write("->Baseline execution time ="+ str(time_baseline)+" s " + "(" + str(percent_var)+" % variation)\n\n")

            #Clean the object files
            os.chdir(base_path)
            Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

            #Clean the object files
            os.chdir(base_path)
            Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

            #Purge the executables from the Demo directory
            os.chdir(base_path+"Demo/")
            Popen(['make','purge'],stdout=PIPE,stderr=PIPE)

            #determine execution time and speedup of the Cetus parallel code with the New Technique of this paper applied
            NewOptCode_time, percent_var = Compile_And_Execute_CHOLMOD(base_path,Supernodal_path,NewTech_CetusOut_file_direc,
                                                                        file,path_to_input,iters,executable)

            f.write("Optimized Code execution time ="+ str(NewOptCode_time)+" s " + "(" + str(percent_var)+" % variation)\n")

            New_Tech_speedup = time_baseline/NewOptCode_time
            f.write("->Speedup="+str(New_Tech_speedup)+"\n")

            #Clean the object files
            os.chdir(base_path)
            Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

            #Purge the executables from the Demo directory
            os.chdir(base_path+"Demo/")
            Popen(['make','purge'],stdout=PIPE,stderr=PIPE)

            f.write("\n-------------------------------------------------------------------------------\n")

            speedup_dict[input_mat] = New_Tech_speedup

    #Clean object files of dependent pacakges

    for package in dependent_packages:
        os.chdir(SuiteSparse_path+package)
        Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

    #Clean the executables in the CHOLMOD directory
    os.chdir(base_path)
    Popen(['make','clean'],stdout=PIPE,stderr=PIPE)

    #Purge the executables from the Demo directory
    os.chdir(base_path+"Demo/")
    Popen(['make','purge'],stdout=PIPE,stderr=PIPE)

    return speedup_dict



#Call specific subroutines that execute the benchmarks
def run_benchmark(benchmark,Exp1_directory,root_directory,iters,path_to_reports_dir):

    speedup_dict = {}
    xlabel = ''
    plot_title = ' '
    if(benchmark == 'AMGmk'):
        speedup_dict = run_exp_amgmk(Exp1_directory,iters,path_to_reports_dir)
        plot_title = "Performance improvement of the AMGMk benchmark"
        xlabel = "Input Matrices"

    elif(benchmark == 'UA-NAS'):
        
        speedup_dict = run_exp_UA(Exp1_directory,iters,path_to_reports_dir)
        plot_title = "Performance improvement of the UA benchmark"
        xlabel = "Input Class"

    elif(benchmark == 'SDDMM'):
        speedup_dict = run_exp_SDDMM(Exp1_directory,iters,path_to_reports_dir)
        xlabel = "Input Matrices"
        plot_title = "Performance improvement of the SDDMM benchmark"
    
    elif(benchmark == 'SuiteSparse'):
        speedup_dict = run_SuiteSparse(benchmark,Exp1_directory,root_directory,iters,path_to_reports_dir)
        xlabel = "Input Matrices"
        plot_title = "Performance improvement of the CHOLMOD Supernodal benchmark"

    else:
        print("Benchmark not supported")
        sys.exit()

    
    return speedup_dict,plot_title,xlabel


#Run the main experiment
def RunExp(root_directory):

    iters =  3

    Exp1_directory = root_directory + '/Experiment_1/'

    list_benchmarks = ['AMGmk','UA-NAS', 'SDDMM','SuiteSparse']

    #Some plot parameters
    path_o_graphs_dir = root_directory + '/Graphs/Exp-1/'
    plot_colors = ['Red','Blue','Green','Black']
    ylabel="Performance Improvement"

    for i in range(0,len(list_benchmarks)):

        benchmark = list_benchmarks[i]

        print(str(i+1) + "." , "For Benchmark:", benchmark)

        path_to_reports_dir = os.getcwd() + '/Reports/Experiment_1/' + benchmark

        if(os.path.exists(path_to_reports_dir) == False):
            os.mkdir(path_to_reports_dir)

        speedup_dict,plot_title,xlabel = run_benchmark(benchmark,Exp1_directory,root_directory,iters,path_to_reports_dir)

        os.chdir(root_directory)

        #Plot the speedup data. Graph saved in the Graphs/Exp-1 directory with the benchmark name.
        utils.plot_data_Exp1(benchmark,speedup_dict,plot_title,xlabel,ylabel,path_o_graphs_dir,plot_colors[i])



    return