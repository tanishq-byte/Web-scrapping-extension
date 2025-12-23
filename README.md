# test
"""
pip freeze -r "requirements.txt"
"""
Core (must-have)
country / region (use ISO codes / standardized region names)
subnational_region (state / province / county / district)
year (YYYY)
crop or commodity (standardized name)
area_organic_ha (hectares under organic cultivation)
production_organic_tonnes (total production)
yield_organic_t_per_ha (production/area)
number_of_organic_farms (or producers)
certification_scheme (e.g., PGS, India Organic, USDA NOP, EU Reg.)
data_source (URL + scraped date)
Important extra fields (very useful)
production_value_usd or local currency (market size)
export_volume / export_value (if available)
crop_subtype (e.g., rice / basmati)
farming_system (certified vs PGS/participatory)
farm_size_mean_median_ha
year_of_certification or certified_area_change (trend)
notes or methodology (how the number was collected)
Nice-to-have (for geospatial / advanced analysis)
latitude, longitude (if farm/plot level)
soil_type, irrigation flags, input_use (organic fertiliser, compost)
price_per_tonne or local_market_prices
data_quality_flag (official estimate vs survey vs private)