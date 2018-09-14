# Datatable holds Two-dimensional size-mutable, tabular data structure 
# with labeled axes (rows and columns). Columns are categories and
# rows are series
class Datatable:

    # Init internal data and assigns null Element that is used to 
    # fill new series
    def __init__(self, nullElem):
        self.data = [['Titles']]    # creates a new empty list for each dog
        self.nullElem = nullElem    # creates a new empty list for each dog

    
    # Add a new serie and returns that serie
    def add_serie(self, name):
        newSerie = [name]
        dataCols = len(self.data[0]) - 1
        newSerie.extend([self.nullElem] * dataCols)
        self.data.append(newSerie)
        return newSerie
        
    # Add a new category and returns its index
    def add_category(self, name):
        rowCount = len(self.data)
        rowIndex = 0
        while rowIndex < rowCount:
            row = self.data[rowIndex]
            if rowIndex == 0:
                row.append(name)
            else:
                row.append(self.nullElem)
            rowIndex += 1
        return len(self.data[0]) - 1
            
    # Gets first serie by name
    def get_serie(self, name):
        seriesCount = len(self.data) - 1
        serie = None
        rowIndex = 1
        while rowIndex <= seriesCount:
            row = self.data[rowIndex]
            if name == row[0]:
                serie = row
            if not serie is None:
                break
            rowIndex += 1
        return serie

    # Gets first category index by name
    def get_category_index(self, name):
        categoryRow = self.data[0]
        categoriesCount = len(self.data[0]) - 1
        index = -1
        categoryIndex = 1
        while categoryIndex <= categoriesCount:
            if name == categoryRow[categoryIndex]:
                index = categoryIndex
            if index != -1:
                break
            categoryIndex += 1
        return index

    # Add sets serie value in a certain category. 
    # If a category with categoryName does't exists it is created otherwise 
    # category with categoryName is used. If a serie with serieName does't 
    # exists it is created otherwise serie with serieName is used
    def add(self, serieName, categoryName, value):
        serie = self.get_serie(serieName)
        if serie is None:
            serie = self.add_serie(serieName)
        categoryIndex = self.get_category_index(categoryName)
        if categoryIndex == -1:
            categoryIndex = self.add_category(categoryName)
        serie[categoryIndex] = value
            
