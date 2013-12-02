# read CSV
df <- read.csv("density.csv", header=FALSE, sep=",", as.is=TRUE)

# plot data
plot(df[, 1], df[, 2], type="p", pch=19, xaxs="i", yaxs="i", ylab="Filmweb rating", xlab="IMDb rating", main="Filmweb Top 500 Movies", xlim=c(5, 10), ylim=c(7.45, 10), cex=df[, 3])

# add lines
abline(a=0, b=1, col=4, lty=3)
abline(a=-0.5, b=1, col=2, lty=3)


# add legend
legend("topleft", c("y = x", "y = x - 0.5"), col=c(4, 2), lty=c(3, 3), bty="n")