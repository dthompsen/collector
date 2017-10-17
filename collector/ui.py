import wx
import wx.grid as gridlib
import os.path

class UI(wx.Frame):
    def __init__(self, collection):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Collector")
        self.SetInitialSize((1600,900))
        self.MaxImageSize = 800
        
        self.panel = wx.Panel(self)
        self.collection = collection
        self.rowCnt = len(self.collection.getRows())
        self.colCnt = len(self.collection.getColnames())
        self.curRow = 0
        self.curQuery = ""
        self.findRownums = []  # list of rownums that were found to match query
        self.findIndex = None # current index into findRownums

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        prevBtn = wx.Button(self.panel, label='Prev')
        prevBtn.Bind(wx.EVT_BUTTON, self.OnPrevBtnClick)
        nextBtn = wx.Button(self.panel, label='Next')
        nextBtn.Bind(wx.EVT_BUTTON, self.OnNextBtnClick)
        findBtn = wx.Button(self.panel, label='Find')
        findBtn.Bind(wx.EVT_BUTTON, self.OnFindBtnClick)
        self.findTxt = wx.TextCtrl(self.panel)
        hbox1.Add(prevBtn)
        hbox1.Add(nextBtn)
        hbox1.Add(self.findTxt, proportion=1)
        hbox1.Add(findBtn)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = gridlib.Grid(self.panel)
        self.grid.CreateGrid(self.rowCnt, self.colCnt)
        self.loadGrid(self.collection.getRows(), self.collection.getColnames())
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        img = wx.Image(self.MaxImageSize, self.MaxImageSize)
        self.imageCtrl = wx.StaticBitmap(self.panel, id=wx.ID_ANY, bitmap=wx.Bitmap(img),
                                         size=wx.Size(self.MaxImageSize, self.MaxImageSize))
        hbox2.Add(self.grid)
        hbox2.Add(self.imageCtrl)

        vbox = wx.BoxSizer(wx.VERTICAL)        
        vbox.Add(hbox1, proportion=0, flag=wx.ALL, border=5)
        vbox.Add(hbox2, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.panel.SetSizer(vbox)

        if self.rowCnt > 0:
            self.curRow = 0
            self.WhenRowChanged()

    def WhenRowChanged(self):
        self.grid.SelectRow(self.curRow)
        self.loadRowImage(self.curRow)

    def OnSelectCell(self, evt):
        if self.curRow == None or self.curRow != evt.GetRow():
            self.curRow = evt.GetRow()
            self.WhenRowChanged()
        evt.Skip()

    def OnPrevBtnClick(self, evt):
        if self.curRow > 0:
            self.curRow = self.curRow - 1
            self.grid.SetGridCursor(self.curRow, 0)
            self.WhenRowChanged()

    def OnNextBtnClick(self, evt):
        if self.curRow < self.rowCnt - 1:
            self.curRow = self.curRow + 1
            self.grid.SetGridCursor(self.curRow, 0)
            self.WhenRowChanged()

    def OnFindBtnClick(self, evt):
        query = self.findTxt.GetValue().strip()
        if query == "":
            # Blank query - reset if had non-blank query before
            if self.curQuery != "":
                self.unhighlight()
                self.curQuery = ""
                self.findRownums = []
                self.findIndex = None
        elif query == self.curQuery:
            # same query - select next one found
            if self.findIndex < len(self.findRownums) - 1:
                self.findIndex = self.findIndex + 1
                self.curRow = self.findRownums[self.findIndex]
                self.grid.SetGridCursor(self.curRow, 0)
                self.WhenRowChanged()
            else:
                print("last one") # TODO _ display in new status label
        else:
            # New query
            self.unhighlight()
            self.curQuery = query
            # returns list of row numbers that match query
            self.findRownums = self.collection.find(self.curQuery)
            print('Results: ', self.findRownums)
            if self.findRownums:
                self.highlight(self.findRownums)
                self.curRow = self.findRownums[0]
                self.findIndex = 0
                self.WhenRowChanged()
            else:
                self.findIndex = None

    def highlight(self, rownums):
        if len(rownums) == 0:
            return
        color = (204, 255, 204) # RGB light green
        for rownum in rownums:
            attr = gridlib.GridCellAttr()
            attr.SetBackgroundColour(color)
            self.grid.SetRowAttr(rownum, attr)
        self.grid.ForceRefresh()

    def unhighlight(self):
        if len(self.findRownums) == 0:
            return
        color = (255, 255, 255)  # RGB white
        for rownum in self.findRownums:
            attr = gridlib.GridCellAttr()
            attr.SetBackgroundColour(color)
            self.grid.SetRowAttr(rownum, attr)
        self.grid.ForceRefresh()

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

    def loadRowImage(self, row):
        id = self.grid.GetCellValue(row, 0)
        country = self.grid.GetCellValue(row, 1)
        self.loadImage(country, id)

    def loadImage(self, country, id):
        filepath = 'E:\\DaveSync\\Stamps\\countries\\' + country + '\\S' + str(id) + '.jpg'
        if not os.path.isfile(filepath):
            filepath = 'logo.jpg'
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image to fit, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.MaxImageSize
            NewH = self.MaxImageSize * H / W
        else:
            NewH = self.MaxImageSize
            NewW = self.MaxImageSize * W / H
        img = img.Scale(NewW, NewH)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.panel.Refresh()