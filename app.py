from appJar import gui
from bs4 import BeautifulSoup
import requests
import datetime
app = gui()
BaseURL = 'http://www.freecline.com/history/CCcam/'
clineByHost = {}
NUMBER_OF_CLINES_TO_WRITE_TO_FILE = 10

def getCurrentDateUrl():
    currentDate = datetime.datetime.now()
    year = currentDate.year
    month = currentDate.month
    day = currentDate.day - 1
    return BaseURL + str(year) + '/' +str(month) + '/' + str(day)

def printClinesToFile(fileDir):
    cLinesCounter = 0
    for key, value in clineByHost.iteritems():
        if cLinesCounter < 8:
            with open(fileDir,'a') as f:
                f.write(value[0])
                if cLinesCounter < 7:
                    f.write('\n')
        else: break
        cLinesCounter = cLinesCounter + 1



def getCLinesFromWebsite(fileDir):
    url = getCurrentDateUrl()
    #print(url)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    # Find all html tags that have an attribute "title" with value "Detailed information of the line" which is a Cline element
    #for cline in soup.find_all(attrs={"title" : "Detailed information of the line"}):
    for clineWrapper in soup.find('tbody').find_all('tr'):
        clineValue= clineWrapper.find('td').find('a').get_text()
        clineStatusWrapper = clineWrapper.find('td', {'class' : 'text-center'})
        if 'status_icon_online' in clineStatusWrapper.find('span').get('class'):
            hostname = clineValue.split(' ')[1]
            #print(hostname)
            if not hostname in clineByHost:
                clineByHost[hostname] = []
            clineByHost[hostname].append(clineValue)
        #    with open(fileDir,'a') as f:
        #    f.write(cline.get_text())
        #    f.write('\n')
    #print(clineByHost)
    
    printClinesToFile(fileDir)
    showSuccess()


def clearTextFile(fileDir):
    print(fileDir)
    open(fileDir, 'w').close()

def showSuccess():
    app.infoBox("Sucesso", "As linhas foram copiadas com sucesso para o ficheiro")

def press(button):
    fileDir = app.openBox(title=None, dirName=None, fileTypes=[('cfg', '.*cfg')], asFile=False, parent=None)
   #answer = app.yesNoBox("O que queres fazer?", "Queres acrescentar mais linhas?(yes) Queres apenas as novas linhas?(No)")
   #if answer == False:
    clearTextFile(fileDir)
    getCLinesFromWebsite(fileDir)



app.addLabel("title", "Content content content")
app.setLabelBg("title", "orange")
app.addButton("Escolher ficheiro", press)

app.go()


