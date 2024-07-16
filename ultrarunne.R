# This script does the econometrics for the ultraCOVID project

# Loading libraries

library(stargazer)
library(dplyr)
library(sandwich)
library(miceadds)
library(lmtest)
library(multiwayvcov)
library(margins)
library(mfx)
library(ggplot2)
library(maps)
library(sf)
library(tmap)
library(socviz)
library(lme4)

# Specifying project directory

direc <- 'D:/ultraCOVID/'

# Reading in the data

ultradata <- read.csv(paste0(direc, 'ultradata.csv'))

# Creating and age squared variable

ultradata$Age2 <- ultradata$Age * ultradata$Age

# Summary stats for runner level data

write.csv(stargazer(ultradata, summary.stat = c('n', 'mean', 'sd', 'min', 'max')),
          paste('D:/ultraCOVID/summary_stats_runner.txt', sep = ''), row.names = FALSE)

# Dividing covid data through by 1000 for easier reporting of regression coefficients

ultradata$Runner_City_Cases_MA7 <- ultradata$Runner_City_Cases_MA7 / 1000
ultradata$Runner_City_Cases_MA14 <- ultradata$Runner_City_Cases_MA14 / 1000
ultradata$Runner_City_Cases_MA30 <- ultradata$Runner_City_Cases_MA30 / 1000
ultradata$Runner_State_Cases_MA7 <- ultradata$Runner_State_Cases_MA7 / 1000
ultradata$Runner_State_Cases_MA14 <- ultradata$Runner_State_Cases_MA14 / 1000
ultradata$Runner_State_Cases_MA30 <- ultradata$Runner_State_Cases_MA30 / 1000

ultradata$Race_City_Cases_MA7 <- ultradata$Race_City_Cases_MA7 / 1000
ultradata$Race_City_Cases_MA14 <- ultradata$Race_City_Cases_MA14 / 1000
ultradata$Race_City_Cases_MA30 <- ultradata$Race_City_Cases_MA30 / 1000
ultradata$Race_State_Cases_MA7 <- ultradata$Race_State_Cases_MA7 / 1000
ultradata$Race_State_Cases_MA14 <- ultradata$Race_State_Cases_MA14 / 1000
ultradata$Race_State_Cases_MA30 <- ultradata$Race_State_Cases_MA30 / 1000

# Creating the baseline data set

ud <- ultradata[which(ultradata$Race_Held_Next_Year == 1),]

# Running LPMs for starters

m1 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
         + In_State + Travel_Distance + Ability + Total_Races
         + Total.Appearances + factor(RACE_Name)
         + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
         + Median_Household_Income + Unemployment_Rate + Some_College_Ass
         + College_Degree, data = ud)

cl.cov1 <- cluster.vcov(m1, ud$RACE_Name) # cluster-robust SEs
cl.robust.se.1 <- sqrt(diag(cl.cov1))

m2 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
         + In_State + Travel_Distance + Ability + Total_Races
         + Total.Appearances + factor(RACE_Name)
         + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
         + Median_Household_Income + Unemployment_Rate + Some_College_Ass
         + College_Degree, data = ultradata)

cl.cov2 <- cluster.vcov(m2, ultradata$RACE_Name) # cluster-robust SEs
cl.robust.se.2 <- sqrt(diag(cl.cov2))

# Looking at only people who ran consecutive race before covid

UD1 <- ultradata[which(ultradata$Consecutive.Appearances == 1), ]
ud1 <- ud[which(ud$Consecutive.Appearances == 1), ]

m11 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races 
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud1)

cl.cov11 <- cluster.vcov(m11, ud1$RACE_Name) # cluster-robust SEs
cl.robust.se.11 <- sqrt(diag(cl.cov11))

m12 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races 
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = UD1)

cl.cov12 <- cluster.vcov(m12, UD1$RACE_Name) # cluster-robust SEs
cl.robust.se.12 <- sqrt(diag(cl.cov12))

# Looking at people who ran more than once in a row before covid

UD2 <- ultradata[which(ultradata$Consecutive.Appearances != 1), ]
ud2 <- ud[which(ud$Consecutive.Appearances != 1), ]

m21 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races 
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud2)

cl.cov21 <- cluster.vcov(m21, ud2$RACE_Name) # cluster-robust SEs
cl.robust.se.21 <- sqrt(diag(cl.cov21))

m22 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races 
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = UD2)

cl.cov22 <- cluster.vcov(m22, UD2$RACE_Name) # cluster-robust SEs
cl.robust.se.22 <- sqrt(diag(cl.cov22))

