# Aliases

PS1='\n\h|\u: $PWD > '

HISTSIZE=5000
HISTCONTROL=ignorespace # Any lines that start with at least one space are not added to the history

# Eg. Let's say you want to re-run the last command you ran that started with 'r'. 
# You type '!r' and press 'Enter' -- however, since you don't get a chance to see what exactly that command is before it runs, if that last command was actually a destructive command, you wouldn't realize until after it was already executed!
# To prevent this, set the below binding. Now, to safely run the last command you ran that started with 'r':
# Type '!r' and then press the spacebar -- the '!r' will expand to show you what command it is. Once you're satisfied that it's the command you wanted, you can press 'Enter' to actually run it.
bind Space:magic-space

alias root='sudo -s'
alias v='vim'
alias vi='vim +startinsert' # Open file in 'insert' mode
alias vr='vim -R' # Open file in read-only mode
alias l-'ls -A'
alias 11-'ls -Al --si'
alias c='clear'
alias cl='clear && ls -A'
alias cll='clear && ls -Al --si'
#alias find='find / -iname FILENAME 2>/dev/null'
alias gdb='gdb -q' # Start GDB in quiet mode to avoid printing warranty info in beginning
alias cp='cp --preserve-mode, ownership --recursive'
alias mkdir='mkdir --parents'
alias diff='diff -s' # Explicitly tell me when there are no differences
alias p='python3'
alias zip='zip --recurse-paths'
alias gzip='gzip --keep'
alias gunzip='gunzip --keep'
alias od='od -c'
# alias grep='grep -i' # Case-insensitive
# alias grep='grep -in' # Case-insensitive and displays line number
alias grep='grep --fixed-strings' # Do NOT assume pattern is regex!
alias trunc='truncate --size 0'
alias chown='chown --recursive'
alias host='echo ${HOSTNAME}'
alias shell='echo ${SHELL}'
alias user='whoami'
alias co='command'
alias sudoe='sudo --preserve-env'
alias so='source /home/ec2-user/.bash_profile'
alias lo='logout &>/dev/null || exit &>/dev/null'

# HTTP Proxies
# alias set_proxies='export http_proxy="http://...:..." \
#                     && export https_proxy="${http_proxy}" \
#                     && EC2_METADATA_SERVICE="169.254.169.254" \
#                     && export no_proxy="localhost,${EC2_METADATA_SERVICE},test.com" \
#                     && unset HTTP_PROXY HTTPS_PROXY NO_PROXY \
#                     && env | grep -i "proxy"'
alias proxies='env | grep -i "proxy"'
alias unset_proxies='unset http_proxy https_proxy no_proxy HTTP_PROXY HTTPS_PROXY NO_PROXY'

# Docker
alias images='docker images | less'
alias containers='docker ps -a'
alias run='docker run --rm -it'

# Git
# If you're working on a branch that is NOT 'master' (eg. 'feature/test', make sure to replace every occurrence of 'master' with your branch name). 
# alias status='clear && git status'
# alias pull='clear && git pull origin master'
# alias commit='git commit -a'
# alias push='clear && git push origin master'
# alias add='clear && git commit -a && git pull origin master && git push origin master'
