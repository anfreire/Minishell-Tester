#!/bin/bash

write() {
    message=$1
    echo -n $message | awk '{for(i=1;i<=length;i++) {printf "%s",substr($0,i,1); fflush(); system("sleep 0.1")}}'
    echo ""
}


install_library(){
	python3 -m venv Minienv	> /dev/null 2>&1
	source Minienv/bin/activate	> /dev/null 2>&1
    Minienv/bin/pip install --quiet subprocess > /dev/null 2>&1
}

display_message(){
	clear	2< /dev/null
	clear	2< /dev/null
	echo	2< /dev/null
	write "$(tput setaf 2)\033[1m MINISHELL TESTER \033[0m$(tput sgr0)"	2< /dev/null
	echo	2< /dev/null
	echo	2< /dev/null
	write "$(tput setaf 2)\033[1mSetting up a virtual environment and installing Python libraries ...\033[0m$(tput sgr0)"	2< /dev/null
}

display_message & install_library & wait
chmod 777 $(pwd)/../minishell	2< /dev/null
chmod +x $(pwd)/tester.py	2< /dev/null
chmod 777 $(pwd)/tester.py	2< /dev/null
python3 tester.py
