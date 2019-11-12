from Tkinter import *  #Importing modules
import tkFileDialog     #Importing modules
from recommendations import * #importing modeules



class go_term(): #GO Class with two attributes of type strings
    def __init__(self,go_id,go_name):
        self.go_id = go_id
        self.go_name = go_name


class ecv():    #ECV Class with two attributes of type strings
    def __init__(self,ecv_acronym,numeric_value):
        self.ecv_acronym = ecv_acronym
        self.numeric_value = numeric_value

class annontaion(): #Annotation Class with two attributes of type objects of previous classes
    def __init__(self,functionality,ec):
        self.functionality = functionality
        self.ec = ec


class protein():    ##Protien Class with first two attributes as strings and last attribute is a dict of annotations objects
    def __init__(self,id,name,annotations):
        self.id = id
        self.name = name
        self.annotations = annotations





class data_center():#Data center Class
    def __init__(self,proteins,dict_of_comparison):

        self.names = [] #used to store info from anno file
        self.ids = []   # used to store info from anno file
        self.go_terms = [] # used to store info from anno file
        self.ecv_acronym = [] # used to store info from anno file
        self.dict_of_comparison = dict_of_comparison # dictionary that will be used in topmatches and getrecommendations
        self.proteins = proteins #dictionary used to store everything



    def reading_anno(self): #reading the annotataion file

        for i in open(tkFileDialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("gaf files", ".gaf"),("all files", ".*"))),"r"):
            if i.startswith("ComplexPortal"):
                    b = i.split('	')                 #reading correct lines in specific format

                    self.ids.append(b[1])       #appending to previously created lists
                    self.names.append(b[2])
                    self.go_terms.append(b[4])
                    self.ecv_acronym.append(b[6])

        for i,j,z,x in zip(self.ids,self.names,self.go_terms,self.ecv_acronym): #using multiple for loops to read data of four lists

            if i in self.proteins: #condition to add annotation to a protein id(if it already exists)
                if z not in self.proteins[i].annotations: #condition to ignore other annotations from same protein if go_id is same

                    # adding to the protein dictionary some values set to 0 or empty at first
                    self.proteins[i].annotations[annontaion(go_term(z,""),ecv(x,0)).functionality.go_id] = annontaion(go_term(z,""),ecv(x,0))
            else: #if protein is new creates an object of protein and adds it to dictionary with key as id
                self.object = protein(i, j,{annontaion(go_term(z,""),ecv(x,0)).functionality.go_id:annontaion(go_term(z,""),ecv(x,0))})
                self.proteins[self.object.id] = self.object




    def reading_ecv(self): #parses to ecv file
        self.txt_File_Path = tkFileDialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("txt files", ".txt"), ("all files", ".*")))
        file1 = open(self.txt_File_Path, "r")
        for i in file1:
            b = i.split("	")
            for protein_ids in self.proteins: #looping through protein ids in protein dict
                for x in self.proteins[protein_ids].annotations:    #looping through annotations of the same protein
                    if self.proteins[protein_ids].annotations[x].ec.ecv_acronym == b[0]: #condtion to see if ec_acronym is the same as in file
                        self.proteins[protein_ids].annotations[x].ec.numeric_value = b[1] #if true sets numeric value to numeric value from file





    def reading_go(self):   #parses go.obo
        self.txt_File_Path = tkFileDialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("obo files", ".obo"), ("all files", ".*")))

        self.list_of_names_for_go=[] #lists created that will later become a dict
        self.list_of_ids_for_go=[]

        file1 = open(self.txt_File_Path, "r")
        sum=1 #control variable
        for i in file1:
            listem = i.split(": ") #splits at id: or name:

            if sum % 2 == 0: #adding the names,ids by using the control variable and testing if its odd or even
                self.list_of_names_for_go.append(listem[1].rstrip())
            else:
                self.list_of_ids_for_go.append(listem[1].rsplit())
            sum += 1

        newdict={} #dict of key as id and value as name

        for i,j in zip(self.list_of_ids_for_go,self.list_of_names_for_go):

            newdict[i[0]]=j #insterting to dict by parsing the lists

        for id in newdict:  #looping the elements of the dict

            for protein_ids in self.proteins: # looping the elements of the protein dict

                self.dict_of_comparison[protein_ids] = {} #creating the dictionary that will be used in the recommendations methods
                for x in self.proteins[protein_ids].annotations: #lopping through different annotations of the same protein
                    #this dict has a key of cpx and value of dict with key as go id and value as ecv numeric value
                    self.dict_of_comparison[protein_ids][x] = float(self.proteins[protein_ids].annotations[x].ec.numeric_value.split("\n")[0])
                    #if the go_id is equal to go_id in the newdict then the go_name equals the value of the go_id key which is the name
                    if self.proteins[protein_ids].annotations[x].functionality.go_id == id:
                        self.proteins[protein_ids].annotations[x].functionality.go_name = newdict[id]












