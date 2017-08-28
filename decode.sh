# Upload
set -e
/root/Android/Sdk/platform-tools/adb push /root/Workspace/Which/cloudpets/audio/$1.au /data/data/com.termux/files/home/clbt/$1.au
/root/Android/Sdk/platform-tools/adb shell "/data/data/com.termux/files/home/bin/termux-shell.sh" "$1"
/root/Android/Sdk/platform-tools/adb pull /data/data/com.termux/files/home/clbt/$1.wav /root/Workspace/Which/cloudpets/audio/$1.wav
/root/Android/Sdk/platform-tools/adb shell "rm /data/data/com.termux/files/home/clbt/$1.*"
rm /root/Workspace/Which/cloudpets/audio/$1.au
