VIDEO_DIR=/home/ncoghlan/fedoradevel/_misc
OGV_NAME=$VIDEO_DIR/screencast-$1.ogv
MP4_NAME=$VIDEO_DIR/screencast-$1.mp4

recordmydesktop -o $OGV_NAME --fps 15 -x 3000 -y 100 --width 1920 --height 1080 --channels 1 --freq 22050 --v_quality 63 --s_quality 10 --workdir /tmp
ffmpeg -i $OGV_NAME $MP4_NAME
