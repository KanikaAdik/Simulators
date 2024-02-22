export PATH="/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin:$PATH"
pkill -9 python
pkill -9 java
sleep 5
#cd /data/vmax && /usr/bin/forever start -c python vmax.py
cd /data/BNA && /usr/bin/forever start -c python bna.py > /root/bna.log

