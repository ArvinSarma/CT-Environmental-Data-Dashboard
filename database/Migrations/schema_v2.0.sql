CREATE TABLE IF NOT EXISTS ct_hazardous_data (
    geoid VARCHAR(20),                                                      -- Historic or current GEOID from CSV/lookup
    town_name VARCHAR(100) REFERENCES ct_towns(town_name) ON DELETE CASCADE,-- Foreign key referencing parent town table
    town_address VARCHAR(500),                                              -- Address of the incident
    client VARCHAR(255),                                                    -- Who filed the report
    manifest_number VARCHAR(50),                                            -- Manifest number (id1)
    generator_id_number VARCHAR(50),                                        -- Generator ID (id2)
    date_shipped DATE                                                       -- Date report was made
);