stargazer(m1, m2, m11, m12, m21, m22,
          se = list(cl.robust.se.1, cl.robust.se.2, cl.robust.se.11, cl.robust.se.12, cl.robust.se.21, cl.robust.se.22), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

# Repeating above models with an Age^2 variable

# Running LPMs for starters

m01 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud)

cl.cov01 <- cluster.vcov(m01, ud$RACE_Name) # cluster-robust SEs
cl.robust.se.01 <- sqrt(diag(cl.cov01))

m02 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ultradata)

cl.cov02 <- cluster.vcov(m02, ultradata$RACE_Name) # cluster-robust SEs
cl.robust.se.02 <- sqrt(diag(cl.cov02))

# Looking at only people who ran consecutive race before covid

m011 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud1)

cl.cov011 <- cluster.vcov(m011, ud1$RACE_Name) # cluster-robust SEs
cl.robust.se.011 <- sqrt(diag(cl.cov011))

m012 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = UD1)

cl.cov012 <- cluster.vcov(m012, UD1$RACE_Name) # cluster-robust SEs
cl.robust.se.012 <- sqrt(diag(cl.cov012))

# Looking at people who ran more than once in a row before covid

m021 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud2)

cl.cov021 <- cluster.vcov(m021, ud2$RACE_Name) # cluster-robust SEs
cl.robust.se.021 <- sqrt(diag(cl.cov021))

m022 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = UD2)

cl.cov022 <- cluster.vcov(m022, UD2$RACE_Name) # cluster-robust SEs
cl.robust.se.022 <- sqrt(diag(cl.cov022))

stargazer(m01, m02, m011, m012, m021, m022,
          se = list(cl.robust.se.01, cl.robust.se.02, cl.robust.se.011, cl.robust.se.012, cl.robust.se.021, cl.robust.se.022), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

write.csv(stargazer(m01, m02, m011, m012, m021, m022,
                    se = list(cl.robust.se.01, cl.robust.se.02, cl.robust.se.011, cl.robust.se.012, cl.robust.se.021, cl.robust.se.022), 
                    omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month')),
          paste('D:/ultraCOVID/lpm_results.txt', sep = ''), row.names = FALSE)

# Repeating the above with logit models

l1 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud, family = binomial(link = 'logit'))

ccl.cov1 <- cluster.vcov(l1, ud$RACE_Name) # cluster-robust SEs
ccl.robust.se.1 <- sqrt(diag(ccl.cov1))

l2 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ultradata, family = binomial(link = 'logit'))

ccl.cov2 <- cluster.vcov(l2, ultradata$RACE_Name) # cluster-robust SEs
ccl.robust.se.2 <- sqrt(diag(ccl.cov2))

# Looking at only people who ran consecutive race before covid

UD1 <- ultradata[which(ultradata$Consecutive.Appearances == 1), ]
ud1 <- ud[which(ud$Consecutive.Appearances == 1), ]

l11 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud1, family = binomial(link = 'logit'))

ccl.cov11 <- cluster.vcov(l11, ud1$RACE_Name) # cluster-robust SEs
ccl.robust.se.11 <- sqrt(diag(ccl.cov11))

l12 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = UD1, family = binomial(link = 'logit'))

ccl.cov12 <- cluster.vcov(l12, UD1$RACE_Name) # cluster-robust SEs
ccl.robust.se.12 <- sqrt(diag(ccl.cov12))

# Looking at people who ran more than once in a row before covid

UD2 <- ultradata[which(ultradata$Consecutive.Appearances != 1), ]
ud2 <- ud[which(ud$Consecutive.Appearances != 1), ]

l21 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud2, family = binomial(link = 'logit'))

ccl.cov21 <- cluster.vcov(l21, ud2$RACE_Name) # cluster-robust SEs
ccl.robust.se.21 <- sqrt(diag(ccl.cov21))

l22 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = UD2, family = binomial(link = 'logit'))

ccl.cov22 <- cluster.vcov(l22, UD2$RACE_Name) # cluster-robust SEs
ccl.robust.se.22 <- sqrt(diag(ccl.cov22))

stargazer(l1, l2, l11, l12, l21, l22,
          se = list(ccl.robust.se.1, ccl.robust.se.2, ccl.robust.se.11, ccl.robust.se.12, ccl.robust.se.21, ccl.robust.se.22), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

# Repeating above models with an Age^2 variable

l01 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud, family = binomial(link = 'logit'))

ccl.cov01 <- cluster.vcov(l01, ud$RACE_Name) # cluster-robust SEs
ccl.robust.se.01 <- sqrt(diag(ccl.cov01))

l02 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ultradata, family = binomial(link = 'logit'))

ccl.cov02 <- cluster.vcov(l02, ultradata$RACE_Name) # cluster-robust SEs
ccl.robust.se.02 <- sqrt(diag(ccl.cov02))

