import wx #GUI
import wolframalpha #API to communicate with Wolfram Alpha
import wikipedia #API to communicate with Wikipedia
import pyttsx3 as speak #Text to speech library
import speech_recognition as speech #Voice recognition library

#Welcome note at the beginning of App START
engine = speak.init()
engine.say("Welcome Avenger! What can I do for you?")
engine.runAndWait()

# obtain audio from the microphone
r = speech.Recognizer()
with speech.Microphone() as source:
    print("Ask now")
    audio = r.listen(source)
try:
    audio_recognized = r.recognize_google(audio)
except speech.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except speech.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

#VirtualFrame is a class and take cares of the GUI stuff
class VirtualFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, pos=wx.DefaultPosition,
                          size=wx.Size(450, 100), style=wx.MINIMIZE_BOX |
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title="Virtual Assistant")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(
            panel, label="Hello, I am your virtual assistant. How can I help you?")
        my_sizer.Add(label, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(
            panel, style=wx.TE_PROCESS_ENTER, size=(400, 30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        self.txt.SetValue(audio_recognized)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    #This method will trigger once the ENTER button is hit and gets the responses from the API's
    def OnEnter(self, event):
        input = self.txt.GetValue().lower()
        try:
            appID = "Set the API key here provided by signing into Wolfram Alpha developer community"
            client = wolframalpha.Client(appID)
            result = client.query(input)
            answer = next(result.results).text
            print(answer)
            engine.say("For your request "+ input + "this is what I found on Wolf Ram Alpha "  + answer)
            engine.runAndWait()
        except:
            answer = wikipedia.summary(input)
            print(answer)
            engine.say("For your request "+ input + "this is what I found on Wikipedia "  + answer)
            engine.runAndWait()


if __name__ == "__main__":
    app = wx.App(True)
    frame = VirtualFrame()
    app.MainLoop()
