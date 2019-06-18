# string = input()
# string += " "
# number_file = open("number.txt",'r')
# list = []
# f_list = []
# temp = ""
# for x in string:
#     if(x != " "):
#         temp = temp + x
#     else:
#         list.append(temp)
#         temp=""
# c=0
# for word in list:
#     #print(list)
#     for i in range(25):
#         f_list.append(number_file.readline())
#     for w in f_list:
#         if((word + "\n" )==w):
#             print(list[c+1] + " Noun")
#     c+=1
# number_file.close()

import re

# def remove_extra_word(string):
#     extra_word_file = open("extra_word.txt","r")
#     line = extra_word_file.readline()[0:-1]
#     while line:
#         for word in string.split():
#             if(string.find(line)!=-1):
#                 string=string.replace(line,"")
#                 string = string.replace("  ", " ")
#                 string=string.strip()
#                 print("True")
#         line=extra_word_file.readline()
#     extra_word_file.close()
#     print(string)

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

            pt = re.compile(r'ના$|નું$|ની$|માંથી$|માં$|થી$')
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
        self.list = list
        self.dict = {}
        for i in range(0,len(self.list)):
            self.dict[self.list[i]]=[i,"NaN"]
        self.totalw = len(self.list)
        self.NaNcount=0

    def base_tag(self):
        for w in self.list:
            (self.dict[w])[1] = self.base_search(w)             #searches word in the file and tags
        return self.dict

    def rule_based_tag(self):
        lst = list(self.dict.values())
        rn = re.compile(r'\w+\W?\w+\W?નો|\w+\W?\w+\W?ની|\w+\W?\w+\W?નું|\w+\W?\w+\W?ના|\w+\W?\w+\W?ને|\w+\W?\w+\W?થી|\w+\W?\w+\W?માંથી|\w+\W?[^વા]માં')                  #noun
        rv = re.compile(r'હોય|થવું|\w+\W?વ્યા|\w+\W?વ્યું|\w+\W?વવું|\w+\W?\w+\W?વું')                           #verb

        i=flag=0
        for w,l in self.dict.items():

            if(flag):
                self.dict[w][1] = "noun"
                flag=0

            # Nouns
            if(rn.search(w) and self.dict[w][1]=="NaN"):
                self.dict[w][1]="noun"                                   #tags nouns with suffix following pattern
                if(i<self.dict.__len__()-3):
                    if(lst[i+1][1]=="NaN" and lst[i+2][1]!="stopper" ):     #noun NaN !stopper => noun noun !stopper
                        lst[i + 1][1] = "noun"
                        #print("got it",i)
                        flag=1

            #Verbs
            if (rv.search(w) and self.dict[w][1] == "NaN"):
                self.dict[w][1]='verb'

            i+=1


        return self.dict

    def countNaNs(self):
        for key,value in self.dict.items():
            if value[1]=='NaN':
                self.NaNcount+=1
        return self.NaNcount

    def perc_tagged(self):
        return (self.totalw-self.countNaNs())/self.totalw

#MAIN FUNCTION

string_lines = open("input.txt","r").readlines()

for line in string_lines:
    str = remove_extra.remove_extra_word(line)
    ls = tockenizer(str).tokenize()

    tg = tagger(ls)
    ans1 = tg.base_tag()
    print(tg.rule_based_tag())
    print("tagged : ",tg.perc_tagged())
