from tkinter import *
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from os import listdir, getcwd, remove
from os.path import isfile, join

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Initialization -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
app = Tk()
app.title("Create, Learn, Repeat !")
app.geometry("400x500")
app.resizable(width = False, height = False)
app.wm_attributes('-transparentcolor','green')

canvas = Canvas(app, height = 500, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.pack()

backgroundImage = ImageTk.PhotoImage(Image.open("data/img/background.png").resize((800, 1100)))
backImage = ImageTk.PhotoImage(Image.open("data/img/back.png").resize((32, 32)))
logoandnameImage = ImageTk.PhotoImage(Image.open("data/img/logoandname_white.png").resize((64,32)))


iconImage = ImageTk.PhotoImage(Image.open("data/img/logo.png"))
app.iconphoto(False, iconImage)

myFontBig = ("Bahnschrift 40")
myFontLittle = ("Bahnschrift 13 italic")

combostyle = ttk.Style()

combostyle.theme_create("combostyle", parent="alt",
                         settings = {"TCombobox":
                                     {"configure":
                                      {"selectbackground": "#396287",
                                       "fieldbackground": "#2C5F8D",
                                       "foreground": "white"
                                       }}}
                         )

combostyle.theme_use('combostyle')


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Usefull functions -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def clear():
    canvas.delete("all")
    canvas.create_image(0, 0, image = backgroundImage)
    canvas.create_image(360, 480, image = logoandnameImage)

def MakeLabel(label):
    canvas.tag_bind(label, "<Enter>", lambda event: enterLabel(event, label))
    canvas.tag_bind(label, "<Leave>", lambda event: leaveLabel(event, label))

def enterLabel(event, label):
    canvas.itemconfig(label, fill = "white")

def leaveLabel(event, label):
    canvas.itemconfig(label, fill = "#dbdbdb")


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Saving cards -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def saveQuestion(event, questionEntry, answerEntry, groupCombo):
    question = questionEntry.get()
    answer = answerEntry.get()
    group = groupCombo.get()

    if question == "" and answer == "":
        messagebox.showerror("Error", "You have to fill both entry.")
    elif question == "":
        messagebox.showerror("Error", "You have to fill the 'Question' entry.")
    elif answer == "":
        messagebox.showerror("Error", "You have to fill the 'Answer' entry.")
    elif group == "":
        messagebox.showerror("Error", "Please give a name to your group.")
    elif group == "Create a new group":
        messagebox.showerror("Error", "Please choose an other group or name a new one.")
    elif "~" in group:
        messagebox.showerror("Error", "'~' : This character is not allowed")
    else:
        fileGroup = "data/" + group + ".txt"
        try:
            with open(fileGroup, "r") as file:
                data = file.readlines()

        except FileNotFoundError:
            with open(fileGroup, "w") as file:
                file.write("")

            with open(fileGroup, "r") as file:
                data = file.readlines()

        data.append(question + "\n")
        data.append(answer + "\n")

        with open(fileGroup, "w") as file:
            for i in range(len(data)):
                file.write(data[i])

        Add_Card_GUI(True)

def Add_Card_GUI(event):
    clear()

    questionLabel = canvas.create_text(200, 50, text = "Question", fill = "#dbdbdb", font = myFontBig)
    questionEntry = Entry(canvas, bg = "#2C5F8D", width = "40", font = myFontLittle, fg = "white", justify = "center", relief = "flat")
    canvas.create_window(200,110,window = questionEntry)

    answerLabel = canvas.create_text(200, 180, text = "Answer", fill = "#dbdbdb", font = myFontBig)
    answerEntry = Entry(canvas, bg = "#256A85", width = "40", font = myFontLittle, fg = "white", justify = "center", relief = "flat")
    canvas.create_window(200, 250, window = answerEntry)

    groupLabel = canvas.create_text(50, 330, text = "Group", fill = "#dbdbdb", font = myFontLittle)

    path = getcwd() + "/data"
    groupnames = [f for f in listdir(path) if isfile(join(path, f))]
    groupList = ["Create a new group"]

    for element in groupnames:
        if element.endswith(".txt"):
            groupList.append(element.replace(".txt", ""))

    groupCombo = ttk.Combobox(app, values = groupList, width = "27", font = myFontLittle)
    groupCombo.current(0)
    canvas.create_window(225, 330, window = groupCombo)

    SubmitButton = canvas.create_text(200, 400, text = "Submit", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(SubmitButton)

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", Del_Add_GUI)


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Deleting cards -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def Del_Card(event, questionList):
    selected = questionList.curselection()

    try:
        selectedQuestion = questionList.get(selected)
        found = False
        name = ""
        quest = ""
        for char in selectedQuestion:
            if char == "~":
                found = True
            if found == True:
                name += char
            if found == False:
                quest += char

        quest = quest[:-1]
        filename = name.replace("~ ", "").replace(" ~", "").replace("\n", "")

        path = "data/" + filename + ".txt"

        with open(path, "r") as file:
            data = file.readlines()

        index = ""

        for i in range(len(data)):
            if data[i].replace("\n", "") == quest:
                index = i
                del data[i]
                del data[i]
                break

        if index != "":
            if len(data) != 0:
                with open(path, "w") as file:
                    for element in data:
                        file.write(element)
            else:
                remove(path)

    except IndexError:
        messagebox.showerror("Error", "You have to select a question.")

    Del_Card_GUI(True)

def Del_Card_GUI(event):
    clear()

    path = getcwd() + "/data"
    groupnames = [f for f in listdir(path) if isfile(join(path, f))]
    groupList = []

    for element in groupnames:
        if element.endswith(".txt"):
            groupList.append(element.replace(".txt", ""))

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", Del_Add_GUI)

    questionList = Listbox(app, width = "40", height = "11", font = myFontLittle, bg = "#2C5F8D", fg = "white", relief = "flat", activestyle = "none")

    questionsAndGroup = []

    for i in range(len(groupList)):
        with open("data/" + groupList[i] + ".txt", "r") as file:
            data = file.readlines()
            for x in range(len(data)):
                data[x] = data[x].replace("\n", "") + " ~ " + groupList[i] + " ~"
                questionsAndGroup.append(data[x])

    pos = 0

    for i in range(len(questionsAndGroup)):
        if (i % 2) == 0:
            questionList.insert(pos, questionsAndGroup[i])
            pos += 1

    canvas.create_window(200, 180, window = questionList )

    AddLabel = canvas.create_text(200, 420, text = "Delete", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(AddLabel)


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Rest of the GUI -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def menu(event):
    clear()

    CardsLabel = canvas.create_text(200, 110, text = "Manage cards", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(CardsLabel)
    canvas.tag_bind(CardsLabel, "<Button-1>", Del_Add_GUI)

    LearnLabel = canvas.create_text(200, 235, text = "Learn", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(LearnLabel)

    SettingsLabel = canvas.create_text(200, 360, text = "Settings", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(SettingsLabel)

def Del_Add_GUI(event):
    clear()

    AddLabel = canvas.create_text(200, 110, text = "Add card", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(AddLabel)
    canvas.tag_bind(AddLabel, "<Button-1>", Add_Card_GUI)

    DelLabel = canvas.create_text(200, 300, text = "Delete card", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(DelLabel)
    canvas.tag_bind(DelLabel, "<Button-1>", Del_Card_GUI)

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", menu)


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Start the GUI -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
clear()

menu(True)

app.mainloop()
