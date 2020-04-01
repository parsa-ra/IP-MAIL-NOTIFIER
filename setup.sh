#!bin/sh

sudo cp paramailnot.cpython-37.pyc /usr/local/bin && cp paramailnot.service /etc/systemd/system && cp paramailnot.timer /etc/systemd/system && cp paramailnot.sh /usr/local/bin && systemctl enable paramailnot.timer && systemctl start paramailnot.timer

