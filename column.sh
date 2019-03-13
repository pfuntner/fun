rm -rvf ~/tmp/fifo
mkfifo ~/tmp/fifo
column < ~/tmp/fifo &
echo -e 'this is a test\nthis is not a test' > ~/tmp/fifo
wait
