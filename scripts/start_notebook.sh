export XDG_RUNTIME_DIR=""
export ipnport=$(shuf -i8000-9999 -n1)
export ipnip=$(hostname -i | xargs)

echo -e "
        Copy/Paste this in your local terminal to ssh tunnel with remote
        -----------------------------------------------------------------
        sshuttle -r $USER@graham.computecanada.ca -v $ipnip/24
        -----------------------------------------------------------------

        Then open a browser on your local machine to the following address
        ------------------------------------------------------------------
        http://$ipnip:$ipnport (prefix w/ https:// if using password)
        ------------------------------------------------------------------
        "a
jupyter-notebook --no-browser --port=$ipnport --ip=$ipnip
