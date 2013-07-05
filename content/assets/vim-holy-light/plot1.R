# read CSV
df <- read.csv("data.csv", header=FALSE, sep=",", as.is=TRUE)

# treat time as time
time <- as.POSIXct(df[, 1] + 3600, origin=ISOdatetime(1970, 1, 1, 0, 0, 0))

# use light in millions
light <- df[, 2] / 1e6

# plot data
plot(time, light, type="s", ylim=c(0, 13), yaxs="i", ylab="Millions of something...", xlab="Time", main="Ambient light level measured by holylight-checker")

# add threshold
abline(h=4, col=4, lty=3)

# add legend
legend("topright", c("measurement", "threshold"), col=c(1, 4), lty=c(1, 3), bty="n")