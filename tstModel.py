from model.category import Category
from model.model import Model

myModel = Model()
c = Category(7, "Road Bikes")
myModel.buildGraph(c)
n,e = myModel.getGraphDetails()
print(f"N nodi: {n} , N archi: {e}")
