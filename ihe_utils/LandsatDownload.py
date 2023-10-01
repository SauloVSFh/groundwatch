from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer
import json


# Initialize a new API instance and get an access key
username = 'SauloVSFh'
password = '32316547eu94'
api = API(username, password)


# Perform a request. Results are returned in a dictionnary
# Search for Landsat TM scenes
scenes = api.search(
    dataset='landsat_8_c1',
    latitude=37.28,
    longitude= 46.38,
    start_date='2017-10-01',
    end_date='2018-09-30',
    max_cloud_cover=50
)


print(f"{len(scenes)} scenes found.")

# Log out
api.logout()

# Process the result
output_dir = 'D:\My Documents\RemoteSensing\Assignment\Part2'
i=0
for scene in scenes:
    i+=1
    if i in range(15,18):
        print(i , '\n', scene['acquisition_date'].strftime('%Y-%m-%d'))
        ee = EarthExplorer(username, password)
        ee.download(scene['entity_id'], output_dir= output_dir)
        ee.logout()
    # Write scene footprints to disk
    fname = f"{scene['landsat_product_id']}.geojson"
    with open(fname, "w") as f:
        json.dump(scene['spatial_coverage'].__geo_interface__, f)
        
