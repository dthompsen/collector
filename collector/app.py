import wx
from collector.collection import Collection
from collector.ui import UI

COLLECTION_FILE_PATH = 'E:\DaveSync\Stamps\stamps.csv'

if __name__ == "__main__":
    collection = Collection()
    collection.readCsv(COLLECTION_FILE_PATH)
    collection.buildIndex()
    
    app = wx.App()
    form = UI(collection)
    frame = form.Show()
    
    app.MainLoop()

    
    
