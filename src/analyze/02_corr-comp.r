rm(list = ls()) # clean workspace
library(wCorr) # install.packages("wCorr")

# configuration
setwd('/home/<username>/PSMA/src/analyze/') # add username
datasets <- list("rockyou", "linkedin", "000webhost")
scenarios <- list("online", "offline")
meters <- list("zxcvbn_guess_number", "zxcvbn_score")
methods = c("wspearman") # recommended

# Loop
for (meter in meters) {
    for (s in scenarios) {
        for (d in datasets) {
            # read prepared data from disk
            merged <- read.delim(paste("result_",d,"_",s,".csv",sep = ""), header = TRUE, quote = "")
            reference = merged$strength # used as reference
            weight    = merged$weight   # used as weight
            cat(meter, "\t")
            SAM = merged[, meter]
            for (method in methods) {
                if (method == "wspearman") {
                    C = weightedCorr(reference, SAM, method = "spearman", weights = weight)
                } else{
                    C = -20
                }
                cat(d, "\t", s, "\t", format(round(C, digits = 3), nsmall= 3)) # output to stdout
            }
            cat("\n")
        }
    }
}
# -1.0 means strong negative correlation; meter works but 'strong' passwords are in fact 'weak' and the other way round
#  0.0 means no correlation; meter is randomly guessing, and not estimating password strength
#  1.0 means strong positive correlation; meter works perfectly