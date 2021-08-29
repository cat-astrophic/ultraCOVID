# This script runs regression for the ultraCOVID project without race level FEs
# Be sure to update the username from User

clear

import delimited "C:\Users\User\Documents\Data\ultraCOVID\ultradata.csv"

save "C:\Users\User\Documents\Data\ultraCOVID\ultradata.dta", replace

use "C:\Users\User\Documents\Data\ultraCOVID\ultradata.dta"

# Generate an age squared variable and convert some string variables b/c I hate stata

gen age2 = age*age

egen race_name2 = group(race_name)

egen gender2 = group(gender)

egen ny_race_month2 = group(ny_race_month)

# Increase the COVID data by a factor of 1000 so that the point estimate is legible

gen runner_city_cases_ma301 = runner_city_cases_ma30/1000
gen race_city_cases_ma301 = race_city_cases_ma30/1000

# Running the regressions

logit attended_next_year_race runner_city_cases_ma301 race_city_cases_ma301 in_state travel_distance ability total_races totalappearances i.gender2 age age2 i.ny_race_month2 race_finisher_count median_household_income unemployment_rate some_college_ass college_degree, r

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_results_no_FE.dta, replace excel dec(3)

margins, dydx(*)

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_margins_no_FE.dta, replace excel dec(3)

logit y runner_city_cases_ma301 race_city_cases_ma301 in_state travel_distance ability total_races totalappearances i.gender2 age age2 i.ny_race_month2 race_finisher_count median_household_income unemployment_rate some_college_ass college_degree, r

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_results_no_FE.dta, append excel dec(3)

margins, dydx(*)

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_margins_no_FE.dta, append excel dec(3)

logit attended_next_year_race runner_city_cases_ma301 race_city_cases_ma301 in_state travel_distance ability total_races totalappearances i.gender2 age age2 i.ny_race_month2 race_finisher_count median_household_income unemployment_rate some_college_ass college_degree if consecutiveappearances == 1, r

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_results_no_FE.dta, append excel dec(3)

margins, dydx(*)

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_margins_no_FE.dta, append excel dec(3)

logit y runner_city_cases_ma301 race_city_cases_ma301 in_state travel_distance ability total_races totalappearances i.gender2 age age2 i.ny_race_month2 race_finisher_count median_household_income unemployment_rate some_college_ass college_degree if consecutiveappearances == 1, r

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_results_no_FE.dta, append excel dec(3)

margins, dydx(*)

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_margins_no_FE.dta, append excel dec(3)

logit attended_next_year_race runner_city_cases_ma301 race_city_cases_ma301 in_state travel_distance ability total_races totalappearances i.gender2 age age2 i.ny_race_month2 race_finisher_count median_household_income unemployment_rate some_college_ass college_degree if consecutiveappearances > 1, r

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_results_no_FE.dta, append excel dec(3)

margins, dydx(*)

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_margins_no_FE.dta, append excel dec(3)

logit y runner_city_cases_ma301 race_city_cases_ma301 in_state travel_distance ability total_races totalappearances i.gender2 age age2 i.ny_race_month2 race_finisher_count median_household_income unemployment_rate some_college_ass college_degree if consecutiveappearances > 1, r

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_results_no_FE.dta, append excel dec(3)

margins, dydx(*)

outreg2 using C:\Users\User\Documents\Data\ultraCOVID\logit_margins_no_FE.dta, append excel dec(3)

