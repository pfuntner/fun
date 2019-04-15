iteration=0
while [ $iteration -lt 1000000 ]
do
  echo $iteration
  let 'iteration=iteration+1'
done
