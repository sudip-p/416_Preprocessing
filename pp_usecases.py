import json, configparser, os
import clean_data
# import pygeoj, shapely, shapefile

# IMPORT CONFIGURATIONS
parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['DEFAULT']


def rename_precincts(state):

    # IF STATE IS MARYLAND, THEN THE ONLY DATA MISSING FROM MD_JSON
    # IS COUNTY NAME AND CANONICAL NAME. WE ADD THOSE TO THE JSON OBJECT AND
    # CREATE A NEW OUT FILE IN ./out/
    if state == 'MD':

        out = open(config['out_rel_dir'] + 'MD_precinct.json', 'w')
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
            md_counties.close()

    elif state == 'FL':
        #TODO: We need to have full name for each county in the FL_geojson
        county_file = open(config['FL_dir'] + 'fl_counties_full.txt')
        counties_str = county_file.read()
        fl_counties = counties_str.split("\n")
        county_file.close()

        abbrev_file = open(config['FL_dir'] + "fl_counties_abbrev.txt")
        abbrev_str = abbrev_file.read()
        abbrevs = abbrev_str.split("\n")
        abbrev_file.close()

        fl_county_dict = {}
        for i in range(len(fl_counties)):
            fl_county_dict[abbrevs[i]] = fl_counties[i]

        abbrevs_used = {}
        for i in range(len(abbrevs)):
            abbrevs_used[abbrevs[i]] = False

        # Iterate thru fl precinct lines json and set values in abbrevs_used to True if it is found in json
        with open(config['FL_json']) as file:
            str_data = file.read()
            fl_geojson = json.loads(str_data)

            for item in fl_geojson['features']:
                if item['properties']['county'] in abbrevs_used:
                    abbrevs_used[item['properties']['county']] = True

        file.close()

        # print("Abbrevs\tCounty")
        # for item in abbrevs_used:
        #     if abbrevs_used[item] == False:
        #         print(item,"\t",fl_county_dict[item])

        # added new keys
        fl_county_dict['ALA'] = fl_county_dict['ALC']
        fl_county_dict['CAL'] = fl_county_dict['CAH']
        fl_county_dict['CLL'] = fl_county_dict['CLR']
        fl_county_dict['FLA'] = fl_county_dict['FLG']
        fl_county_dict['IND'] = fl_county_dict['IDR']
        fl_county_dict['MAN'] = fl_county_dict['MTE']
        fl_county_dict['MRN'] = fl_county_dict['MAO']
        fl_county_dict['WAS'] = fl_county_dict['WAG']

        # delete old keys
        del(fl_county_dict['ALC'])
        del(fl_county_dict['CAH'])
        del(fl_county_dict['CLR'])
        del(fl_county_dict['FLG'])
        del(fl_county_dict['IDR'])
        del(fl_county_dict['MTE'])
        del(fl_county_dict['MAO'])
        del(fl_county_dict['WAG'])

        for item in fl_geojson['features']:
            item['properties']['COUNTY_FULLNAME'] = fl_county_dict[item['properties']['county']]
            item['properties']['CANON_NAME'] = item['properties']['COUNTY_FULLNAME'] + "_" + item['properties']["pct"]

        with open(config['out_rel_dir'] + 'FL_precinct.json', 'w') as outfile:

            json_str = json.dumps(fl_geojson)
            outfile.write(json_str)

        outfile.close()

    # IF STATE = NY, SIMPLY ADD A CANONICAL NAME ELEMENT TO THE JSON
    elif state == 'NY':

        with open(config['NY_json']) as file:
            x = 3


    else:
        raise ValueError("Wrong parameters used for rename_precincts()")

if __name__ == '__main__':

    path = os.getcwd()
    if not os.path.exists(path + config['out_dir']):
        os.mkdir(path + config['out_dir'])

    rename_precincts('MD')
    # rename_precincts("FL")
    # rename_precincts('NY')
