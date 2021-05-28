# This script does the econometrics for the ultraCOVID project

# Loading libraries

library(stargazer)
library(dplyr)
library(sandwich)
library(miceadds)
library(lmtest)
library(multiwayvcov)
library(margins)

# Specifying your username

username <- ''

# Reading in the data

ultradata <- read.csv(paste('C:/Users/', username, '/Documents/Data/ultraCOVID/ultradata.csv', sep = ''))

# Creating and age squared variable

ultradata$Age2 <- ultradata$Age * ultradata$Age

# Creating the baseline data set

ud <- ultradata[which(ultradata$Race_Held_Next_Year == 1),]

# Running LPMs for starters

m1 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races# + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud)

cl.cov1 <- cluster.vcov(m1, ud$RACE_Name) # cluster-robust SEs
cl.robust.se.1 <- sqrt(diag(cl.cov1))

m2 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
         + In_State + Travel_Distance + Ability + Total_Races# + Consecutive.Appearances
         + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
         + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
         + Median_Household_Income + Unemployment_Rate + Some_College_Ass
         + College_Degree, data = ultradata)

cl.cov2 <- cluster.vcov(m2, ultradata$RACE_Name) # cluster-robust SEs
cl.robust.se.2 <- sqrt(diag(cl.cov2))

# Looking at only people who ran consecutive race before covid

UD1 <- ultradata[which(ultradata$Consecutive.Appearances == 1), ]
ud1 <- ud[which(ud$Consecutive.Appearances == 1), ]

m11 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
         + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
         + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
         + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
         + Median_Household_Income + Unemployment_Rate + Some_College_Ass
         + College_Degree, data = ud1)

cl.cov11 <- cluster.vcov(m11, ud1$RACE_Name) # cluster-robust SEs
cl.robust.se.11 <- sqrt(diag(cl.cov11))

m12 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
         + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
         + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
         + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
         + Median_Household_Income + Unemployment_Rate + Some_College_Ass
         + College_Degree, data = UD1)

cl.cov12 <- cluster.vcov(m12, UD1$RACE_Name) # cluster-robust SEs
cl.robust.se.12 <- sqrt(diag(cl.cov12))

# Looking at people who ran more than once in a row before covid

UD2 <- ultradata[which(ultradata$Consecutive.Appearances != 1), ]
ud2 <- ud[which(ud$Consecutive.Appearances != 1), ]

m21 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud2)

cl.cov21 <- cluster.vcov(m21, ud2$RACE_Name) # cluster-robust SEs
cl.robust.se.21 <- sqrt(diag(cl.cov21))

m22 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
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
         + In_State + Travel_Distance + Ability + Total_Races# + Consecutive.Appearances
         + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
         + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
         + Median_Household_Income + Unemployment_Rate + Some_College_Ass
         + College_Degree, data = ud)

cl.cov01 <- cluster.vcov(m01, ud$RACE_Name) # cluster-robust SEs
cl.robust.se.01 <- sqrt(diag(cl.cov01))

m02 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
         + In_State + Travel_Distance + Ability + Total_Races# + Consecutive.Appearances
         + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
         + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
         + Median_Household_Income + Unemployment_Rate + Some_College_Ass
         + College_Degree, data = ultradata)

cl.cov02 <- cluster.vcov(m02, ultradata$RACE_Name) # cluster-robust SEs
cl.robust.se.02 <- sqrt(diag(cl.cov02))

# Looking at only people who ran consecutive race before covid

m011 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
          + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud1)

cl.cov011 <- cluster.vcov(m011, ud1$RACE_Name) # cluster-robust SEs
cl.robust.se.011 <- sqrt(diag(cl.cov011))

m012 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
          + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = UD1)

cl.cov012 <- cluster.vcov(m012, UD1$RACE_Name) # cluster-robust SEs
cl.robust.se.012 <- sqrt(diag(cl.cov012))

# Looking at people who ran more than once in a row before covid

m021 <- lm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
          + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud2)