# Looking at only people who ran consecutive race before covid

l011 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud1, family = binomial(link = 'logit'))

ccl.cov011 <- cluster.vcov(l011, ud1$RACE_Name) # cluster-robust SEs
ccl.robust.se.011 <- sqrt(diag(ccl.cov011))

l012 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = UD1, family = binomial(link = 'logit'))

ccl.cov012 <- cluster.vcov(l012, UD1$RACE_Name) # cluster-robust SEs
ccl.robust.se.012 <- sqrt(diag(ccl.cov012))

# Looking at people who ran more than once in a row before covid

l021 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud2, family = binomial(link = 'logit'))

ccl.cov021 <- cluster.vcov(l021, ud2$RACE_Name) # cluster-robust SEs
ccl.robust.se.021 <- sqrt(diag(ccl.cov021))

l022 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = UD2, family = binomial(link = 'logit'))

ccl.cov022 <- cluster.vcov(l022, UD2$RACE_Name) # cluster-robust SEs
ccl.robust.se.022 <- sqrt(diag(ccl.cov022))

stargazer(l01, l02, l011, l012, l021, l022,
          se = list(ccl.robust.se.01, ccl.robust.se.02, ccl.robust.se.011, ccl.robust.se.012, ccl.robust.se.021, ccl.robust.se.022), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

write.csv(stargazer(l01, l02, l011, l012, l021, l022,
                    se = list(ccl.robust.se.01, ccl.robust.se.02, ccl.robust.se.011, ccl.robust.se.012, ccl.robust.se.021, ccl.robust.se.022), 
                    omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month')),
          paste('D:/ultraCOVID/logit_results.txt', sep = ''), row.names = FALSE)

# Generating the average marginal effects from the logit models

mar01 <- margins(l01, data = find_data(l01, ud))
mar02 <- margins(l02, data = find_data(l02, ultradata))
mar011 <- margins(l011, data = find_data(l011, ud1))
mar012 <- margins(l012, data = find_data(l012, UD1))
mar021 <- margins(l021, data = find_data(l021, ud2))
mar022 <- margins(l022, data = find_data(l022, UD2))

# Repeating the above with probit models

xl1 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud, family = binomial(link = 'probit'))

xccl.cov1 <- cluster.vcov(xl1, ud$RACE_Name) # cluster-robust SEs
xccl.robust.se.1 <- sqrt(diag(xccl.cov1))

xl2 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ultradata, family = binomial(link = 'probit'))

xccl.cov2 <- cluster.vcov(xl2, ultradata$RACE_Name) # cluster-robust SEs
xccl.robust.se.2 <- sqrt(diag(xccl.cov2))

# Looking at only people who ran consecutive race before covid

UD1 <- ultradata[which(ultradata$Consecutive.Appearances == 1), ]
ud1 <- ud[which(ud$Consecutive.Appearances == 1), ]

xl11 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud1, family = binomial(link = 'probit'))

xccl.cov11 <- cluster.vcov(xl11, ud1$RACE_Name) # cluster-robust SEs
xccl.robust.se.11 <- sqrt(diag(xccl.cov11))

xl12 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = UD1, family = binomial(link = 'probit'))

xccl.cov12 <- cluster.vcov(xl12, UD1$RACE_Name) # cluster-robust SEs
xccl.robust.se.12 <- sqrt(diag(xccl.cov12))

# Looking at people who ran more than once in a row before covid

UD2 <- ultradata[which(ultradata$Consecutive.Appearances != 1), ]
ud2 <- ud[which(ud$Consecutive.Appearances != 1), ]

xl21 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud2, family = binomial(link = 'probit'))

xccl.cov21 <- cluster.vcov(xl21, ud2$RACE_Name) # cluster-robust SEs
xccl.robust.se.21 <- sqrt(diag(xccl.cov21))

xl22 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = UD2, family = binomial(link = 'probit'))

xccl.cov22 <- cluster.vcov(xl22, UD2$RACE_Name) # cluster-robust SEs
xccl.robust.se.22 <- sqrt(diag(xccl.cov22))

stargazer(xl1, xl2, xl11, xl12, xl21, xl22,
          se = list(xccl.robust.se.1, xccl.robust.se.2, xccl.robust.se.11, xccl.robust.se.12, xccl.robust.se.21, xccl.robust.se.22), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

# Repeating above models with an Age^2 variable

xl01 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud, family = binomial(link = 'probit'))

xccl.cov01 <- cluster.vcov(xl01, ud$RACE_Name) # cluster-robust SEs
xccl.robust.se.01 <- sqrt(diag(xccl.cov01))

