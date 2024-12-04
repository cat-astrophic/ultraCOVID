# ultraCOVID

This repo contains scripts which collect data on ultramarathons and their participants for a paper entitled "Gender, Risk Aversion, and Travel: How COVID-19 Affected Participation in Ultramarathons" which has been published in the [*Journal of Sports Economics*](https://journals.sagepub.com/doi/abs/10.1177/15270025241279231). All race and runner data are obtained through these scripts; data for all covariates used in this paper can be found in the compressed data file.

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

## Citation

### APA

Cary, M., & Stephens, H. M. (2024). How COVID-19 Affected Participation in Ultramarathons: Gender, Risk Aversion, and Travel. *Journal of Sports Economics*, 15270025241279231.

### MLA

Cary, Michael, and Heather M. Stephens. "How COVID-19 Affected Participation in Ultramarathons: Gender, Risk Aversion, and Travel." *Journal of Sports Economics* (2024): 15270025241279231.

### Bibtex

@article{cary2024covid,\
&nbsp;&nbsp;&nbsp;&nbsp;title={How COVID-19 Affected Participation in Ultramarathons: Gender, Risk Aversion, and Travel},\
&nbsp;&nbsp;&nbsp;&nbsp;author={Cary, Michael and Stephens, Heather M},\
&nbsp;&nbsp;&nbsp;&nbsp;journal={Journal of Sports Economics},\
&nbsp;&nbsp;&nbsp;&nbsp;pages={15270025241279231},\
&nbsp;&nbsp;&nbsp;&nbsp;year={2024},\
&nbsp;&nbsp;&nbsp;&nbsp;publisher={SAGE Publications Sage CA: Los Angeles, CA}\
}

