#!/bin/bash
cd "$(dirname "$0")"; mkdir -p videos
while IFS=$'\t' read -r name url; do
  out="videos/$name.mp4"; [ -s "$out" ] && continue
  base="${url%%hls_264_master*}"; m=$(curl -s "$url")
  v=$(echo "$m" | grep -A1 'RESOLUTION=1280x720' | tail -1 | tr -d '\r')
  [ -z "$v" ] && v=$(echo "$m" | grep -A1 'EXT-X-STREAM-INF' | sed -n 2p | tr -d '\r')
  a=$(echo "$m" | grep -o 'URI="[^"]*audio[^"]*"' | head -1 | sed 's/URI="//;s/"//')
  if [ -n "$a" ]; then ffmpeg -nostdin -loglevel error -y -i "$base$v" -i "$base$a" -map 0:v -map 1:a -c copy "$out"
  else ffmpeg -nostdin -loglevel error -y -i "$base$v" -c copy "$out"; fi
  echo "done $name $(du -h "$out" | cut -f1)"
done < list.tsv
echo ALLDONE
