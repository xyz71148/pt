## docker

cmd

	docker run -it -e SERVER_START=1 \
      -e CMD_1="ls -al /data" \
      -e BOOTS=lab \
      -e PIPS=flask \
      -v "$PWD":/data \
      -p 10000:8020 \
      sanfun-docker.pkg.coding.net/utils/public/jupyterlab:v_98