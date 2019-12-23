import wx
import Model
import os
import pickle


"""
Define Progress Bar
"""
class MyProgBar(wx.Panel):
    def __init__(self, parent, id=-1, position=(0, 0), size=(20, 100), prog=50):
        self.myWidth = size[0]
        self.myHeight = size[1]
        self.myprogress = 0
        self.myerror = 0
        self.BasePanel = wx.Panel(parent, id, position, size, wx.BORDER)
        self.ProgPanel = wx.Panel(self.BasePanel, -1, (0, 0), (1, self.myHeight))
        self.bgcolor = wx.WHITE
        self.progcolor = wx.GREEN
        self.errcolor = wx.RED
        self.BasePanel.SetBackgroundColour(self.bgcolor)
        self.SetProgress(0)

    def SetProgress(self, prog=50, error=0):
        width = self.myWidth * prog / 100
        self.myerror = error
        if (prog < 0):
            prog = 0
        if (prog > 100):
            prog = 100
        self.myprogress = prog
        width = self.myWidth * prog / 100
        if (width < 1):
            width = 1
        if (error):
            self.ProgPanel.SetBackgroundColour(self.errcolor)
        else:
            self.ProgPanel.SetBackgroundColour(self.progcolor)
        self.ProgPanel.SetSize((0, 0))
        self.ProgPanel.SetSize((width, self.myHeight))

    def SetBGColor(self, color=wx.WHITE):
        self.bgcolor = color
        self.BasePanel.SetBackgroundColour(color)

    def SetProgColor(self, color=wx.GREEN):
        self.progcolor = color
        self.ProgPanel.SetBackgroundColour(color)

    def SetErrColor(self, color=wx.RED):
        self.errcolor = color

    def GetProgress(self):
        return self.myprogress


"""
Define Progress Bar Frame
"""
class ProgressBarFrame(wx.Frame):
    def __init__(self,parent, id, title, position, size):
        wx.Frame.__init__(self,parent, id, title, position, size)

        self.topPanel = wx.Panel(self)
        self.bottomPanel = wx.Panel(self)
        self.Text = wx.StaticText(self.topPanel, label="   ")
        self.BlankText = wx.StaticText(self.topPanel, label="   ")
        self.progress = MyProgBar(self.bottomPanel, -1, (15, 10), (300, 20))
        self.progress.SetBGColor(wx.WHITE)
        self.progress.SetProgColor(wx.GREEN)
        self.progress.SetErrColor(wx.RED)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(self.BlankText, 0, wx.EXPAND, 1)
        topSizer.Add(self.Text, 0, wx.EXPAND, 1)
        self.topPanel.SetSizer(topSizer)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(self.topPanel, 0, wx.EXPAND, 1)
        Sizer.Add(self.bottomPanel, 0, wx.EXPAND, 1)

        self.SetBackgroundColour('WHITE')

        self.SetSizer(Sizer)

        self.Centre()

        self.Show(True)


