job_id=$SLURM_ARRAY_JOB_ID

check_all_done() {
    # Get the list of all tasks in the array job
    tasks=$(squeue -r --job $job_id | awk 'NR > 1 {print $1}')
    
    # Check if any tasks except index 0 are still running or pending
    num_ids=$(echo "$tasks" | wc -w)
    if [ "$num_ids" -eq 1 ]; then
        return 0 # If any other task is still running or pending, return false
    else 
        return 1
    fi
}

# Check if any tasks are still running or pending
if [ "$SLURM_ARRAY_TASK_ID" -eq 0 ]; then
    while true; do
        if check_all_done; then
            time python3 ./merge_npy.py -jd $json_dir -ar $tot_arr
            break
        else
            sleep 60
            echo "Other jobs not done"
        fi
    done
fi