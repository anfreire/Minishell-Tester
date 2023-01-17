#!/bin/bash

chmod 777 $(pwd)/converter.sh	2< /dev/null
write() {
    message=$1
    echo -n $message | awk '{for(i=1;i<=length;i++) {printf "%s",substr($0,i,1); fflush(); system("sleep 0.1")}}'
    echo ""
}
clear	2< /dev/null
echo	2< /dev/null
write "$(tput setaf 2)\033[1m MINISHELL TESTER \033[0m$(tput sgr0)"	2< /dev/null
prompt_user() {
  echo "\nPlease select an option:\n"
  echo "\n1) Brute force the commands into minishell\n"
  echo "\n2) Run the tester\n"
  read -p "Enter your choice: " user_input
  case $user_input in
    1)
      bash ./.converter.sh
	  gnome-terminal -- bash -c "$(pwd)/../minishell < commands_only.txt; exec bash"
      ;;
    2)
      	display_message & install_library & wait
		chmod 777 $(pwd)/../minishell	2< /dev/null
		chmod +x $(pwd)/tester.py	2< /dev/null
		chmod 777 $(pwd)/tester.py	2< /dev/null
		python3 tester.py
      ;;
    *)
      echo "Invalid choice. Please select a valid option."
      ;;
  esac
}

prompt_user

install_library(){
	python3 -m venv Minienv	> /dev/null 2>&1
	source Minienv/bin/activate	> /dev/null 2>&1
    Minienv/bin/pip install --quiet subprocess > /dev/null 2>&1
}

display_message(){
	clear	2< /dev/null
	echo	2< /dev/null
	echo	2< /dev/null
	write "$(tput setaf 2)\033[1mSetting up a virtual environment and installing Python libraries ...\033[0m$(tput sgr0)"	2< /dev/null
}

