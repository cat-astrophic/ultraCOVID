# ultraCOVID

currently this repo contains scripts which collect data on ultramarathons and their participants - eventually I aim to use this to study some questions related to the decision to compete (and travel) during the pandemic

1. ultrascraper1.py -- gets event specific urls
2. ultrascraper2.py -- scrapes event urls for results data
3. ultraprepper.py -- preps initial runner and race data
4. ultracovidatamaker.py -- creates race & runner county COVID data
5. ultrablender.py -- blends the COVID data and the ultramarathon data
6. ultralast.py --  this script adds race_held_next_year data to pm1 columns
7. ultravariables.py -- ensures all variables are in a format suitable for regressions
8. ultraERS.py -- adds county level socioeconomic covariates
9. ultrarunne.R -- runs all models (runner and race models)
10. ultraCOVID.do -- this runs the race models from ultrarunne.R since it generates margins more quickly
