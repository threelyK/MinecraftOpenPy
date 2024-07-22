#!/bin/bash

if ! tmux has-session -t discord 2>/dev/null; then
    tmux new-session -ds discord
fi

tmux send-keys -t discord "source .venv/bin/activate" ENTER
tmux send-keys -t discord "python3 app.py" ENTER