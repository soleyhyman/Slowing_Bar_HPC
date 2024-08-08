DIR='./envs/slowing_bar_hpc'

check_condition() {
    if [ -d "$DIR" ]; then
        return 0  
    else
        return 1
    fi
}

# Correct syntax for the `if` statement and `-a` (AND) operator
if [ ! -d "$DIR" ] && [ "$SLURM_ARRAY_TASK_ID" -eq 0 ]; then
    echo "Setting up environment..."
    python3 -m venv "$DIR"
    source "$DIR/bin/activate"
    pip install -r ./envs/requirements.txt
else
    while true; do
        if check_condition; then
            echo "ENV Installed"
            break
        else 
            echo "ENV Installing"
        fi
        sleep 30
    done
fi

echo "Environment Setup Complete"