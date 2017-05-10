args <- commandArgs(trailingOnly = TRUE)
xyz <- read.csv(file=args[1])
pdf(args[2])
scatterplot3d::scatterplot3d(xyz, color="blue", pch=19, xlab="Statistical Distance", ylab="Sample Size", zlab="Match Percentage", type="h")
