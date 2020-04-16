import json, configparser, os
import clean_data
# import pygeoj, shapely, shapefile

# IMPORT CONFIGURATIONS
parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['DEFAULT']

# TODO: NEED TO FINISH WRITING THIS FUNCTION
def rename_precincts(state):
    if state == 'MD':
        # IF STATE IS MARYLAND, THEN
        precincts = []
        out = open(config['out_rel_dir'] + 'MD_precinct_names.txt', 'w')
        with open(config['MD_json']) as file:
            data = file.read()
            precinct_geoj = json.loads(data)

            for f in precinct_geoj['features']:
                out.write(f['properties']['NAME'] + "\n")

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

