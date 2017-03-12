#!/usr/bin/env bash
set -e
set -o verbose

for path in .vimrc .vim .env .gitconfig; do
	echo $path;
	if [ ! -h ~/$path ]; then
		ln -vis ~/.dotfiles/$path ~/$path
	fi
done

echo "Deploy done"