xl02 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ultradata, family = binomial(link = 'probit'))

xccl.cov02 <- cluster.vcov(xl02, ultradata$RACE_Name) # cluster-robust SEs
xccl.robust.se.02 <- sqrt(diag(xccl.cov02))

# Looking at only people who ran consecutive race before covid

xl011 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
             + In_State + Travel_Distance + Ability + Total_Races 
             + Total.Appearances + factor(RACE_Name)
             + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass
             + College_Degree, data = ud1, family = binomial(link = 'probit'))

xccl.cov011 <- cluster.vcov(xl011, ud1$RACE_Name) # cluster-robust SEs
xccl.robust.se.011 <- sqrt(diag(xccl.cov011))

xl012 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
             + In_State + Travel_Distance + Ability + Total_Races 
             + Total.Appearances + factor(RACE_Name)
             + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass
             + College_Degree, data = UD1, family = binomial(link = 'probit'))

xccl.cov012 <- cluster.vcov(xl012, UD1$RACE_Name) # cluster-robust SEs
xccl.robust.se.012 <- sqrt(diag(xccl.cov012))

# Looking at people who ran more than once in a row before covid

xl021 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
             + In_State + Travel_Distance + Ability + Total_Races 
             + Total.Appearances + factor(RACE_Name)
             + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass
             + College_Degree, data = ud2, family = binomial(link = 'probit'))

xccl.cov021 <- cluster.vcov(xl021, ud2$RACE_Name) # cluster-robust SEs
xccl.robust.se.021 <- sqrt(diag(xccl.cov021))

xl022 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
             + In_State + Travel_Distance + Ability + Total_Races 
             + Total.Appearances + factor(RACE_Name)
             + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass
             + College_Degree, data = UD2, family = binomial(link = 'probit'))

xccl.cov022 <- cluster.vcov(xl022, UD2$RACE_Name) # cluster-robust SEs
xccl.robust.se.022 <- sqrt(diag(xccl.cov022))

