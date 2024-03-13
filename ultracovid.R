# This script runs regression for the ultraCOVID project

# Loading libraries

library(lmtest)
library(margins)
library(sandwich)
library(stargazer)

# Project directory

direc <- 'D:/ultraCOVID/'

# Read in the data

ud <- read.csv(paste0(direc, 'ultradata.csv'))

# Adjust the COVID data by a factor of 1000 so that the point estimate is legible

ud$Runner_City_Cases_MA30 <- ud$Runner_City_Cases_MA30 / 1000
ud$Race_City_Cases_MA30 <- ud$Race_City_Cases_MA30 / 1000

# Running the regressions

m1 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud)

m2 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud)

m3 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud[which(ud$Consecutive.Appearances == 1),])

m4 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud[which(ud$Consecutive.Appearances == 1),])

m5 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud[which(ud$Consecutive.Appearances > 1),])

m6 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud[which(ud$Consecutive.Appearances > 1),])

n1 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30_PC + Race_City_Cases_MA30_PC + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud)

n2 <- glm(Y ~ Runner_City_Cases_MA30_PC + Race_City_Cases_MA30_PC + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud)

n3 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30_PC + Race_City_Cases_MA30_PC + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud[which(ud$Consecutive.Appearances == 1),])

n4 <- glm(Y ~ Runner_City_Cases_MA30_PC + Race_City_Cases_MA30_PC + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud[which(ud$Consecutive.Appearances == 1),])

n5 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30_PC + Race_City_Cases_MA30_PC + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit),  data = ud[which(ud$Consecutive.Appearances > 1),])

n6 <- glm(Y ~ Runner_City_Cases_MA30_PC + Race_City_Cases_MA30_PC + In_State
          + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age  + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
          family = binomial(link = logit), data = ud[which(ud$Consecutive.Appearances > 1),])

# Robust standard errors

m1x <- coeftest(m1, vcov = vcovCL(m1, type = 'HC1'))
m2x <- coeftest(m2, vcov = vcovCL(m2, type = 'HC1'))
m3x <- coeftest(m3, vcov = vcovCL(m3, type = 'HC1'))
m4x <- coeftest(m4, vcov = vcovCL(m4, type = 'HC1'))
m5x <- coeftest(m5, vcov = vcovCL(m5, type = 'HC1'))
m6x <- coeftest(m6, vcov = vcovCL(m6, type = 'HC1'))

n1x <- coeftest(n1, vcov = vcovCL(n1, type = 'HC1'))
n2x <- coeftest(n2, vcov = vcovCL(n2, type = 'HC1'))
n3x <- coeftest(n3, vcov = vcovCL(n3, type = 'HC1'))
n4x <- coeftest(n4, vcov = vcovCL(n4, type = 'HC1'))
n5x <- coeftest(n5, vcov = vcovCL(n5, type = 'HC1'))
n6x <- coeftest(n6, vcov = vcovCL(n6, type = 'HC1'))

# A quick stargazer check

stargazer(m1, m2, m3, m4, m5, m6, type = 'text', omit = c('RACE_Name'))
stargazer(n1, n2, n3, n4, n5, n6, type = 'text', omit = c('RACE_Name'))

stargazer(m1x, m2x, m3x, m4x, m5x, m6x, type = 'text', omit = c('RACE_Name'))
stargazer(n1x, n2x, n3x, n4x, n5x, n6x, type = 'text', omit = c('RACE_Name'))

# Margins

marm1 <- margins(m1)
marm2 <- margins(m2)
marm3 <- margins(m3)
marm4 <- margins(m4)
marm5 <- margins(m5)
marm6 <- margins(m6)

marn1 <- margins(n1)
marn2 <- margins(n2)
marn3 <- margins(n3)
marn4 <- margins(n4)
marn5 <- margins(n5)
marn6 <- margins(n6)

write.csv(summary(marm1), paste0(direc, 'margins_1.txt'), row.names = FALSE)
write.csv(summary(marm2), paste0(direc, 'margins_2.txt'), row.names = FALSE)
write.csv(summary(marm3), paste0(direc, 'margins_3.txt'), row.names = FALSE)
write.csv(summary(marm4), paste0(direc, 'margins_4.txt'), row.names = FALSE)
write.csv(summary(marm5), paste0(direc, 'margins_5.txt'), row.names = FALSE)
write.csv(summary(marm6), paste0(direc, 'margins_6.txt'), row.names = FALSE)

write.csv(summary(marn1), paste0(direc, 'margins_pc_1.txt'), row.names = FALSE)
write.csv(summary(marn2), paste0(direc, 'margins_pc_2.txt'), row.names = FALSE)
write.csv(summary(marn3), paste0(direc, 'margins_pc_3.txt'), row.names = FALSE)
write.csv(summary(marn4), paste0(direc, 'margins_pc_4.txt'), row.names = FALSE)
write.csv(summary(marn5), paste0(direc, 'margins_pc_5.txt'), row.names = FALSE)
write.csv(summary(marn6), paste0(direc, 'margins_pc_6.txt'), row.names = FALSE)

