#!/bin/bash
set -e
cd /tmp/claude-0/prod/exam
mkdir -p out
: > out/list.txt
: > out/chapters.txt
T=0
declare -A NAME=([INTRO]="Introducción" [P1]="Pregunta 1: redox, pila y solubilidad" [P2B]="Pregunta 2B: configuración electrónica y espectro" [P4A]="Pregunta 4A: termoquímica y síntesis de metanol" [P4B]="Pregunta 4B: amoniaco y neutralización" [CIERRE]="Cierre")
for S in INTRO P1 P2B P4A P4B CIERRE; do
  M=p_rest; [ $S = P1 ] && M=p1
  ffmpeg -y -loglevel error -i media/videos/$M/1080p30/$S.mp4 -i clean/${S}_edit.wav -map 0:v -map 1:a -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -ar 48000 -ac 2 -shortest out/$S.mp4
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/$S.mp4)
  printf "%d:%02d %s\n" $(python3 -c "t=int($T);print(t//60,t%60)") "${NAME[$S]}" >> out/chapters.txt
  echo "file '$S.mp4'" >> out/list.txt
  T=$(python3 -c "print($T+$D)")
  echo "$S video=$(ffprobe -v error -show_entries format=duration -of csv=p=0 media/videos/$M/1080p30/$S.mp4) audio=$(ffprobe -v error -show_entries format=duration -of csv=p=0 clean/${S}_edit.wav) out=$D"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i out/list.txt -c copy -movflags +faststart out/quimica-madrid-2026-junio.mp4
ls -la out/quimica-madrid-2026-junio.mp4; cat out/chapters.txt