cl.cov021 <- cluster.vcov(m021, ud2$RACE_Name) # cluster-robust SEs
cl.robust.se.021 <- sqrt(diag(cl.cov021))

m022 <- lm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
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
                    paste('C:/Users/', username, '/Documents/Data/ultraCOVID/lpm_results.txt', sep = ''), row.names = FALSE)

# Repeating the above with logit models

l1 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races# + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ud, family = binomial(link = logit))

ccl.cov1 <- cluster.vcov(l1, ud$RACE_Name) # cluster-robust SEs
ccl.robust.se.1 <- sqrt(diag(ccl.cov1))

l2 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
          + In_State + Travel_Distance + Ability + Total_Races# + Consecutive.Appearances
          + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
          + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
          + Median_Household_Income + Unemployment_Rate + Some_College_Ass
          + College_Degree, data = ultradata, family = binomial(link = logit))

ccl.cov2 <- cluster.vcov(l2, ultradata$RACE_Name) # cluster-robust SEs
ccl.robust.se.2 <- sqrt(diag(ccl.cov2))

# Looking at only people who ran consecutive race before covid

UD1 <- ultradata[which(ultradata$Consecutive.Appearances == 1), ]
ud1 <- ud[which(ud$Consecutive.Appearances == 1), ]

l11 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
           + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud1, family = binomial(link = logit))

ccl.cov11 <- cluster.vcov(l11, ud1$RACE_Name) # cluster-robust SEs
ccl.robust.se.11 <- sqrt(diag(ccl.cov11))

l12 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
           + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = UD1, family = binomial(link = logit))

ccl.cov12 <- cluster.vcov(l12, UD1$RACE_Name) # cluster-robust SEs
ccl.robust.se.12 <- sqrt(diag(ccl.cov12))

# Looking at people who ran more than once in a row before covid

UD2 <- ultradata[which(ultradata$Consecutive.Appearances != 1), ]
ud2 <- ud[which(ud$Consecutive.Appearances != 1), ]

l21 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
           + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud2, family = binomial(link = logit))

ccl.cov21 <- cluster.vcov(l21, ud2$RACE_Name) # cluster-robust SEs
ccl.robust.se.21 <- sqrt(diag(ccl.cov21))

l22 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
           + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
           + factor(Gender) + Age + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = UD2, family = binomial(link = logit))

ccl.cov22 <- cluster.vcov(l22, UD2$RACE_Name) # cluster-robust SEs
ccl.robust.se.22 <- sqrt(diag(ccl.cov22))

stargazer(l1, l2, l11, l12, l21, l22,
          se = list(ccl.robust.se.1, ccl.robust.se.2, ccl.robust.se.11, ccl.robust.se.12, ccl.robust.se.21, ccl.robust.se.22), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

# Repeating above models with an Age^2 variable

l01 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races# + Consecutive.Appearances
           + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ud, family = binomial(link = logit))

ccl.cov01 <- cluster.vcov(l01, ud$RACE_Name) # cluster-robust SEs
ccl.robust.se.01 <- sqrt(diag(ccl.cov01))

l02 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
           + In_State + Travel_Distance + Ability + Total_Races# + Consecutive.Appearances
           + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
           + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
           + Median_Household_Income + Unemployment_Rate + Some_College_Ass
           + College_Degree, data = ultradata, family = binomial(link = logit))

ccl.cov02 <- cluster.vcov(l02, ultradata$RACE_Name) # cluster-robust SEs
ccl.robust.se.02 <- sqrt(diag(ccl.cov02))

# Looking at only people who ran consecutive race before covid

l011 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
            + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud1, family = binomial(link = logit))

ccl.cov011 <- cluster.vcov(l011, ud1$RACE_Name) # cluster-robust SEs
ccl.robust.se.011 <- sqrt(diag(ccl.cov011))

l012 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
            + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = UD1, family = binomial(link = logit))

ccl.cov012 <- cluster.vcov(l012, UD1$RACE_Name) # cluster-robust SEs
ccl.robust.se.012 <- sqrt(diag(ccl.cov012))

