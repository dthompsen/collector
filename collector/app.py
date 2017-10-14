import wx
from collection import Collection
from ui import UI

if __name__ == "__main__":
    collection = Collection()
    collection.readCsv('data.csv')
    collection.buildIndex()
    
    app = wx.App()
    form = MyForm(collection)
    frame = form.Show()
    
    app.MainLoop()

    
    
