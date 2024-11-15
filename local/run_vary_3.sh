#!/usr/bin/env bash
source ~/tools/setup_data_qe7.3.1.sh
cur=$(pwd)
export I_MPI_PMI_LIBRARY=/opt/sw/slurm/x86_64/alma8.8/22-05-2-1/lib/libpmi.so
list1=''
for i in *;do 
	if [ -d "$i" ] && [ "$(basename "$i")" != "__pycache__" ] ; then 
        counter=$((counter+1))
        list1=$list1"$i "
	fi
done
arr=($list1)

nodes=($(scontrol show hostname $SLURM_NODELIST))

list1_cores="32 32 32 32"
arr1_cores=(${list1_cores})
#for i in {0..7} ; do echo ${arr1_cores[i]} ; done
list1_cpu=$(../local/hexadecimal_part.py ${list1_cores})
arr1_cpu=($list1_cpu)

list2_cores="32 32 32 32"
arr2_cores=(${list2_cores})
list2_cpu=$(../local/hexadecimal_part.py ${list2_cores})
arr2_cpu=($list2_cpu)

list3_cores="64 64"
arr3_cores=(${list3_cores})
list3_cpu=$(../local/hexadecimal_part.py ${list3_cores})
arr3_cpu=($list3_cpu)

list4_cores="64 64"
arr4_cores=(${list4_cores})
list4_cpu=$(../local/hexadecimal_part.py ${list4_cores})
arr4_cpu=($list4_cpu)


counter=0

for bin in InAs GaAs ; do 
    cd $bin 
    #echo $counter
    #echo ${arr3_cores[counter]}
    for k in *.relax.in ; do 
        base="${k%.relax.in}"
        srun --nodes=1 --mpi=pmi2 -n ${arr3_cores[counter]} --overlap \
            --cpu-bind=mask_cpu:${arr3_cpu[counter]} \
            -w ${nodes[0]}\
            pw.x -ndiag 64 -i ${base}.relax.in > ${base}.relax.out &
    done
    cd $cur
    counter=$((counter+1))
done

counter=0
for bin in GaSb InSb ; do 
    cd $bin 
    #echo ${arr4_cores[counter]}
    for k in *.relax.in ; do 
        base="${k%.relax.in}"
        srun --nodes=1 --mpi=pmi2 -n ${arr4_cores[counter]} --overlap \
            --cpu-bind=mask_cpu:${arr4_cpu[counter]} \
            -w ${nodes[1]}\
            pw.x -ndiag 64 -i ${base}.relax.in > ${base}.relax.out &
    done
    cd $cur
    counter=$((counter+1))
done 
wait

counter=0
for bin in GaAs1Sb3 GaAs3Sb1 InAs1Sb3 InAs3Sb1 ; do 
    cd $bin 
    #echo ${arr1_cores[counter]}
    for k in *.relax.in ; do 
        base="${k%.relax.in}"
        srun --nodes=1 --mpi=pmi2 -n ${arr1_cores[counter]} --overlap \
            --cpu-bind=mask_cpu:${arr1_cpu[counter]} \
            -w ${nodes[0]}\
            pw.x -ndiag 25 -i ${base}.relax.in > ${base}.relax.out &
    done
    cd $cur
    counter=$((counter+1))
done

counter=0
for bin in In1Ga3As In3Ga1As In1Ga3Sb In3Ga1Sb ; do 
    cd $bin 
    #${arr2_cores[counter]} 
    for k in *.relax.in ; do 
        base="${k%.relax.in}"
        srun --nodes=1 --mpi=pmi2 -n ${arr2_cores[counter]} --overlap \
            --cpu-bind=mask_cpu:${arr2_cpu[counter]} \
            -w ${nodes[1]}\
            pw.x -ndiag 25 -i ${base}.relax.in > ${base}.relax.out &
    done
    cd $cur
    counter=$((counter+1))
done 
wait

counter=0

for bin in GaAs2Sb2 InAs2Sb2 ; do 
    cd $bin 
    for k in *.relax.in ; do 
        base="${k%.relax.in}"
        srun --nodes=1 --mpi=pmi2 -n ${arr3_cores[counter]} --overlap \
            --cpu-bind=mask_cpu:${arr3_cpu[counter]} \
            -w ${nodes[0]}\
            pw.x -ndiag 64 -i ${base}.relax.in > ${base}.relax.out &
    done
    cd $cur
    counter=$((counter+1))
done

counter=0
for bin in In2Ga2As In2Ga2Sb ; do 
    cd $bin 
    for k in *.relax.in ; do 
        base="${k%.relax.in}"
        srun --nodes=1 --mpi=pmi2 -n ${arr4_cores[counter]} --overlap \
            --cpu-bind=mask_cpu:${arr4_cpu[counter]} \
            -w ${nodes[1]}\
            pw.x -ndiag 64 -i ${base}.relax.in > ${base}.relax.out &
    done
    cd $cur
    counter=$((counter+1))
done 
wait

for i in {0..15} ; do cd ${arr[i]}
    for k in *.relax.in; do base="${k%.relax.in}" ; done
	#base="${*%.relax.in}"
    #echo $base
	remove_wfc.sh 
	if [ -f ${base}.meff.in ]; then
		rm -r ./meff/
		cp -r ./tmp/ ./meff/
		mpirun -n ${procs} pw.x -i ${base}.meff.in > ${base}.meff.out
	fi
    cd $cur
done