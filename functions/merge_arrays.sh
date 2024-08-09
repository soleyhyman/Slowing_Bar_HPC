job_id=$SLURM_ARRAY_JOB_ID

check_all_done() {
    # Get the list of all tasks in the array job
    tasks=$(squeue -r --job $job_id | awk 'NR > 1 {print $1}')
    
    # checks how many jobs are running
    num_ids=$(echo "$tasks" | wc -w)
    if [ "$num_ids" -eq 1 ]; then
        return 0 # If tasks running is 1 returns true
    else 
        return 1
    fi
}

# checks to see if there is only one node running and if so merges
if check_all_done; then
    echo "Last Node running. Will Merge."
    time python3 ./merge_npy.py -jd $json_dir -ar $tot_arr
else
    echo "Other nodes running. Last will merge."
fi
