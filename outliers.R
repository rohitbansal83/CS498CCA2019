library(tidyverse)
library(MASS)

# Unproccessed Cleveland Data
colNames <- c("age", "sex", "cp", "trestbps", "chol","fbs", "restecg", "thalach", "exang","oldpeak", "slope", "ca", "thal", "num")
data <- data.frame(read.table("pre_cleveland.txt", col.names = colNames, header=FALSE, sep =" "))
cleveland.lm <- lm(num ~ age + sex + cp + trestbps + chol + fbs + restecg + thalach + exang + oldpeak + slope + ca + thal, data=data)
plot(cleveland.lm, which=5, id.n = 297)
abline(2,0, lty=4, col = 59 )
abline(-2,0, lty=4, col = 59 )
summary(cleveland.lm)

# Proccessed Cleveland Data
data <- data.frame(read.table("cleveland_data.txt", col.names = colNames, header=FALSE, sep =" "))
cleveland.lm <- lm(num ~ age + sex + cp + trestbps + chol + fbs + restecg + thalach + exang + oldpeak + slope + ca + thal, data=data)
plot(cleveland.lm, which=5, id.n = 290)
abline(2,0, lty=4, col = 59 )
abline(-2,0, lty=4, col = 59 )
summary(cleveland.lm)

# Unproccessed Combined Data
colNames <- c("age", "sex", "cp","restecg", "thalach", "exang", "set_id", "num")
data <- data.frame(read.table("pre_combined.txt", col.names = colNames, header=FALSE, sep =" "))
combined <- lm(num ~ age + sex + cp + restecg + thalach + exang + set_id, data=data)
plot(combined, which=5, id.n = 20)
abline(2,0, lty=4, col = 59 )
abline(-2,0, lty=4, col = 59 )
summary(combined)

# Proccessed Combined Data
data <- data.frame(read.table("combined_data.txt", col.names = colNames, header=FALSE, sep =" "))
combined <- lm(num ~ age + sex + cp + restecg + thalach + exang + set_id, data=data)
plot(combined, which=5, id.n = 20)
abline(2,0, lty=4, col = 59 )
abline(-2,0, lty=4, col = 59 )
summary(combined)

