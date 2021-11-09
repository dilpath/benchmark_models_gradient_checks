benchmark_dir=Benchmark-Models-PEtab/Benchmark-Models

model_names=$(find $benchmark_dir/* -maxdepth 0 -type d -printf '%f\n')

for tool_name in amici pypesto
do
	for model_name in $model_names
	do
		echo $tool_name $model_name
		sbatch submit.sh $tool_name $model_name
	done
done
