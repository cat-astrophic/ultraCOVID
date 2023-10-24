# This script runs bonus LPMs for the ultraCOVID project including gender x covid interaction models

# Loading libraries

library(stargazer)
library(lmtest)

# Project directory

xdirec <- 'D:/ultraCOVID/'

# Read in the data

snarf <- read.csv(paste0(xdirec, 'ultradata.csv'))

# Adjust the MA data

snarf$Runner_City_Cases_MA30 <- snarf$Runner_City_Cases_MA30 / 1000
snarf$Race_City_Cases_MA30 <- snarf$Race_City_Cases_MA30 / 1000

# Run LPMs

lpm11 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State + Travel_Distance
            + Ability + Total_Races + Total.Appearances + factor(RACE_Name) + factor(Gender) + Age + I(Age^2)
            + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income + Unemployment_Rate
            + Some_College_Ass + College_Degree, data = snarf)

lpm21 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State + Travel_Distance
            + Ability + Total_Races + Total.Appearances + factor(RACE_Name) + factor(Gender) + Age + I(Age^2)
            + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income + Unemployment_Rate
            + Some_College_Ass + College_Degree, data = snarf)

lpm12 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State + Travel_Distance
            + Ability + Total_Races + Total.Appearances + factor(RACE_Name) + factor(Gender) + Age + I(Age^2)
            + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income + Unemployment_Rate
            + Some_College_Ass + College_Degree, data = snarf[which(snarf$Consecutive.Appearances == 1),])

lpm22 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State + Travel_Distance
            + Ability + Total_Races + Total.Appearances + factor(RACE_Name) + factor(Gender) + Age + I(Age^2)
            + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income + Unemployment_Rate
            + Some_College_Ass + College_Degree, data = snarf[which(snarf$Consecutive.Appearances == 1),])

lpm13 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State + Travel_Distance
            + Ability + Total_Races + Total.Appearances + factor(RACE_Name) + factor(Gender) + Age + I(Age^2)
            + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income + Unemployment_Rate
            + Some_College_Ass + College_Degree, data = snarf[which(snarf$Consecutive.Appearances > 1),])

lpm23 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30 + In_State + Travel_Distance
            + Ability + Total_Races + Total.Appearances + factor(RACE_Name) + factor(Gender) + Age + I(Age^2)
            + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income + Unemployment_Rate
            + Some_College_Ass + College_Degree, data = snarf[which(snarf$Consecutive.Appearances > 1),])

lpm11x <- coeftest(lpm11, vcov. = vcovCL, cluster = ~RACE_Name)
lpm21x <- coeftest(lpm21, vcov. = vcovCL, cluster = ~RACE_Name)
lpm12x <- coeftest(lpm12, vcov. = vcovCL, cluster = ~RACE_Name)
lpm22x <- coeftest(lpm22, vcov. = vcovCL, cluster = ~RACE_Name)
lpm13x <- coeftest(lpm13, vcov. = vcovCL, cluster = ~RACE_Name)
lpm23x <- coeftest(lpm23, vcov. = vcovCL, cluster = ~RACE_Name)

stargazer(lpm11x, lpm21x, lpm12x, lpm22x, lpm13x, lpm23x, type = 'text', omit = c('RACE_Name', 'NY_RACE_Month'))

# Repeat with an interaction term


xlpm11 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30*factor(Gender) + Race_City_Cases_MA30*factor(Gender)
             + In_State + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
             + Age + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income
             + Unemployment_Rate + Some_College_Ass + College_Degree, data = snarf)

xlpm21 <- lm(Y ~ Runner_City_Cases_MA30*factor(Gender) + Race_City_Cases_MA30*factor(Gender)
             + In_State + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
             + Age + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income
             + Unemployment_Rate + Some_College_Ass + College_Degree, data = snarf)

xlpm12 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30*factor(Gender) + Race_City_Cases_MA30*factor(Gender)
             + In_State + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
             + Age + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income
             + Unemployment_Rate + Some_College_Ass + College_Degree, data = snarf[which(snarf$Consecutive.Appearances == 1),])

xlpm22 <- lm(Y ~ Runner_City_Cases_MA30*factor(Gender) + Race_City_Cases_MA30*factor(Gender)
             + In_State + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
             + Age + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income
             + Unemployment_Rate + Some_College_Ass + College_Degree, data = snarf[which(snarf$Consecutive.Appearances == 1),])

xlpm13 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30*factor(Gender) + Race_City_Cases_MA30*factor(Gender)
             + In_State + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
             + Age + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income
             + Unemployment_Rate + Some_College_Ass + College_Degree, data = snarf[which(snarf$Consecutive.Appearances > 1),])

xlpm23 <- lm(Y ~ Runner_City_Cases_MA30*factor(Gender) + Race_City_Cases_MA30*factor(Gender)
             + In_State + Travel_Distance + Ability + Total_Races + Total.Appearances + factor(RACE_Name)
             + Age + I(Age^2) + factor(NY_RACE_Month) + RACE_Finisher_Count + Median_Household_Income
             + Unemployment_Rate + Some_College_Ass + College_Degree, data = snarf[which(snarf$Consecutive.Appearances > 1),])

xlpm11x <- coeftest(xlpm11, vcov. = vcovCL, cluster = ~RACE_Name)
xlpm21x <- coeftest(xlpm21, vcov. = vcovCL, cluster = ~RACE_Name)
xlpm12x <- coeftest(xlpm12, vcov. = vcovCL, cluster = ~RACE_Name)
xlpm22x <- coeftest(xlpm22, vcov. = vcovCL, cluster = ~RACE_Name)
xlpm13x <- coeftest(xlpm13, vcov. = vcovCL, cluster = ~RACE_Name)
xlpm23x <- coeftest(xlpm23, vcov. = vcovCL, cluster = ~RACE_Name)

stargazer(xlpm11x, xlpm21x, xlpm12x, xlpm22x, xlpm13x, xlpm23x, type = 'text', omit = c('RACE_Name', 'NY_RACE_Month'))