stargazer(xl01, xl02, xl011, xl012, xl021, xl022,
          se = list(xccl.robust.se.01, xccl.robust.se.02, xccl.robust.se.011, xccl.robust.se.012, xccl.robust.se.021, xccl.robust.se.022), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

write.csv(stargazer(xl01, xl02, xl011, xl012, xl021, xl022,
                    se = list(xccl.robust.se.01, xccl.robust.se.02, xccl.robust.se.011, xccl.robust.se.012, xccl.robust.se.021, xccl.robust.se.022), 
                    omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month')),
          paste('D:/ultraCOVID/probit_results.txt', sep = ''), row.names = FALSE)

# RUN REGRESSIONS PREDICTING IF THE EVENT WAS HELD OR NOT USING COVID DATA, RACE FINISHERS, & DISTANCE

# Data prep to convert runner level data to race level data

ultradata$Female <- as.numeric(ultradata$Gender == 'F')
ultradata$Male <- as.numeric(ultradata$Gender == 'M')

racedata <- ultradata %>%
  group_by(RACE_ID) %>%
  summarize(across(everything(), mean))

RACE_Dist <- c()
RACE_Mon <- c()
RACE_Cit <- c()
RACE_St <- c()

for (i in 1:dim(racedata)[1]) {
  
  rid <- racedata$RACE_ID[i]
  tmp <- ultradata[which(ultradata$RACE_ID == rid),]
  
  RACE_Dist <- c(RACE_Dist, tmp$RACE_Distance[1])
  RACE_Mon <- c(RACE_Mon, tmp$RACE_Month[1])
  RACE_Cit <- c(RACE_Cit, tmp$RACE_City[1])
  RACE_St <- c(RACE_St, tmp$RACE_State[1])
  
}

racedata$RACE_Dist <- RACE_Dist
racedata$RACE_Mon <- RACE_Mon
racedata$RACE_Cit <- RACE_Cit
racedata$RACE_St <- RACE_St

# Start with an LPM

rm1 <- lm(Race_Held_Next_Year ~ Race_City_Cases_MA30_PM1 + Race_State_Cases_MA30_PM1
          + RACE_Finisher_Count + In_State + Travel_Distance + Ability + Age
          + Male + factor(RACE_Dist) + factor(RACE_St) + Total.Appearances, data = racedata)

cl.cov1r <- cluster.vcov(rm1, racedata$RACE_St) # cluster-robust SEs
cl.robust.se.1r <- sqrt(diag(cl.cov1r))

stargazer(rm1, se = list(cl.robust.se.1r),  type = 'text', omit = c('RACE_Dist', 'RACE_St'))

# Summary stats for the race level data

racedata <- as.data.frame(racedata)

write.csv(stargazer(racedata, summary.stat = c('n', 'mean', 'sd', 'min', 'max')),
          paste('D:/ultraCOVID/summary_stats_race.txt', sep = ''), row.names = FALSE)

# Create a figure showing where runners were more or less likely to compete (using hometowns)

plotdata <- ultradata %>%
  group_by(Y) %>%
  count(FIPS)

plotdata <- as.data.frame(plotdata)

plotdata0 <- plotdata[which(plotdata$Y == 0),]
plotdata1 <- plotdata[which(plotdata$Y == 1),]

id <- unique(ultradata$FIPS)
vals <- c()

for (f in id) {
  
  if (f %in% plotdata0$FIPS) {
    
    tmp <- plotdata0[which(plotdata0$FIPS == f),]
    
    if (dim(tmp)[1] > 0) {
      
      val0 <- tmp$n
      
    } else {
      
      val0 <- 0
      
    }
    
  } else {
    
    val0 <- 0
    
  }
  
  if (f %in% plotdata1$FIPS) {
    
    tmp <- plotdata1[which(plotdata1$FIPS == f),]
    
    if (dim(tmp)[1] > 0) {
      
      val1 <- tmp$n
      
    } else {
      
      val1 <- 0
      
    }
    
  } else {
    
    val1 <- 0
    
  }
  
  v <- val0 + val1
  
  if (v > 0) {
    
    val <- val1 / v
    vals <- c(vals, val)
    
  } else {
    
    vals <- c(vals, NA)
    
  }
  
}

plotdf <- cbind(id, vals)
plotdf <- as.data.frame(plotdf)
plotdf$vals <- 100*plotdf$vals

finalvals <- c()
cats <- c('0% - 12.5%', '12.5% - 25%', '25% - 37.5%', '37.5% - 50%',
          '50% - 62.5%', '62.5% - 75%', '75% - 87.5%', '87.5% - 100%')

for (v in plotdf$vals) {
  
  tmp <- ceiling(v / 12.5) + 1
  newval <- cats[tmp]
  finalvals <- c(finalvals, newval)
  
}

plotdf$pcts <- finalvals

county_map
county_map$id <- as.numeric(county_map$id)

plotdf <- left_join(county_map, plotdf, by = 'id')

p <- ggplot(data = plotdf, mapping = aes(x = long, y = lat, fill = pcts, group = group))

p <- p + geom_polygon(color = 'gray90', size = 0.05)

p <- p + scale_fill_brewer(palette = 'Reds')

p <- p + theme_bw()

p <- p + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())

p <- p + theme(panel.border = element_blank())

p <- p + ggtitle('Percentage of Runners Competing During COVID-19')

p <- p + theme(plot.title = element_text(hjust = 0.5))

p <- p + theme(axis.title.x = element_blank(),
               axis.text.x = element_blank(),
               axis.ticks.x = element_blank(),
               axis.title.y = element_blank(),
               axis.text.y = element_blank(),
               axis.ticks.y = element_blank())

p + labs(fill = 'Percentage') +
  guides(fill = guide_legend(nrow = 2)) + 
  theme(legend.position = 'bottom')

# Generate a figure showing that more in state runners correlates with smaller races

racedata$Race_Finisher_Count <- racedata$RACE_Finisher_Count
racedata$In_State <- 100*racedata$In_State

fc <- lm(Race_Finisher_Count ~ In_State, data = racedata)
fc2 <- lm(log(Race_Finisher_Count) ~ In_State, data = racedata)

with(racedata, plot(In_State, Race_Finisher_Count))
abline(fc, col = 'red', lwd = 4)

with(racedata, plot(In_State, log(Race_Finisher_Count), xlab = 'Percent In State', ylab = 'ln(Race Finisher Count)'))
abline(fc2, col = 'red', lwd = 4)

# Running logit models for peer review

l1 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud, family = binomial(link = 'probit'))

ccl.cov1 <- cluster.vcov(l1, ud$RACE_Name) # cluster-robust SEs
ccl.robust.se.1 <- sqrt(diag(ccl.cov1))

l2 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races
          + Total.Appearances + factor(RACE_Name)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ultradata, family = binomial(link = 'probit'))

ccl.cov2 <- cluster.vcov(l2, ultradata$RACE_Name) # cluster-robust SEs
ccl.robust.se.2 <- sqrt(diag(ccl.cov2))

# Looking at only people who ran consecutive race before covid

UD1 <- ultradata[which(ultradata$Consecutive.Appearances == 1), ]
ud1 <- ud[which(ud$Consecutive.Appearances == 1), ]

l11 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud1, family = binomial(link = 'probit'))

