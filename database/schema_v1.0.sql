CREATE TABLE IF NOT EXISTS ct_towns (
    geoid VARCHAR(20) PRIMARY KEY,       -- Standardized GeoID (Unique Key)
    fid INT,                             -- Feature ID
    fid_1 INT,                           -- Secondary Feature ID
    sfips VARCHAR(10),                   -- State FIPS code
    prfips VARCHAR(10),                  -- Planning Region FIPS code
    tfips VARCHAR(10),                   -- Town FIPS code
    town_name VARCHAR(100) NOT NULL,     -- Town Name
    county_name VARCHAR(100),            -- County Name 
    tfips20 VARCHAR(10),                 -- 2020 Town FIPS
    cfips20 VARCHAR(10),                 -- 2020 County FIPS
    pr_name VARCHAR(100),                -- Planning Region Name
    puma20_code VARCHAR(20),             -- Public Use Microdata Area Code
    puma20_name VARCHAR(100),            -- PUMA Name
    shape_area NUMERIC,                  -- GIS Polygon Area
    shape_length NUMERIC                 -- GIS Polygon Perimeter
);

CREATE TABLE IF NOT EXISTS ct_towns_median_income (
    geoid VARCHAR(20) PRIMARY KEY REFERENCES towns(geoid) ON DELETE CASCADE,  -- Standardized GeoID (Unique Key)
    town_name VARCHAR(100) NOT NULL,                                          -- Town Name
    median_income NUMERIC,                                                    -- Median Household Income for a town
    margin_of_error NUMERIC,                                                  -- Margin of Error for the median income
    data_year INT,                                                                 -- Year of the data
    race_ethnicity VARCHAR(50),                                               -- Race/Ethnicity category for the median income data
    geography_type VARCHAR(50)                                                -- Type of geography (e.g., Town, County, etc.)
);