class GUI(Frame):       #defining third class
    def __init__(self, parent):         #defining attributes of third class
        self.parent = parent
        self.data_center = data_center({},{}) #creating an object of data center with empty dicts at first
        self.control_variable = 0           #variable that checks if file has been imported
        Frame.__init__(self, parent)
        self.initUI(parent)             #calling the ui function which displays everything


    def initUI(self,parent):     #creating a function that has all widgets

        self.checkbox_var = StringVar()
        self.checkbox_var.set("Euclidean")
        self.main_frame = Frame(self, borderwidth=0, relief=GROOVE)
        self.main_frame.grid(sticky = W,row = 0, column = 0)

        Label(self.main_frame,text = "Protein Function Prediction Tool",bg="#36d16c", fg="white", font=("Helvetica", 18,"bold"),width = 76,height = 2).grid(sticky = W,row = 0, column = 0)

        self.upload_annotations_button = Button(self.main_frame,text = "Upload\nAnnotations",height = 2,command = self.adding,font=("Helvetica", 9,"bold"))
        self.upload_annotations_button.grid(sticky = W,row = 1,padx = 420,pady = 20)

        self.upload_evidence_button = Button(self.main_frame,text="Upload Evidence\nCode Values",font=("Helvetica", 9,"bold"), height=2,command = self.data_center.reading_ecv)
        self.upload_evidence_button.grid(sticky= W,row = 1,padx = 540)

        self.upload_go_button = Button(self.main_frame,text="Upload GO File",font=("Helvetica", 9,"bold"), height=0,command = self.data_center.reading_go)
        self.upload_go_button.grid(row = 1,column = 0,padx = 690)

        self.bottom_frame = Frame(self,borderwidth = 0,relief = GROOVE)
        self.bottom_frame.grid(row = 1,column = 0,sticky = W)

        Label(self.bottom_frame,text = "Proteins",font=("Helvetica", 9,"bold")).grid(sticky = W,padx = 65)

        self.scrollbar = Scrollbar(self.bottom_frame)
        self.scrollbar.grid(sticky = NW,column = 0,ipady = 86,padx = 180)

        self.protein_box = Listbox(self.bottom_frame, yscrollcommand=self.scrollbar.set,bd = 1)
        self.protein_box.grid(sticky = NW,row = 1,padx=5,ipadx = 27,ipady = 30)

        self.scrollbar.config(command=self.protein_box.yview)

        Label(self.bottom_frame,text = "Similarity Metric",font=("Helvetica", 9,"bold")).grid(sticky = W,column = 0,row = 0,padx = 290)

        self.outline_for_checkboxes = Canvas(self.bottom_frame,width = 150,height = 220)
        rect = self.outline_for_checkboxes.create_rectangle(3,3,150,220,outline = "Black",width = 2)
        self.outline_for_checkboxes.grid(column = 0,row = 1,sticky = W,padx = 265)

        self.Checkbox1 = Checkbutton(self.bottom_frame,variable = self.checkbox_var, text='Pearson', onvalue='Pearson',command = self.similarity)
        self.Checkbox1.grid(row=1,column=0,sticky="NW", pady = 20,padx = 300)

        self.Checkbox2 = Checkbutton(self.bottom_frame,variable = self.checkbox_var, text='Euclidean', onvalue='Euclidean',command = self.similarity)
        self.Checkbox2.grid(row=1,column=0,sticky="NW", pady = 45,padx= 300)

        Label(self.bottom_frame,text = "Similar Protein",font=("Helvetica", 9,"bold")).grid(sticky = W,row = 0,padx = 520)

        self.scrollbar2 = Scrollbar(self.bottom_frame)
        self.scrollbar2.grid(row = 1,sticky=NW, column=0, ipady=86, padx=660)

        self.sim_protein_box = Listbox(self.bottom_frame, bd=1,yscrollcommand=self.scrollbar2.set)
        self.sim_protein_box.grid(sticky=NW, row=1, padx=450, ipadx=44, ipady=30)

        self.scrollbar2.config(command=self.sim_protein_box.yview)

        Label(self.bottom_frame,text = "Predicted Function",font=("Helvetica", 9,"bold")).grid(row = 0,sticky = W,padx = 850)

        self.scrollbar3 = Scrollbar(self.bottom_frame)
        self.scrollbar3.grid(row=1, sticky=NW, column=0, ipady=86, padx=1125)

        self.predicted_func_box = Listbox(self.bottom_frame, bd=1, yscrollcommand=self.scrollbar3.set)
        self.predicted_func_box.grid(sticky=NW, row=1, padx=700, ipadx=150, ipady=30)

        self.scrollbar3.config(command=self.predicted_func_box.yview)

        self.pack()

        self.protein_box.bind("<<ListboxSelect>>", lambda x : self.similarity()) #when user selects item from listbox

    def similarity(self):#function that is called when user selects item in listbox
            x = self.protein_box.curselection() #gets item index
            self.sim_protein_box.delete(0, END) # deleting everything in listboxes previously
            self.predicted_func_box.delete(0, END)

            if self.checkbox_var.get() == "Euclidean":



                for i in self.data_center.proteins: #looping over ids in protein dict

                    if self.data_center.proteins[i].name == self.protein_box.get(x): #if the name of the protein equals the selection then i = the protein id
                        #lists to store the results of the methods
                        list_of_results = topMatches(self.data_center.dict_of_comparison,i,n=-1,similarity=sim_distance) #calling topmatches
                        list_of_results2 = getRecommendations(self.data_center.dict_of_comparison, i, similarity=sim_distance) #calling get recommendations



                        new_list = [] #list that will be used to retreive data to display in listbox
                        for c in list_of_results: #looping over data from TopMatches


                            if c[0] >0: #if score greater than 0

                                instered_value = str(round(c[0], 1)) + " - " + c[1] + " - " + self.data_center.proteins[c[1]].name #pre defining text that will be added

                                self.sim_protein_box.insert(END, instered_value) #adding it to the end



                            for v in list_of_results2: #loop to append to the new_list
                                # format of list is [[go_id,go_name,ecv_numeric_value],[go_id2,go_name2,ecv_numeric_value2]
                                for annontaion in self.data_center.proteins[c[1]].annotations:
                                    if self.data_center.proteins[c[1]].annotations[annontaion].functionality.go_id == v[1]:
                                        new_list.append([v[1],self.data_center.proteins[c[1]].annotations[v[1]].functionality.go_name,float(self.data_center.proteins[c[1]].annotations[v[1]].ec.numeric_value)])





                        new_list.sort(key=lambda index:index[2],reverse=True) #sorting from greatest to lowest by the 2nd index value in each list(this was learned from stackoverflow)

                        self.predicted_func_box.delete(0,END) #emptying listbox
                        for i in new_list: #looping over the new_list elements

                            instered_value = str(i[2]) + " - " + str(i[0]) + " - " + str(i[1]) #predifing text to be added
                            if instered_value not in self.predicted_func_box.get(0,END): #if it isnt already addded
                                self.predicted_func_box.insert(END, instered_value) # then add it





            if self.checkbox_var.get() == "Pearson":        #same as above but changed to sim_pearson



                    for i in self.data_center.proteins:

                        if self.data_center.proteins[i].name == self.protein_box.get(x):

                            list_of_results = topMatches(self.data_center.dict_of_comparison, i, n=-1,
                                                         similarity=sim_pearson)
                            list_of_results2 = getRecommendations(self.data_center.dict_of_comparison, i,
                                                                  similarity=sim_pearson)

                            new_list = []
                            for c in list_of_results:
                                for v in list_of_results2:
                                    for annontaion in self.data_center.proteins[c[1]].annotations:
                                        if self.data_center.proteins[c[1]].annotations[
                                            annontaion].functionality.go_id == v[1]:
                                            new_list.append([v[1], self.data_center.proteins[c[1]].annotations[
                                                v[1]].functionality.go_name, float(
                                                self.data_center.proteins[c[1]].annotations[v[1]].ec.numeric_value)])

                                if c[0] > 0:
                                    instered_value = str(round(c[0], 1)) + " - " + c[1] + " - " + \
                                                     self.data_center.proteins[c[1]].name

                                    self.sim_protein_box.insert(END, instered_value)

                            new_list.sort(key=lambda index: index[2], reverse=True)

                            self.predicted_func_box.delete(0, END)
                            for i in new_list:

                                instered_value = str(i[2]) + " - " + str(i[0]) + " - " + str(i[1])
                                if instered_value not in self.predicted_func_box.get(0, END):
                                    self.predicted_func_box.insert(END, instered_value)

    def adding(self): #function that calls the reading annotaion and adds to first listbox
        self.data_center.reading_anno()
        self.protein_box.delete(0, END) #emptying listbox
        for i in self.data_center.proteins:
            self.protein_box.insert(END,self.data_center.proteins[i].name) #adding to listbox


def main():# function that runs the app by creating object of tk and third class which takes the object of tk as argument
    root = Tk()
    root.title('Protein Function Prediction Tool v1.0')
    root.geometry("1146x400")
    app = GUI(root)
    root.mainloop()
main()
#using the lambda was learned and understood from stackoverflow and no code was copied.