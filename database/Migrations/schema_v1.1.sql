-- 1. Remove the Primary Key constraint from geoid on ct_towns_median_income
ALTER TABLE ct_towns_median_income 
DROP CONSTRAINT IF EXISTS ct_towns_median_income_pkey;

-- 2. Define a Composite Primary Key so a town can have multiple entries across years & races
ALTER TABLE ct_towns_median_income 
ADD CONSTRAINT ct_towns_median_income_pkey PRIMARY KEY (geoid, data_year, race_ethnicity);