from .datatable import Datatable
import copy

# Graphdata extends Datatable to hold data for graphics
class Graphdata(Datatable):

    def __init__(self, nullElem):
        Datatable.__init__(self, nullElem)
        
    # Load data from a tuple of tuples in the form 
    # (
    #   (serieName1, categoryName1, value1), 
    #   (serieName2, categoryName2, value2), ...
    # )
    def load(self, data):
        for tuple in data:
            self.add(str(tuple[0]), str(tuple[1]), tuple[2])
            
    # Returns all categories
    def get_categories(self):
        row = copy.copy(self.data[0])
        row.pop(0)
        return row

    # Returns all categories
    def get_series(self):
        rowIndex = 1
        rowCount = len(self.data)
        series = []
        while rowIndex < rowCount:
            dataSerie = self.data[rowIndex]
            serie = {}
            serie["name"] = dataSerie[0]
            data = copy.copy(dataSerie)
            data.pop(0)
            serie["data"] = data
            series.append(serie)
            rowIndex += 1
        return series

    
