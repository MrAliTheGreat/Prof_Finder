import requests
from bs4 import BeautifulSoup
import spacy
import re
import webbrowser

NER = spacy.load("en_core_web_sm")


# def runTest(NER , text):
#     if(not NER(text).ents):
#         for word in NER(text.lower()).ents:
#             print(word.text , word.label_)
#         return
    
#     for word in NER(text).ents:
#         print(word.text , word.label_)

# runTest(NER , "Miriah Meyer")


inputURL = input("CS Dept URL: ")
soup = BeautifulSoup(requests.get(inputURL).text, features = "lxml")
foundFacultyLinks = []
for tag in soup.find_all("a"):
    link = tag.get("href")
    if(link is not None and ("faculty" in link or "people" in link)):
        foundFacultyLinks.append(link)

if(len(foundFacultyLinks) <= 0):
    print("\nNo faculty link found!!!")
elif(len(foundFacultyLinks) == 1):
    print("\nOnly one faculty link found")
    targetFacultyLink = foundFacultyLinks[0]
else:
    print("\nMultiple faculty links found which one do you want?")
    idx = 0
    for link in foundFacultyLinks:
        print(str(idx) + ": " + link)
        idx += 1
    userIndex = int(input("Your choice: "))
    targetFacultyLink = foundFacultyLinks[userIndex]

if(targetFacultyLink[0] == "/"):
    targetFacultyLink = inputURL + targetFacultyLink[1:]

print("\nProceeding with link: " + targetFacultyLink)

print("\n===== All Professors =====")

profLinks = {}
idx = 0
soupFacultyPage = BeautifulSoup(requests.get(targetFacultyLink).text, features = "lxml")
for tag in soupFacultyPage.find_all("a"):
    link = tag.get("href")
    if(link is not None and link != "" and link[0] != "#" and len(link) > 1):
        tagStr = tag.get_text().encode("utf-8").decode("ascii", "ignore")
        if(NER(tagStr).ents):
            for word in NER(tagStr).ents:
                if(word.label_ == "PERSON" and "@" not in word.text):
                    print(str(idx) + ": " + tagStr , end = "     "); profLink = link.encode("utf-8").decode("ascii", "ignore")
                    if(profLink == ""):
                        continue

                    if(profLink[0] == "/"):
                        profLink = inputURL + profLink[1:]
                        print(profLink)
                    else:
                        print(profLink)

                    profLinks[tagStr] = profLink
                    if(tag.string):
                        tag.string.replace_with("0000000000")
                    idx += 1
        else:
            for word in NER(tagStr.lower()).ents:
                if(word.label_ == "PERSON" and "@" not in word.text):
                    print(str(idx) + ": " + tagStr , end = "     "); profLink = link.encode("utf-8").decode("ascii", "ignore")
                    if(profLink == ""):
                        continue

                    if(profLink[0] == "/"):
                        profLink = inputURL + profLink[1:]
                        print(profLink)
                    else:
                        print(profLink)

                    profLinks[tagStr] = profLink
                    if(tag.string):
                        tag.string.replace_with("0000000000")
                    idx += 1

print("\n\nStarted Deep Search For Interests...\n")

myInterests = ["Machine Learning" , "Machine learning" , "machine learning" ,
               "Artificial Intelligence" , "Artificial intelligence" , "artificial Intelligence" ,
               "Computer Vision" , "Computer vision" , "computer vision" ,
               "Data Science" , "Data science" , "data science" ,
               "Data Mining" , "Data mining" , "data mining"
              ]

for profName , profLink in profLinks.items():
    soup = BeautifulSoup(requests.get(profLink).text, features = "lxml")
    matched = False
    for myInterest in myInterests:
        # The tag here that is <p> right now must be determined by inspecting the research interest tag in browser
        # Meaning that sometimes it can be other tags for example <li> or <div>. Just take a look at inspect to be sure
        if(soup.find("p" , text = re.compile(myInterest))):
            matched = True
            break
    if(matched):
        print("+++ Match Found!    " + profName + "     " + profLink)
    else:
        print("--- Match NOT Found!    " + profName + "     " + profLink)


f = open('LeftOutProfs.html', 'w')
f.write(soupFacultyPage.encode("utf-8").decode("ascii", "ignore"))
f.close()
webbrowser.open_new_tab('LeftOutProfs.html')