ccl.cov11 <- cluster.vcov(l11, ud1$RACE_Name) # cluster-robust SEs
ccl.robust.se.11 <- sqrt(diag(ccl.cov11))

l12 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = UD1, family = binomial(link = 'probit'))

ccl.cov12 <- cluster.vcov(l12, UD1$RACE_Name) # cluster-robust SEs
ccl.robust.se.12 <- sqrt(diag(ccl.cov12))

# Looking at people who ran more than once in a row before covid

UD2 <- ultradata[which(ultradata$Consecutive.Appearances != 1), ]
ud2 <- ud[which(ud$Consecutive.Appearances != 1), ]

l21 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud2, family = binomial(link = 'probit'))

ccl.cov21 <- cluster.vcov(l21, ud2$RACE_Name) # cluster-robust SEs
ccl.robust.se.21 <- sqrt(diag(ccl.cov21))

l22 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races 
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = UD2, family = binomial(link = 'probit'))

ccl.cov22 <- cluster.vcov(l22, UD2$RACE_Name) # cluster-robust SEs
ccl.robust.se.22 <- sqrt(diag(ccl.cov22))

stargazer(l1, l2, l11, l12, l21, l22,
          se = list(ccl.robust.se.1, ccl.robust.se.2, ccl.robust.se.11, ccl.robust.se.12, ccl.robust.se.21, ccl.robust.se.22), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

# Repeating above models with an Age^2 variable

l01 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud, family = binomial(link = 'probit'))

ccl.cov01 <- cluster.vcov(l01, ud$RACE_Name) # cluster-robust SEs
ccl.robust.se.01 <- sqrt(diag(ccl.cov01))

l02 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races
           + Total.Appearances + factor(RACE_Name)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ultradata, family = binomial(link = 'probit'))

ccl.cov02 <- cluster.vcov(l02, ultradata$RACE_Name) # cluster-robust SEs
ccl.robust.se.02 <- sqrt(diag(ccl.cov02))

# Looking at only people who ran consecutive race before covid

l011 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud1, family = binomial(link = 'probit'))

ccl.cov011 <- cluster.vcov(l011, ud1$RACE_Name) # cluster-robust SEs
ccl.robust.se.011 <- sqrt(diag(ccl.cov011))

l012 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = UD1, family = binomial(link = 'probit'))

ccl.cov012 <- cluster.vcov(l012, UD1$RACE_Name) # cluster-robust SEs
ccl.robust.se.012 <- sqrt(diag(ccl.cov012))

# Looking at people who ran more than once in a row before covid

l021 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud2, family = binomial(link = 'probit'))

ccl.cov021 <- cluster.vcov(l021, ud2$RACE_Name) # cluster-robust SEs
ccl.robust.se.021 <- sqrt(diag(ccl.cov021))

l022 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races 
            + Total.Appearances + factor(RACE_Name)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = UD2, family = binomial(link = 'probit'))

ccl.cov022 <- cluster.vcov(l022, UD2$RACE_Name) # cluster-robust SEs
ccl.robust.se.022 <- sqrt(diag(ccl.cov022))

