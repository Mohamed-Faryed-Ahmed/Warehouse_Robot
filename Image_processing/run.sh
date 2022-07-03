#!/bin/bash

cd line_follower && python3 main.py > ../line.txt &
cd ~/Desktop/Image_processing/ && python3 QR-Angle-Calculator/main.py > qr-angle.txt


