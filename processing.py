
import csv
from functools import cache
import math

class Process:
    def __init__(self, mode) -> None:
        self.mode = mode
        self.colors = ["red", "yellow", "blue"]

        data = [[],[],[]]
        if self.mode == "predict":
            for color_pointy in range(len(self.colors)):
                #print(self.colors[color_pointy])
                with open(self.colors[color_pointy] + '.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    data[color_pointy].append([values for values in reader])

        self.data = data



    def train(self, color_name, colors_from_object):
        pass
    
    def predict(self, colors) -> list[str, int]:
        """
        :argument takes four color values
        searches for the closest color match from the classified color values
        :returns the color it thinks it sees and its certaity
        """
        distances_to_colors = [None, None, None]
        for color_pointy in range(len(self.colors)):
            color_name = self.colors[color_pointy]
            distances_to_colors[color_pointy] = sum([self.get_shortest_distace(values, self.data[color_pointy]) for values in colors])
        prediction = self.colors[distances_to_colors.index(min(distances_to_colors))]
        certainty = min(distances_to_colors)
        return [prediction, certainty]
    
    def get_shortest_distace(self, color, known_colors) -> float:
        shortest_dist = 1000000
        #print(color)
        #print(known_colors[0])
        for known in known_colors[0]:
            #print(int(color[1])- int(known[1]))
            #print(int(known[0]))
            distance = math.sqrt((int(known[0]) - int(color[0])) ** 2 + (int(known[1]) - int(color[1])) ** 2 + (int(known[2]) - int(color[2])) ** 2)
            if distance < shortest_dist:
                shortest_dist = distance
        return shortest_dist


