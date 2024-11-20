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

list1_cores="4 12 36 12 4 12 12 36"
arr1_cores=(${list1_cores})
for i in {0..7} ; do echo ${arr1_cores[i]} ; done
list1_cpu=$(../local/hexadecimal_part.py ${list1_cores})
arr1_cpu=($list1_cpu)
list1_ndim="4 9 36 9 4 9 9 36"
arr1_ndim=(${list1_ndim})

list2_cores="36 12 12 4 12 36 12 4"
arr2_cores=(${list2_cores})
list2_cpu=$(../local/hexadecimal_part.py ${list2_cores})
arr2_cpu=($list2_cpu)
list2_ndim="36 9 9 4 9 36 9 4"
arr2_ndim=(${list2_ndim})

for i in {0..7}; do cd ${arr[i]}
    for k in *.relax.in ; do 
        base="${k%.relax.in}"
        srun --nodes=1 --mpi=pmi2 -n ${arr1_cores[i]} --overlap \
            --cpu-bind=mask_cpu:${arr1_cpu[i]} -w ${nodes[0]}\
            pw.x -i ${base}.relax.in > ${base}.relax.out &
            #pw.x -ndiag ${arr1_ndim[i]} -i ${base}.relax.in > ${base}.relax.out &
    done
    cd $cur
done
for i in {8..15}; do cd ${arr[i]}
    j=$((i-8))
    for k in *.relax.in ; do
        base="${k%.relax.in}"
        srun --nodes=1 --mpi=pmi2 -n ${arr2_cores[j]} --overlap \
            --cpu-bind=mask_cpu:${arr2_cpu[j]} -w ${nodes[1]}\
            pw.x -i ${base}.relax.in > ${base}.relax.out &
            #pw.x -ndiag ${arr2_ndim[j]} -i ${base}.relax.in > ${base}.relax.out &
    done
    cd $cur
done
wait
procs=16
for i in {0..15} ; do cd ${arr[i]}
    for k in *.relax.in; do base="${k%.relax.in}" ; done
	#base="${*%.relax.in}"
    echo $base
	remove_wfc.sh 
	if [ -f ${base}.meff.in ]; then
		rm -r ./meff/
		cp -r ./tmp/ ./meff/
		mpirun -n ${procs} pw.x -i ${base}.meff.in > ${base}.meff.out
	fi
    cd $cur
done
wait