#!/usr/bin/env bash
set -e

# Regular dotfiles .vimrc, etc
DOTFILES="  .vimrc
	    .vim
	    .zshrc
	    .zshenv
	    .zsh
	    .vsvimrc
	    .tmux.conf
	    .tmux
	    .gitconfig
	    .gdbinit
	    .lldbinit
	    .gitignore
	    .ledgerrc"

# Configuration file in .config
CONFFILES=" mpv
	    nvim"

for path in $DOTFILES; do
      echo $path;
      if [ ! -h ~/$path ]; then
	    ln -vis ~/.dotfiles/$path ~/$path
      fi
done

mkdir -p ~/.config

for path in $CONFFILES; do
      echo .config/$path;
      if [ ! -h ~/.config/$path ]; then
	    ln -vis ~/.dotfiles/.config/$path ~/.config/$path
      fi
done

mkdir -p ~/.vim/tmp/{backup,swap}

echo "Deploy done"
