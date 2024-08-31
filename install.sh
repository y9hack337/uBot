#!/bin/bash

# if you have errors, use manual installation

runin() {
	     { "$@" 2>>../ubot-install.log || return $?; } | while read -r line; do
		   printf "%s\n" "$line" >>../ubot-install.log
	     done
}
runout() {
	     { "$@" 2>>ubot-install.log || return $?; } | while read -r line; do
		   printf "%s\n" "$line" >>ubot-install.log
	done
}

errorin() {
	     cat ../ubot-install.log
}
errorout() {
	     cat ubot-install.log
}

SUDO_CMD=""
if [ ! x"$SUDO_USER" = x"" ]; then
	     if command -v sudo >/dev/null; then
		          SUDO_CMD="sudo -u $SUDO_USER "
	     fi
fi

###########################################

clear
clear

printf "\n                "
printf "\n █ █ █▀▄ █▀█ ▀█▀"
printf "\n █ █ █▀▄ █ █  █ "
printf "\n ▀▀▀ ▀▀  ▀▀▀  ▀ "
printf "\n\n Installing...\n\n"

###########################################

touch ubot-install.log
if [ ! x"$SUDO_USER" = x"" ]; then
	     chown "$SUDO_USER:" ubot-install.log
fi

echo "Installing..." >ubot-install.log

${SUDO_CMD}rm -rf uBot
runout ${SUDO_CMD}git clone https://github.com/y9hack337/uBot || {
	     errorout "Clone failed."
	     exit 3
}

cd uBot || {
	     printf "Install git and restart installer"
	     exit 7
}

printf "\rRepo cloned!"
printf "\n\rInstalling python dependencies...\n"

runin ${SUDO_CMD}python3 -m pip install -r requirements.txt || {
	     errorin "Requirements failed!"
	     exit 4
}

rm -f ../ubot-install.log

printf "\nDependencies installed!"
printf "\n\rStarting uBot...\n"

${SUDO_CMD}bash api_change.sh

${SUDO_CMD}python3 bot.py || {
	printf "Python script failed"
	exit 5
}
