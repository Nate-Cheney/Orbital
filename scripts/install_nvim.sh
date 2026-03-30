#########################
# Neovim Setup          #
#########################

NVIM_CONFIG_DIR="$HOME/.config"
NVIM_TMP_DIR="/tmp/neovim-dotfiles"
PACKER_DIR="$HOME/.local/share/nvim/site/pack/packer/start/packer.nvim"

# 0. Install tree-sitter
ARCH=$(uname -m)
[ "$ARCH" = "x86_64" ] && TS_ARCH="x64" || TS_ARCH="arm64"
echo "Container architecture: $ARCH"

TS_VERSION=$(curl -s https://api.github.com/repos/tree-sitter/tree-sitter/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
echo "Latest tree-sitter version: $TS_VERSION"

echo "Installing tree-sitter..."
curl -L -o tree-sitter.zip "https://github.com/tree-sitter/tree-sitter/releases/download/${TS_VERSION}/tree-sitter-cli-linux-${TS_ARCH}.zip"
unzip tree-sitter.zip
chmod +x tree-sitter
sudo mv tree-sitter /usr/local/bin/
rm tree-sitter.zip
echo "Successfully installed tree-sitter"

# 1. Install packer.nvim if it doesn't exist
if [ ! -d "$PACKER_DIR" ]; then
  echo "Installing packer.nvim..."
  git clone --depth 1 https://github.com/wbthomason/packer.nvim "$PACKER_DIR"
  sleep 2
fi

# 2. Install neovim dotfiles if they don't exist
if [ -d "$NVIM_CONFIG_DIR" ]; then
    rm -rf "$NVIM_CONFIG_DIR"    
fi

echo "Cloning Neovim configuration..."
git clone https://github.com/Nate-Cheney/neovim-dotfiles.git "$NVIM_TMP_DIR"
sleep 2

echo "Syncing Neovim dotfiles..."
(cd $NVIM_TMP_DIR && ./sync-dotfiles.sh -d)
sleep 2 

echo "Cleaning Neovim tmp dir..."
rm -rf $NVIM_TMP_DIR

# 3. Install and compile plugins 
echo "Installing plugins..."
nvim --headless --noplugin \
  -c 'packadd packer.nvim' \
  -c 'luafile $HOME/.config/nvim/lua/plugins.lua' \
  -c 'autocmd User PackerComplete quitall' \
  -c 'PackerSync' || true
sleep 3

