# read CSV
df <- read.csv("data.csv", header=FALSE, sep=",", as.is=TRUE)

# treat time as time
time <- as.POSIXct(df[, 1] + 3600, origin=ISOdatetime(1970, 1, 1, 0, 0, 0))

# use light in millions
light <- df[, 2] / 1e6

# plot data
plot(time, light, type="s", ylim=c(0, 13), yaxs="i", ylab="Millions of something...", xlab="Time", main="Ambient light level, last 5 and 6 digits discarded")

# discard last 5-6 digits
discarded6 <- floor(light)
discarded5 <- floor(light * 10) / 10
lines(time, discarded6, type="s", col=2)
lines(time, discarded5, type="s", col=4)

# plot errors
lines(time, abs(light - discarded6), type="s", col=2, lty=3)
lines(time, abs(light - discarded5), type="s", col=4, lty=3)

# add legend
legend("topright", c("x [millions]", "x1 = floor(x)", "x2 = floor(x * 10) / 10", "abs(x - x1)", "abs(x - x2)"), col=c(1, 2, 4, 2, 4), lty=c(1, 1, 1, 3, 3), bty="n")