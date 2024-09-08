#!/bin/bash

if ! tmux has-session -t bot 2>/dev/null; then
    tmux new-session -ds bot
fi

tmux send-keys -t bot "source venv/bin/activate" ENTER
tmux send-keys -t bot "python3 app.py" ENTER