# Looking at people who ran more than once in a row before covid

l021 <- glm(Attended_Next_Year_Race ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
            + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = ud2, family = binomial(link = logit))

ccl.cov021 <- cluster.vcov(l021, ud2$RACE_Name) # cluster-robust SEs
ccl.robust.se.021 <- sqrt(diag(ccl.cov021))

l022 <- glm(Y ~ Runner_City_Cases_MA30 + Race_City_Cases_MA30
            + In_State + Travel_Distance + Ability + Total_Races # + Consecutive.Appearances
            + Total.Appearances + factor(RACE_Name) + factor(RACE_Distance)
            + factor(Gender) + Age + Age2 + factor(NY_RACE_Month) + RACE_Finisher_Count
            + Median_Household_Income + Unemployment_Rate + Some_College_Ass
            + College_Degree, data = UD2, family = binomial(link = logit))

ccl.cov022 <- cluster.vcov(l022, UD2$RACE_Name) # cluster-robust SEs
ccl.robust.se.022 <- sqrt(diag(ccl.cov022))

stargazer(l01, l02, l011, l012, l021, l022,
          se = list(ccl.robust.se.01, ccl.robust.se.02, ccl.robust.se.011, ccl.robust.se.012, ccl.robust.se.021, ccl.robust.se.022), 
          type = 'text', omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month'))

write.csv(stargazer(l01, l02, l011, l012, l021, l022,
          se = list(ccl.robust.se.01, ccl.robust.se.02, ccl.robust.se.011, ccl.robust.se.012, ccl.robust.se.021, ccl.robust.se.022), 
          omit = c('RACE_Name', 'RACE_Distance', 'NY_RACE_Month')),
          paste('C:/Users/', username, '/Documents/Data/ultraCOVID/logit_results.txt', sep = ''), row.names = FALSE)

# Generating the average effects from the logit models

mar01 <- margins(l01)
mar02 <- margins(l02)
mar011 <- margins(l011)
mar012 <- margins(l012)
mar021 <- margins(l021)
mar022 <- margins(l022)

t01 <- l01$coefficients / subrse01
t02 <- l02$coefficients / subrse02
t011 <- l011$coefficients / subrse011
t012 <- l012$coefficients / subrse012
t021 <- l021$coefficients / subrse021
t022 <- l022$coefficients / subrse022

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

# Start with a LPM

rm1 <- lm(Race_Held_Next_Year ~ Race_City_Cases_MA30_PM1 + Race_State_Cases_MA30_PM1
          + RACE_Finisher_Count + In_State + Travel_Distance + Ability + Age
          + Male + factor(RACE_Dist) + factor(RACE_St) + Total.Appearances, data = racedata)

cl.cov1r <- cluster.vcov(rm1, racedata$RACE_St) # cluster-robust SEs
cl.robust.se.1r <- sqrt(diag(cl.cov1r))
  
stargazer(rm1, se = list(cl.robust.se.1r),  type = 'text', omit = c('RACE_Dist', 'RACE_St'))

# Run a logit model

rl1 <- glm(Race_Held_Next_Year ~ Race_City_Cases_MA30_PM1 + Race_State_Cases_MA30_PM1
          + RACE_Finisher_Count + In_State + Travel_Distance + Ability + Age
          + Male + factor(RACE_Dist) + factor(RACE_St) + Total.Appearances,
          data = racedata, family = binomial(link = logit))

cl.cov1rl <- cluster.vcov(rl1, racedata$RACE_St) # cluster-robust SEs
cl.robust.se.1rl <- sqrt(diag(cl.cov1rl))

stargazer(rl1, se = list(cl.robust.se.1rl),  type = 'text', omit = c('RACE_Dist', 'RACE_St'))

stargazer(rm1, rl1, se = list(cl.robust.se.1r, cl.robust.se.1rl),  type = 'text', omit = c('RACE_Dist', 'RACE_St'))

mar1 <- margins(rl1)
t1 <- rl1$coefficients / mar1



































