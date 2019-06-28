import re


class remove_extra:
    def remove_extra_word(string):
        extra_word_file = open("extra_word.txt","r")
        line = extra_word_file.readline()[0:-1]
        while line:
            if re.search(line,string):                                  #Searches extra words
                string=re.sub(line+" ","",string)                        #removes spaces at the end of line
                string=re.sub(r'-'," ",string)                                 #replaces '-' with " "
                string=re.sub(" {2,}"," ",string)                            #removes extra spaces
                string=re.sub(r"[`\'\"\?!,;]","",string)                             #removes extra symbols
                string=string.strip()
                #print("True")
            line=extra_word_file.readline()[0:-1]
        extra_word_file.close()
        return string


class tockenizer:
    def __init__(self,string):
        self.string = string
        self.list = []

    def tokenize(self):
        temp=""
        for char in self.string:
            if(char!=" " and char!="."):
                temp+=char
            else:
                self.list.append(temp)                  #converts into words
                temp=""
        return self.list



class search:
    def __init__(self):
        self.f_list = ["negation","conjuction","pronoun","verb","preposition","questionnaire","comparative","adverb","number","stopper"]

    def base_search(self,word):
        for t in self.f_list:

            pt = re.compile(r'ના$|નું$|ની$|નો$|માંથી$|માં$|થી$')
            if pt.search(word)and len(word)>4:                       #word with suffix (removes suffix)
                temp=word
                word=word[:pt.search(word).start()]
                if len(word)<2:                                     #word length should be > 2
                    word=temp

            fp = open(t+".txt","r")
            line = fp.readline()
            while line:                                   #searches word in all the files listed in f_list
                if(re.search(word+'\n',line)):
                    fp.close()
                    return t                                #returns type of word
                else:
                    line = fp.readline()
            fp.close()
        return "NaN"                                        #if not found in all files returns NaN

class tagger(search):
    def __init__(self,list):
        search.__init__(self)
        self.word_list = list
        self.tag_list = []
        for i in range(0,len(self.word_list)):
            self.tag_list.append("NaN")
        self.totalw = len(self.word_list)
        self.NaNcount=0

    def base_tag(self):
        for i in range(0, self.totalw):
            self.tag_list[i] = self.base_search(self.word_list[i])             #searches word in the file and tags
        return self.tag_list

    def rule_based_tag(self):
        rn = re.compile(r'\w+\W?\w+\W?નો|\w+\W?\w+\W?ની|\w+\W?\w+\W?નું|\w+\W?\w+\W?ના|\w+\W?\w+\W?ને|\w+\W?\w+\W?થી|\w+\W?\w+\W?માંથી|\w+\W?[^વા]માં')                  #noun
        rv = re.compile(r'હોય|થવું|\w+\W?વ્યા|\w+\W?વ્યું|\w+\W?વવું|\w+\W?\w+\W?વું')                           #verb

        for i in range(self.totalw):

            # Nouns
            if(rn.search(str(self.word_list[i])) and self.tag_list[i]=="NaN"):
                self.tag_list[i]="noun"                                   #tags nouns with suffix following pattern
                if(i<self.totalw-3):
                    if(self.tag_list[i+1]=="NaN" and self.tag_list[i+2]!="stopper" ):     #noun NaN !stopper => noun noun !stopper
                        self.tag_list[i + 1] = "noun"

            #Verbs
            if (rv.search(str(self.word_list[i])) and self.tag_list[i] == "NaN"):
                self.tag_list[i]='verb'


        #return self.tag_list,self.word_list

    def countNaNs(self):                                            #counts NaN values in sentence
        for i in range(self.totalw):
            if self.tag_list[i]=='NaN':
                self.NaNcount+=1
        return self.NaNcount

    def perc_tagged(self):
        return (self.totalw-self.countNaNs())/self.totalw                       #calculates perc

    def print_dict(self):
        for i in range(0,self.totalw):
            print(self.word_list[i],":",self.tag_list[i],end="   ")                #prints word:tag pair


#MAIN FUNCTION

string_lines = open("input.txt","r").readlines()

for line in string_lines:
    string = remove_extra.remove_extra_word(line)
    word_ls = tockenizer(string).tokenize()

    tg = tagger(word_ls)
    tag_ls = tg.base_tag()
    tg.rule_based_tag()
    tg.print_dict()
    print("\ntagged : ",tg.perc_tagged())                               #prints tagged perc
