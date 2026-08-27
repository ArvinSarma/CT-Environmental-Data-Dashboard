-- 1. Drop existing foreign key and primary key constraints
ALTER TABLE ct_towns_median_income 
DROP CONSTRAINT IF EXISTS ct_towns_median_income_geoid_fkey;

ALTER TABLE ct_towns_median_income 
DROP CONSTRAINT IF EXISTS ct_towns_median_income_pkey;

ALTER TABLE ct_towns 
DROP CONSTRAINT IF EXISTS ct_towns_pkey;

-- 2. Set town_name as the Primary Key on ct_towns
ALTER TABLE ct_towns 
ADD CONSTRAINT ct_towns_pkey PRIMARY KEY (town_name);

-- 3. Update ct_towns_median_income to use town_name for FK and PK
ALTER TABLE ct_towns_median_income 
ADD CONSTRAINT ct_towns_median_income_town_fkey 
FOREIGN KEY (town_name) REFERENCES ct_towns(town_name) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ct_towns_median_income 
ADD CONSTRAINT ct_towns_median_income_pkey 
PRIMARY KEY (town_name, data_year, race_ethnicity);