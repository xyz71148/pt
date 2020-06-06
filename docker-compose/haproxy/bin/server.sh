mkdir -p ~/data/projects/wwwroot
echo "bar" > ~/data/projects/wwwroot/bar.txt
cd ~/data/projects/wwwroot
python -m SimpleHTTPServer 8880
