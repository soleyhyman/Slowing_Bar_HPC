DIR='./envs/slowing_bar_hpc'

check_condition() {

    if [ -d "$DIR" ]; then
        return 0  # Condition is true
    else
        return 1  # Condition is false
    fi
}

if [!(-d "$DIR") -a ($SLURM_ARRAY_TASK_ID -eq 0)]; then
    echo
    python3 -m venv $DIR
    source $ENV_DIR/bin/activate
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

echo "Enviroment Setup Complete"