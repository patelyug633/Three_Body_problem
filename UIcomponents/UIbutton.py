class button:
    def __init__(self, Uim, info_panel = None):
        self.size = (10, 670)
        self.text = "Add text"
        self.manager = Uim
        self.container = info_panel
        self.object_id = '#button'
    
    
    
    def setSize(self, size):
        self.size = size
    
    def setText(self, text):
        self.text = text
    
    def setobjectID(self, object_id):
        self.object_id = object_id
    
    def setUiManager(self, Uim):
        self.manager = Uim
    
    def setContainer(self, info_panel):
        self.container = info_panel
    
    