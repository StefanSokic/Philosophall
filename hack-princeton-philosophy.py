from bs4 import BeautifulSoup
import urllib.request

def main():
    subject = str(input("Pls enter the Wikipedia article you would like to start on: "))
    while isRealWiki(subject) == False:
        subject = str(input("Chiiillll, there is no Wikipedia article for that page. Pls enter a valid one: "))

    while subject != "Philosophy":
        paragraphHTML = getHTML('https://en.wikipedia.org/wiki/' + subject)
        print(subject.replace("_", " "))
        subject = findLink(paragraphHTML)
    if subject == "Philosophy":
        print("Philosophy")
    else:
        pass

def findLink(new_soup):
    left_bound = new_soup.find('<a')
    right_bound = new_soup.find('</a>')
    sub_soup = new_soup[left_bound:right_bound]
    new_index = sub_soup.find('>') + 9
    left_check = sub_soup.find('=') + 2
    right_check = left_check + 6
    is_wiki = sub_soup[left_check:right_check]
    while sub_soup[new_index].isupper() or is_wiki != '/wiki/' or sub_soup[right_check:right_check + 4] == 'Help' or \
                    sub_soup[right_check:right_check + 8] == 'Template' or sub_soup[right_check:right_check + 4] == 'File'\
            or sub_soup[right_check:right_check + 9] == 'Wikipedia' or sub_soup[right_check:right_check + 9] == 'Category':
        left_bound = new_soup.find('<a', left_bound + 1)
        right_bound = new_soup.find('</a>', right_bound + 1)
        sub_soup = new_soup[left_bound:right_bound]
        new_index = sub_soup.find('>') + 9

        left_check = sub_soup.find('=') + 2
        right_check = left_check + 6
        is_wiki = sub_soup[left_check:right_check]

    next_start = sub_soup.find('=') + 8
    next_end = sub_soup.find('"', next_start)
    page = sub_soup[next_start:next_end]
    return page

def getHTML(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    string = soup.prettify()
    index = string.find('<p>')
    new_soup = string[index:]
    return new_soup

def isRealWiki(subject):
    try:
        getHTML('https://en.wikipedia.org/wiki/' + subject)
    except:
        return False
    return True

main()