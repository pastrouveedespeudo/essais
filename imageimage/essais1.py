from bs4 import BeautifulSoup as Soup

import json
import urllib.request

#programtically go through google image ajax json return and save links to list#
#num_images is more of a suggestion                                            #  
#it will get the ceiling of the nearest 100 if available                       #
def get_links(query_string, num_images):
    #initialize place for links
    links = []
    #step by 100 because each return gives up to 100 links
    for i in range(0,num_images,100):
        url = "https://www.google.co.in/search?q="+"voiture"+"&source=lnms&tbm=isch"

        #set user agent to avoid 403 error
        request = urllib.request.Request(url, None, {'User-Agent': 'Mozilla/5.0'}) 

        #returns json formatted string of the html
        json_string = urllib.request.urlopen(request).read() 

        #parse as json
        page = json.loads(json_string) 

        #html found here
        html = page[1][1] 

        #use BeautifulSoup to parse as html
        new_soup = Soup(html,'lxml')

        #all img tags, only returns results of search
        imgs = new_soup.find_all('img')

        #loop through images and put src in links list
        for j in range(len(imgs)):
            links.append(imgs[j]["src"])

    return links

#download images                              #
#takes list of links, directory to save to    # 
#and prefix for file names                    #
#saves images in directory as a one up number #
#with prefix added                            #
#all images will be .jpg                      #
def get_images(links,directory,pre):
    for i in range(len(links)):
        urllib.request.urlretrieve(links[i], "./"+directory+"/"+str(pre)+str(i)+".jpg")

#main function to search images                 #
#takes two lists, base term and secondary terms #
#also takes number of images to download per    #
#combination                                    #
#it runs every combination of search terms      #
#with base term first then secondary            #
def search_images(base,terms,num_images):
    for y in range(len(base)):
        for x in range(len(terms)):
            all_links = get_links(base[y]+'+'+terms[x],num_images)
            get_images(all_links,"images",x)

if __name__ == '__main__':
    terms = ["voiture"]
    base = ["animated"]
    search_images(base,terms,1)
