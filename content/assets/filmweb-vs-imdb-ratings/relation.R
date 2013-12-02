# read CSV
df <- read.csv("ratings.csv", header=FALSE, sep="\t", as.is=TRUE)

# get ratings
filmweb <- round(df[, 3], 1)
imdb <- df[, 4]

length(which(filmweb < imdb))
length(which(filmweb == imdb))
length(which(filmweb > imdb))