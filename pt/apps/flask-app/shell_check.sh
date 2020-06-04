file=$1

while [ 1 ]
do
  if test -f "$file"; then
    echo "$file exists"
    sh $file >> /tmp/shell.log
    rm -rf $file
  else
      echo "$file not exists"
  fi
  sleep 1
done