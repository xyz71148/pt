while [ 1 ]
do
     curl http://127.0.0.1:$PORT/check
     sleep 1
done