import pygeoj
# import PyMySQL.cursors

# TODO geojson stuff
testfile = pygeoj.load(filepath="MD_precinct_lots_of_data.json")    # read geojson file

# for feature in testfile:                                          # iterate through each polygon
#     print(feature.properties)
#     print(feature.geometry.coordinates)
#     print(feature.geometry.type)                                  # either polygon or multipolygon
#     feature.properties =
#         {"newfield1":"newvalue1", "newfield2":"newvalue2"}        # set your own properties

# print(len(testfile))                                              # print the amount of polygons
# testfile.remove_feature(8)                                        # delete feature 8
# testfile.save("test_edit.geojson")                                # save json file to a different path
# newfile = pygeoj.new()                                            # create new geojson file
# newfile.add_unique_id()                                           # create unique ids

# TODO use case 11 -> precinct renaming



# TODO use case 12 -> data error data structure



# TODO use case 14 -> identify enclosed precincts



# TODO use case 15 -> identify overlapping precincts
from shapely.geometry import Polygon

for feature in testfile:
    poly = Polygon(feature.geometry.coordinates)
    print(poly)
    for f in testfile:
        my_poly = Polygon(f.geometry.coordinates)
        if poly.intersects(my_poly):
            print("interection at : " + str(feature.properties[2]))

# TODO use case 16 -> identify map coverage errors (ghost precincts)



# TODO use case 19 -> identify anomalous precinct data (pop/voting data is zero, unreasonable precentages)



# TODO use case 18 -> classify map coverage errors (might be incorperated in other use cases)



# TODO use case 21 -> identify precinct neigbors (works but goes to print statements)
import geopandas as gp

df = gp.read_file("MD_precinct_lots_of_data.json")
df["neighbors"] = None

for index, row in df.iterrows():
    neighbors = df[df.geometry.touches(row['geometry'])].NAME.tolist()
    # neighbors = neighbors.remove(row.name)
    df.at[index, "neighbors"] = ", ".join(neighbors)
    print(str(row.NAME) + " -> " + str(neighbors))         # row.NAME is the precinct and neighbors is a list of its neighbors

# df.to_file("new_file.json")       # saving file as a shp file not json

# # TODO mysql stuff use case 13 -> store data in DB
#
# # connect to database
# connection = pymysql.connect(host=dbServerName,
#                                user=user,
#                                password=password,
#                                db=db,
#                                charset=charSet,
#                                cursorclass=pymysql.cursors.DictCursor)
#
# try:
#     with connection.cursor() as cursor:
#         # query state table for maryland
#         sql = "SELECT `id` FROM `state` WHERE `name`=%s"
#         cursor.execute(sql, ('Maryland', ))
#         # check result to make sure it was successful
#         result = cursor.fetchone()
#         MD_id = result[id]
#         print(MD_id)
#     # commit to save changes
#     connection.commit()
#     with connection.cursor() as cursor:
#         # create queries
#         district_query = []
#         precinct_query = []
#         demo_query = []
#         election_query = []
#         # once have all queries write to db
#         cursor.executemany("INSERT INTO district (id, name, state_id) VALUES (%s, %s, %s)", district_query)
#         cursor.executemany("INSERT INTO precinct (id, name, state_id, district_id, county_id) VALUES (%s, %s, %s, %s, %s)", precinct_query)
#         cursor.executemany("INSERT INTO demo (id, total_pop, total_white, total_black, total_asian) VALUES (%s, %s, %s, %s, %s)", demo_query)
#         cursor.executemany("INSERT INTO election (id, total_votes, total_dem, total_rep, total_other) VALUES (%s, %s, %s, %s, %s)", election_query)
#     # commit to save changes
#     connection.commit()
# finally:
#     connection.close()
