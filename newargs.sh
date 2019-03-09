function seeargs {
  echo -n '['
  pos=1
  while [ $pos -le $# ]
  do
    if [ $pos -gt 1 ]
    then
      echo -n ', '
    fi
    echo -n "'${!pos}'"
    let 'pos=pos+1'
  done
  echo ']'
}

seeargs "$@"
set -- -v -la foo\ bar 
seeargs "$@"
