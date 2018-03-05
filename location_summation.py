#!Python3.6
# -*- coding: utf-8 -*-
#
# Imports
#
import sys
import googlemaps
import numpy as np

###############################################################################
#                                    MAIN                                     #
###############################################################################


def main(apikey):
    """
    This script checks which host minimizes the driving time for all involved
    by using Google Maps' API.

    You need an API Key and the module: googlemaps
    """

    # Establish connection to the cyber web
    gmaps = googlemaps.Client(key=apikey)

    # List of hosts, for prettier printing
    names = ["Knugen", "Steffe", "Gudrun", "Ebba"]

    # Dictionary of locations to
    locations = {"Knugen": "Drottningholm Palace, Ekerö, Sweden",
                 "Steffe": "Sveriges Riksdag, Stockholm, Sweden",
                 "Gudrun": "Agavägen 52, Lidingö, Sweden",
                 "Ebba": "Hantverkargatan 45, Stockholm, Sweden"}

    # Matrix to hold distances
    distance_matrix = np.zeros((len(locations), len(locations)))

    # Check distance between all locations
    for p1, place1 in enumerate(locations):
        for p2, place2 in enumerate(locations):
            if place1 != place2:

                result = gmaps.distance_matrix(locations[place1],
                                               locations[place2],
                                               mode="driving")

                # Extract the driving time in seconds
                for row in result["rows"]:
                    elements = row["elements"]
                    for element in elements:
                        duration = element["duration"]
                        distance_matrix[p1, p2] = duration["value"]

    # Find the node which minimizes total travelling distance
    summed_distances = list()
    for i in range(distance_matrix.shape[1]):
        sum_dist = np.sum(distance_matrix[:, i])
        host = names[i]
        summed_distances.append((sum_dist, host))

    summed_distances.sort()

    # Print the result
    print("\nBest place to be is at: {}".format(summed_distances[0][1]))
    print("Total driving time is: {:.0f} minutes\n".format(summed_distances[0][0]/60))

    print("Full list:")
    for (d, h) in summed_distances:
        print("Host: {}, Time: {:.0f} minutes".format(h, d/60))

###############################################################################
#                                    RUN                                      #
###############################################################################


if __name__ == "__main__":
    main(sys.argv[1])
