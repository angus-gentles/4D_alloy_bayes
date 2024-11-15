#!/usr/bin/env bash
source ~/tools/setup_data_qe7.3.1.sh
cur=$(pwd)
for i in *;do 
	if [ -d "$i" ] && [ "$(basename "$i")" != "__pycache__" ] ; then 
		cd $i
		for j in *.relax.in ; do
			base="${j%.relax.in}"
			echo $base
			rm -r ./tmp/
			mpirun -n ${SLURM_NPROCS} pw.x -i ${base}.relax.in > ${base}.relax.out
			if [ -f ${base}.meff.in ]; then
				remove_wfc.sh 
				rm -r ./meff/
				cp -r ./tmp/ ./meff/
				mpirun -n ${SLURM_NPROCS} pw.x -i ${base}.meff.in > ${base}.meff.out
			fi
			remove_wfc.sh
		done
		cd $cur
	fi
done