"""
Define Main Interface
"""
class MainFrame(wx.Frame):

    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self, parent, id, title, position, size)
        # Set Background
        self.SetBackgroundColour('WHITE')
        # Define Panel
        self.UpperPanel = wx.Panel(self)
        self.MiddlePanel = wx.Panel(self)
        self.LowerPanel = wx.Panel(self)
        self.LowerPanel1 = wx.Panel(self.LowerPanel)
        self.LowerPanel2 = wx.Panel(self.LowerPanel)
        self.LowerPanel3 = wx.Panel(self.LowerPanel)
        self.LowerPanel4 = wx.Panel(self.LowerPanel)
        self.LowerPanel5 = wx.Panel(self.LowerPanel)
        self.LowerPanel6 = wx.Panel(self.LowerPanel)
        # Define objects in UpperPanel
        self.TrainLabel = wx.StaticText(self.UpperPanel, label='*Please train the model before proceeding to evaluate')
        self.TrainButton = wx.Button(self.UpperPanel, -1, 'Train')
        self.AccuracyLabel = wx.StaticText(self.UpperPanel, label='Accuracy: ')
        self.TrainButton.Bind(wx.EVT_BUTTON, self.train)
        UpperSizer = wx.BoxSizer(wx.VERTICAL)
        UpperSizer.Add(self.TrainLabel, 0.5, wx.EXPAND)
        UpperSizer.Add(self.TrainButton, 1, wx.BOTTOM, border=5)
        UpperSizer.Add(self.AccuracyLabel, 1, wx.EXPAND | wx.BOTTOM, border=10)
        self.UpperPanel.SetSizer(UpperSizer)
        # Define objects in MiddlePanel
        self.EvaluateText = wx.TextCtrl(self.MiddlePanel, style=wx.SUNKEN_BORDER, size=(150, 100))
        self.EvaluateButton = wx.Button(self.MiddlePanel, -1, 'Evaluate')
        self.EvaluateButton.Bind(wx.EVT_BUTTON, self.evaluate)
        MiddleSizer = wx.BoxSizer(wx.HORIZONTAL)
        MiddleSizer.Add(self.EvaluateText, 1, wx.EXPAND)
        MiddleSizer.Add(self.EvaluateButton, 0.5, wx.EXPAND | wx.LEFT, border=10)
        self.MiddlePanel.SetSizer(MiddleSizer)
        # Define objects in LowerPanel
        self.ToxicLabel = wx.StaticText(self.LowerPanel1, label='Toxic: ')
        self.ToxicValue = wx.TextCtrl(self.LowerPanel1, style=wx.SUNKEN_BORDER | wx.TE_READONLY, size=(50, -1))
        LowerSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        LowerSizer1.Add(self.ToxicLabel, 1)
        LowerSizer1.Add(self.ToxicValue, 1, wx.RIGHT, border=5)
        self.LowerPanel1.SetSizer(LowerSizer1)
        self.SevereToxicLabel = wx.StaticText(self.LowerPanel2, label='Severe Toxic: ')
        self.SevereToxicValue = wx.TextCtrl(self.LowerPanel2, style=wx.SUNKEN_BORDER | wx.TE_READONLY, size=(50, -1))
        LowerSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        LowerSizer2.Add(self.SevereToxicLabel, 1)
        LowerSizer2.Add(self.SevereToxicValue, 1, wx.RIGHT, border=5)
        self.LowerPanel2.SetSizer(LowerSizer2)
        self.ObsceneLabel = wx.StaticText(self.LowerPanel3, label='Obscene: ')
        self.ObsceneValue = wx.TextCtrl(self.LowerPanel3, style=wx.SUNKEN_BORDER | wx.TE_READONLY, size=(50, -1))
        LowerSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        LowerSizer3.Add(self.ObsceneLabel, 1)
        LowerSizer3.Add(self.ObsceneValue, 1, wx.RIGHT, border=5)
        self.LowerPanel3.SetSizer(LowerSizer3)
        self.ThreatLabel = wx.StaticText(self.LowerPanel4, label='Threat: ')
        self.ThreatValue = wx.TextCtrl(self.LowerPanel4, style=wx.SUNKEN_BORDER | wx.TE_READONLY, size=(50, -1))
        LowerSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        LowerSizer4.Add(self.ThreatLabel, 1)
        LowerSizer4.Add(self.ThreatValue, 1, wx.RIGHT, border=5)
        self.LowerPanel4.SetSizer(LowerSizer4)
        self.InsultLabel = wx.StaticText(self.LowerPanel5, label='Insult: ')
        self.InsultValue = wx.TextCtrl(self.LowerPanel5, style=wx.SUNKEN_BORDER | wx.TE_READONLY, size=(50, -1))
        LowerSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        LowerSizer5.Add(self.InsultLabel, 1)
        LowerSizer5.Add(self.InsultValue, 1, wx.RIGHT, border=5)
        self.LowerPanel5.SetSizer(LowerSizer5)
        self.IdentityHateLabel = wx.StaticText(self.LowerPanel6, label='Identity Hate: ')
        self.IdentityHateValue = wx.TextCtrl(self.LowerPanel6, style=wx.SUNKEN_BORDER | wx.TE_READONLY, size=(50, -1))
        LowerSizer6 = wx.BoxSizer(wx.HORIZONTAL)
        LowerSizer6.Add(self.IdentityHateLabel, 1)
        LowerSizer6.Add(self.IdentityHateValue, 1, wx.RIGHT, border=5)
        self.LowerPanel6.SetSizer(LowerSizer6)
        # Define Lower Sizer
        self.CommentLabel = wx.StaticText(self.LowerPanel, label='*[0] is absent, while [1] is present')
        self.CommentLabel.SetForegroundColour("BLUE")
        LowerSizer = wx.BoxSizer(wx.VERTICAL)
        LowerSizer.Add(self.LowerPanel1, 1, wx.EXPAND | wx.ALL, border=5)
        LowerSizer.Add(self.LowerPanel2, 1, wx.EXPAND | wx.ALL, border=5)
        LowerSizer.Add(self.LowerPanel3, 1, wx.EXPAND | wx.ALL, border=5)
        LowerSizer.Add(self.LowerPanel4, 1, wx.EXPAND | wx.ALL, border=5)
        LowerSizer.Add(self.LowerPanel5, 1, wx.EXPAND | wx.ALL, border=5)
        LowerSizer.Add(self.LowerPanel6, 1, wx.EXPAND | wx.ALL, border=5)
        LowerSizer.Add(self.CommentLabel, 1, wx.EXPAND | wx.ALL, border=5)
        self.LowerPanel.SetSizer(LowerSizer)
        # Define Main Sizer
        font = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.Step1Label = wx.StaticText(self, label='Step 1:')
        self.Step2Label = wx.StaticText(self, label='Step 2:')
        self.Step1Label.SetFont(font)
        self.Step2Label.SetFont(font)
        self.Step1Label.SetForegroundColour("CORNFLOWER BLUE")
        self.Step2Label.SetForegroundColour("CORNFLOWER BLUE")
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(self.Step1Label, 1, wx.EXPAND | wx.ALL, border=5)
        MainSizer.Add(self.UpperPanel, 1, wx.EXPAND | wx.ALL, border=10)
        MainSizer.Add(self.Step2Label, 1, wx.EXPAND | wx.ALL, border=5)
        MainSizer.Add(self.MiddlePanel, 1, wx.EXPAND | wx.ALL, border=10)
        MainSizer.Add(self.LowerPanel, 1, wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(MainSizer)

        self.Centre()

        self.Show(True)

        return None

    def train(self, event):
        dlgProgress = ProgressBarFrame(None, -1, "Training", wx.DefaultPosition, (350, 120))
        dlgProgress.Show()
        dlgProgress.Text.SetLabel("     Training Datasets...")
        dlgProgress.Update()
        train, test = Model.read()
        dlgProgress.progress.SetProgress(50)
        dlgProgress.Update()
        accuracy, vect_word = Model.train(train, test)
        dlgProgress.progress.SetProgress(85)
        dlgProgress.Update()
        pickle.dump(vect_word, open('tfidf/vec.pkl', 'wb'))
        message = "Accuracy:\n"
        for col, score in accuracy.items():
            message = message + "  " + str(col) + ": " + str('{0:.2f}'.format(score))
        self.AccuracyLabel.SetLabelText(message)
        dlgProgress.progress.SetProgress(100)
        dlgProgress.Update()
        dlgProgress.Hide()
        dlgProgress.Close()

    def evaluate(self, event):
        if len(os.listdir('models')) == 0:
            wx.MessageBox('please train the model first.')
            return
        if self.EvaluateText == "":
            wx.MessageBox('please enter the evaluate text.')
            return
        vect_word = pickle.load(open('tfidf/vec.pkl', 'rb'))
        scores = Model.predict(vect_word, str(self.EvaluateText.Value))
        self.ToxicValue.SetLabelText(str(scores['toxic']))
        self.SevereToxicValue.SetLabelText(str(scores['severe_toxic']))
        self.ObsceneValue.SetLabelText(str(scores['obscene']))
        self.ThreatValue.SetLabelText(str(scores['threat']))
        self.InsultValue.SetLabelText(str(scores['insult']))
        self.IdentityHateValue.SetLabelText(str(scores['identity_hate']))


if __name__ == '__main__':
    app = wx.App()
    dlg = MainFrame(None, -1, "Evaluate Toxic Comment", wx.DefaultPosition, (560, 585))
    dlg.Show()
    app.MainLoop()