stargazer(l01, l02, l011, l012, l021, l022,
          se = list(ccl.robust.se.01, ccl.robust.se.02, ccl.robust.se.011, ccl.robust.se.012, ccl.robust.se.021, ccl.robust.se.022), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

write.csv(stargazer(l01, l02, l011, l012, l021, l022,
                    se = list(ccl.robust.se.01, ccl.robust.se.02, ccl.robust.se.011, ccl.robust.se.012, ccl.robust.se.021, ccl.robust.se.022), 
                    omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month')),
          paste('D:/ultraCOVID/probit_results_raw.txt', sep = ''), row.names = FALSE)

# Multi-level modelling for peer review

# Does my data have a multilevel structure?

base <- lm(Attended_Next_Year_Race ~ 1, data = ud)

test.mon <- lmer(Attended_Next_Year_Race ~ (1 | RACE_Month), REML = FALSE, data = ud)
test.race <- lmer(Attended_Next_Year_Race ~ (1 | RACE_Name), REML = FALSE, data = ud)
test.st <- lmer(Attended_Next_Year_Race ~ (1 | RACE_State), REML = FALSE, data = ud)
test.morace <- lmer(Attended_Next_Year_Race ~ (1 | RACE_Month/RACE_Name), REML = FALSE, data = ud)
test.most <- lmer(Attended_Next_Year_Race ~ (1 | RACE_Month/RACE_State), REML = FALSE, data = ud)

summary(test.mon)
summary(test.race)
summary(test.st)
summary(test.morace)
summary(test.most)

total.var.mon <- 0.001044 + 0.120254
total.var.race <- 0.009287 + 0.111283
total.var.st <- 0.003572 + 0.117422
total.var.morace <- 0.009247 + 0.00002717 + 0.1113
total.var.most <- 0.008618 + 0.00002836 + 0.113

mon.var <- (0.001044 / total.var.mon)*100
race.var <- (0.03231 / total.var.race)*100
st.var <- (0.003572 / total.var.st)*100
morace.var <- ((0.096161 + 0.005212) / total.var.morace)*100
most.var <- ((0.096161 + 0.005212) / total.var.most)*100

mon.var
race.var
st.var
morace.var
most.var

anova.mon <- anova(test.mon, base)
anova.race <- anova(test.race, base)
anova.st <- anova(test.st, base)
anova.morace <- anova(test.morace, base)
anova.most <- anova(test.most, base)

anova.mon
anova.race
anova.st
anova.morace
anova.most

# Since it does, run the models

mlm <- lmer(Attended_Next_Year_Race ~ (1 | NY_RACE_Month) + Runner_City_Cases_MA30
            + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
            + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree
            + factor(RACE_Name), REML = FALSE, data = ud)

mlm2 <- lmer(Attended_Next_Year_Race ~ (1 | RACE_Name) + Runner_City_Cases_MA30
             + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
             + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree
             + factor(NY_RACE_Month), REML = FALSE, data = ud)

mlm3 <- lmer(Attended_Next_Year_Race ~ (1 | RACE_State) + Runner_City_Cases_MA30
             + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
             + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree
             + factor(NY_RACE_Month), REML = FALSE, data = ud)

mlm4 <- lmer(Attended_Next_Year_Race ~ (1 | NY_RACE_Month/RACE_Name) + Runner_City_Cases_MA30
             + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
             + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
             REML = FALSE, data = ud)

mlm5 <- lmer(Attended_Next_Year_Race ~ (1 | NY_RACE_Month/RACE_State) + Runner_City_Cases_MA30
             + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
             + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree
             + factor(RACE_Name), REML = FALSE, data = ud)

stargazer(mlm, mlm2, mlm3, mlm4, mlm5, type = 'text', omit = c('RACE_Name'))

write.csv(stargazer(mlm, mlm2, mlm3, mlm4, mlm5, omit = c('RACE_Name')), 'D:/ultraCOVID/mlm_results_attended.txt', row.names = FALSE)

# Repeat above analysis for Y

ybase <- lm(Y ~ 1, data = ultradata)

ytest.mon <- lmer(Y ~ (1 | RACE_Month), REML = FALSE, data = ultradata)
ytest.race <- lmer(Y ~ (1 | RACE_Name), REML = FALSE, data = ultradata)
ytest.st <- lmer(Y ~ (1 | RACE_State), REML = FALSE, data = ultradata)
ytest.morace <- lmer(Y ~ (1 | RACE_Month/RACE_Name), REML = FALSE, data = ultradata)
ytest.most <- lmer(Y ~ (1 | RACE_Month/RACE_State), REML = FALSE, data = ultradata)

summary(ytest.mon)
summary(ytest.race)
summary(ytest.st)
summary(ytest.morace)
summary(ytest.most)

ytotal.var.mon <- 0.01006 + 0.22066
ytotal.var.race <- 0.1256 + 0.1564
ytotal.var.st <- 0.03071 + 0.21617
ytotal.var.morace <- 0.121413 + 0.007485 + 0.156369
ytotal.var.most <- 0.087005 + 0.005668 + 0.188613

ymon.var <- (0.01006 / ytotal.var.mon)*100
yrace.var <- (0.1256 / ytotal.var.race)*100
yst.var <- (0.03071 / ytotal.var.st)*100
ymorace.var <- ((0.121413 + 0.007485) / ytotal.var.morace)*100
ymost.var <- ((0.087005 + 0.005668) / ytotal.var.most)*100

ymon.var
yrace.var
yst.var
ymorace.var
ymost.var

yanova.mon <- anova(ytest.mon, ybase)
yanova.race <- anova(ytest.race, ybase)
yanova.st <- anova(ytest.st, ybase)
yanova.morace <- anova(ytest.morace, ybase)
yanova.most <- anova(ytest.most, ybase)

yanova.mon
yanova.race
yanova.st
yanova.morace
yanova.most

# Since it does, run the models

ymlm <- lmer(Y ~ (1 | NY_RACE_Month) + Runner_City_Cases_MA30
             + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
             + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
             + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree
             + factor(RACE_Name), REML = FALSE, data = ultradata)

ymlm2 <- lmer(Y ~ (1 | RACE_Name) + Runner_City_Cases_MA30
              + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
              + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
              + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree
              + factor(NY_RACE_Month), REML = FALSE, data = ultradata)

ymlm3 <- lmer(Y ~ (1 | RACE_State) + Runner_City_Cases_MA30
              + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
              + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
              + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree
              + factor(NY_RACE_Month), REML = FALSE, data = ultradata)

ymlm4 <- lmer(Y ~ (1 | NY_RACE_Month/RACE_Name) + Runner_City_Cases_MA30
              + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
              + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
              + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree,
              REML = FALSE, data = ultradata)

ymlm5 <- lmer(Y ~ (1 | NY_RACE_Month/RACE_State) + Runner_City_Cases_MA30
              + Race_City_Cases_MA30 + In_State + Travel_Distance + Ability + Total_Races
              + Total.Appearances + factor(Gender) + Age + Age2 + RACE_Finisher_Count
              + Median_Household_Income + Unemployment_Rate + Some_College_Ass + College_Degree
              + factor(RACE_Name), REML = FALSE, data = ultradata)

stargazer(ymlm, ymlm2, ymlm3, ymlm4, ymlm5, type = 'text', omit = c('RACE_Name'))

write.csv(stargazer(ymlm, ymlm2, ymlm3, ymlm4, ymlm5, omit = c('RACE_Name')), 'D:/ultraCOVID/mlm_results_Y.txt', row.names = FALSE)

# Making a joint mlm results table to report in paper

stargazer(mlm5, ymlm5, type = 'text', omit = c('RACE_Name'))

write.csv(stargazer(mlm5, ymlm5, omit = c('RACE_Name')), 'D:/ultraCOVID/mlm_results.txt', row.names = FALSE)

# Making a figure for the paper which shows the NY_RACE_Month fixed effect intervals - values from lpm m01 with robust serrs
# COVID data from [https://ourworldindata.org/coronavirus/country/united-states]

covidts <- read.csv(paste0(direc, 'covidts.csv'))
covidts <- covidts %>% filter(Month != 'Apr')

months <- c('May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar')
month.fes <- c(-0.127, 0.021, 0.064, 0.069, 0.136, 0.143, 0.133, 0.144, 0.063, 0.058, 0.042)
month.ses <- c(0.085, 0.036, 0.049, 0.039, 0.010, 0.026, 0.032, 0.043, 0.084, 0.085, 0.089)

ggdf <- as.data.frame(cbind(months, month.fes, month.ses))
colnames(ggdf) <- c('Month', 'Value', 'serr')

ggdf$Cases <- covidts$Cases
ggdf$CasesPM <- covidts$CasesPM
ggdf$Deaths <- covidts$Deaths
ggdf$DeathsPM <- covidts$DeathsPM
ggdf$Value <- as.numeric(ggdf$Value)
ggdf$serr <- as.numeric(ggdf$serr)
ggdf$ID <- 1:11

ggplot(ggdf, aes(x = ID, y = Value)) + 
  geom_errorbar(width = .25, aes(ymin = Value - 1.96*serr, ymax = Value + 1.96*serr)) + 
  geom_point(shape = 21, size = 3, fill = 'black') + 
  geom_hline(yintercept = 0, size = 0.5) + 
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle('Month Fixed Effect Values (Relative to April 2020)') + 
  xlab('Month') + 
  ylab('Value') + 
  scale_x_continuous(breaks = seq(1, 11, 1), labels = months)

# Adding an additional time series for previous month COVID cases

cols <- c('Fixed Effects' = 'black', 'COVID Cases' = 'black')

ggplot(ggdf, aes(x = ID, y = Value)) + 
  geom_errorbar(width = .25, aes(ymin = Value - 1.96*serr, ymax = Value + 1.96*serr, color = 'Fixed Effects')) + 
  geom_point(shape = 21, size = 3, fill = 'black', aes(color = 'Fixed Effects')) +
  geom_hline(yintercept = 0, size = 0.5) + 
  geom_line(aes(x = ID, y = CasesPM/(2*max(CasesPM)), color = 'COVID Cases'), size = 1) + 
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5), legend.box.background = element_rect(color = 'black', size = 1)) + 
  ggtitle('Month Fixed Effect Values and New COVID Cases') + 
  xlab('Month') + 
  scale_x_continuous(breaks = seq(1, 11, 1), labels = months) + 
  scale_y_continuous(name = 'Month Fixed Effect Value (Relative to April)', sec.axis = sec_axis(~.*2*max(ggdf$CasesPM)/1000000, name = 'Million New COVID Cases')) +
  scale_colour_manual(name = 'Legend', values = cols, guide = guide_legend(fill = NULL, color = NULL))

