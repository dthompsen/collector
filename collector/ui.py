import wx
import wx.grid as gridlib

class UI(wx.Frame):
    def __init__(self, collection):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Collector")
        self.SetInitialSize((1200,800))
        
        panel = wx.Panel(self)
        self.collection = collection
        self.rowCnt = len(self.collection.getRows())
        self.colCnt = len(self.collection.getColnames())
        self.highlightedRownums = []
 
        self.grid = gridlib.Grid(panel)
        self.grid.CreateGrid(self.rowCnt, self.colCnt)
        self.loadGrid(self.collection.getRows(), self.collection.getColnames())
 
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.findTxt = wx.TextCtrl(panel)
        findBtn = wx.Button(panel, label='Find')
        findBtn.Bind(wx.EVT_BUTTON, self.OnFindBtnClicked)
        hbox.Add(self.findTxt)
        hbox.Add(findBtn)
        
        vbox = wx.BoxSizer(wx.VERTICAL)        
        vbox.Add(hbox, proportion=0, flag=wx.ALL, border=5)
        vbox.Add(self.grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)       
        panel.SetSizer(vbox)

    def OnFindBtnClicked(self, evt):
        self.unhighlight()
        query = self.findTxt.GetValue()
        print('Query {}'.format(query))
        if query:
            # returns list of row numbers that match query
            results = self.collection.find(query)
            print('Results: ', results)
            if results:
                self.highlight(results)

    def highlight(self, rownums):
        color = (204, 255, 204) # RGB light green
        for rownum in rownums:
            print('Highlighting row {}'.format(rownum))
            attr = gridlib.GridCellAttr()
            attr.SetBackgroundColour(color)
            self.grid.SetRowAttr(rownum, attr)
        self.grid.ForceRefresh()
        self.highlightedRownums = rownums

    def unhighlight(self):
        color = (255, 255, 255)  # RGB white
        for rownum in self.highlightedRownums:
            print('Unhighlighting row {} using color {}'.format(rownum, color))
            attr = gridlib.GridCellAttr()
            attr.SetBackgroundColour(color)
            self.grid.SetRowAttr(rownum, attr)
        self.grid.ForceRefresh()
        self.highlightedRownums = []

    def loadGrid(self, rows, colnames):
        colnum = 0
        for colname in colnames:
            self.grid.SetColLabelValue(colnum, colname)
            colnum = colnum + 1
        rownum = 0
        for row in rows:
            colnum = 0
            for colname in colnames:
                self.grid.SetCellValue(rownum, colnum, row[colname])
                colnum = colnum + 1
            rownum = rownum + 1
 