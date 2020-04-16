import json, configparser, os
import clean_data
# import pygeoj, shapely, shapefile

# IMPORT CONFIGURATIONS
parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['DEFAULT']


# TODO: NEED TO FINISH WRITING THIS FUNCTION
def rename_precincts(state):

    # IF STATE IS MARYLAND, THEN PERFORM THE FOLLOWING OPERATIONS
    if state == 'MD':

        precincts = []
        out = open(config['out_rel_dir'] + 'MD_precinct_names.txt', 'w')
        with open(config['MD_json']) as file:
            data = file.read()
            precinct_geoj = json.loads(data)

            # Write the geojson to the outfile with canonical names added
            md_counties = open(config['MD_dir'] + 'MD_counties_FIPS.txt', 'r')
            Lines = md_counties.readlines()
            county_dict = {}

            for line in Lines:
                compartments = line.split(',')
                compartments[1] = compartments[1].replace(' ', '')
                county_dict[compartments[1][0:5]] = compartments[0]

            for item in precinct_geoj['features']:
                item['properties']['COUNTY'] = county_dict[item['properties']['COUNTY']]
                item['properties']['CANON_NAME'] = item['properties']['COUNTY'] + "_" + item['properties']['NAME']

            out.write(json.dumps(precinct_geoj))

            file.close()
            out.close()

    elif state == 'FL':
        #TODO: We need to have full name for each county in the FL_geojson
        x = 4

if __name__ == '__main__':

    path = os.getcwd()
    if not os.path.exists(path + config['out_dir']):
        os.mkdir(path + config['out_dir'])

    rename_precincts('MD')

