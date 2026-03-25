#!/bin/bash

# Enable mouse support 
if ! grep -q "set -g mouse on" "$HOME/.tmux.conf" 2>/dev/null; then
  echo "Enabling Tmux mouse mode..."
  echo "set -g mouse on" >> "$HOME/.tmux.conf"
fi

