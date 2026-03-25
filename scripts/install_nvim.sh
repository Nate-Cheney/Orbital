#!/bin/bash

# 0. Get pre-requisites
sudo apt-get install -y tree-sitter-cli

NVIM_CONFIG_DIR="$HOME/.config"
PACKER_DIR="$HOME/.local/share/nvim/site/pack/packer/start/packer.nvim"

# 1. Install packer.nvim if it doesn't exist
if [ ! -d "$PACKER_DIR" ]; then
  echo "Installing packer.nvim..."
  git clone --depth 1 https://github.com/wbthomason/packer.nvim "$PACKER_DIR"
  sleep 2
fi

# 2. Install neovim dotfiles if they don't exist
if [ ! -d "$NVIM_CONFIG_DIR" ]; then
  echo "Cloning Neovim configuration..."
  git clone https://github.com/Nate-Cheney/neovim-dotfiles.git "$NVIM_CONFIG_DIR"
  sleep 2
fi

# 3. Install and compile plugins (single pass)
echo "Installing plugins..."
nvim --headless --noplugin \
  -c 'packadd packer.nvim' \
  -c 'luafile $HOME/.config/nvim/lua/plugins.lua' \
  -c 'autocmd User PackerComplete quitall' \
  -c 'PackerSync' || true
sleep 3

