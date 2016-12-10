ffmpeg -i x.mp4 -vf fps=20,scale=320:-1:flags=lanczos,palettegen palette.png
ffmpeg -i x.mp4 -i palette.png -filter_complex "fps=20,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
