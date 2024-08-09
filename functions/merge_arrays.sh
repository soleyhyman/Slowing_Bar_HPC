job_id=$SLURM_ARRAY_JOB_ID

check_all_done() {
    # Get the list of all tasks in the array job
    tasks=$(squeue -j "$job_id" -o "%.2t %.7i" | awk '{print $2}')
    echo $tasks
    
    # Check if any tasks except index 0 are still running or pending
    for task in $tasks; do
        if [ "$task" != "0" ]; then
            task_status=$(squeue -j "$SLURM_JOB_ID" -t R,PD -o "%.2t %.7i" | awk -v id="$task" '{if ($2 == id) print $1}')
            if [[ -n "$task_status" ]]; then
                return 1 # If any other task is still running or pending, return false
            fi
        fi
    done
    return 0 # All other tasks are done
}

# Check if any tasks are still running or pending
if [ "$SLURM_ARRAY_TASK_ID" -eq 0 ]; then
    while true; do
        if check_all_done; then
            time python3 ./merge_npy.py -jd $json_dir -ar $tot_arr
        else
            sleep 60
            echo "Other jobs not done"
        fi
    done
fi