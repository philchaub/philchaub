import os 

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm,trange

from concurrent.futures import ThreadPoolExecutor



# # fonction de scrapping de la doc de blender :
############################################################################################################

# recuparation des liens des pages de la doc
def get_links_of_other_page_of_same_subject(adress,key_words_in,key_words_out,method_in=all,method_out=any):

    #tentative de recuperation de la page principal 
    try : 
        main_page = requests.get(adress)
    except Exception as e:
        print("failed to get the page",adress)
        print("error:",e)

    #tentative de parsing de la page principal 
    try : 
        main_soup = BeautifulSoup(main_page.content, "html.parser")
    except Exception as e:
        print("failed to parse the page of adress",adress)
        print("error:",e)

    # recuperation des liens des pages en aval 
    links_selected=[]
    other=[]

    for link in main_soup.find_all('a'):
        #print("-->",link)
        l=link.get('href')
        try:  
            #condition de selection des liens
            c1=l
            c2=method_in(item in l for item in key_words_in)
            c3=method_out(item not in l for item in key_words_out)

            if c1 and c2 and c3: links_selected.append(l)
            else:  other.append(l)

        except Exception as e:
            print("failed to get the link of the page",l)
            print("error:",e)  
            pass
    
    print("lien selectionner:",len(links_selected),"autre lien:",len(other))
    return ["https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/"+ str(x) for x in links_selected]


def get_pages_of_links (complet_links:list):
    # recuparation des pages de la doc
    pages_download=[]
    pages_failed=[]
    pages_names=[]
    for adress in complet_links : 
        try:
            page = requests.get(adress)
            soup = BeautifulSoup(page.content, "html.parser")   
            pages_download+=[soup]#.find_all(text=lambda text:isinstance(text)) extract()
            pages_names+=[adress.split("/")[-1]]
        except:
            pages_failed+=[page]

    if pages_failed !=[]:
        print('len of pages_failed',len(pages_failed),"for len complet_links",len(complet_links))
        # for p in pages_failed:
        #     print("failed to download the following pages",p)  

    return pages_download,pages_names


# stockage avant traitement
def save_pages_json(pages_download,pages_names,path):
    for element in range(len(pages_download)):
        jsontext = pages_download[element].prettify("utf-8")   
        mypath = path+str(pages_names[element])+".json"
        with open(mypath, 'w') as outfile:
            json.dump(str(jsontext), outfile, ensure_ascii=False, indent=4)

############################################################################################################


# fonction de parsing de la doc de blender:
############################################################################################################

def load_page(mypath):
    with open(mypath, 'r') as outfile:
        pages_download = json.load(outfile)
    return pages_download

def load_pages(mypath):
    pages=[]
    files_names=[]
    for file_name in os.listdir(mypath):
        pages.append(load_page(mypath+file_name))
        files_names.append(file_name)
    return pages,files_names

#recupere le textes des pages
def get_text_of_pages(pages_download,page_name):
    # #transformer les pages en texte
    # #print("get text",page_name)
    # text_pages=[]
    # for element in trange(len(pages_download)):
    #     soup=BeautifulSoup(pages_download[element], "html.parser")
    #     texte_page=[]
    #     for p in soup.find_all('p'):
    #         texte_page.append(p.text)

    #     text_pages.append(texte_page)
    # return text_pages
        soup=BeautifulSoup(pages_download, "html.parser")
        texte_page=[]
        for p in soup.find_all('p'):
            texte_page.append(p.text)
        return texte_page

def save_pages_txt(pages_download,pages_names,path):
        
    # for element in trange(len(pages_download)):
    #     print("save  text")
    #     with open(path+str(pages_names[element])+".txt", 'w') as outfile:
    #         for p in pages_download[element]:
    #             p = p.replace("\n","").replace("\\n","")
    #             p = p.replace("  ","")
    #             p = p.replace("Sections","",1)
    #             p = p.replace("Get Involved","",1)
    #             p = p.replace("Getting Started","",1)
    #             outfile.write(p)
    #             outfile.write("\n")

   
    with open(path+str(pages_names)+".txt", 'w') as outfile:
        for p in pages_download:
            p = p.replace("\n","").replace("\\n","")
            p = p.replace("  ","")
            p = p.replace("Sections","",1)
            p = p.replace("Get Involved","",1)
            p = p.replace("Getting Started","",1)
            outfile.write(p)
            outfile.write("\n")

def extract_text (pages_download,pages_names,path):

    # for p in trange(len(pages_download)):
    #     print("traitement de la page ",pages_names,pages_names)
    #     pd = pages_download[p]
    #     pn = pages_names[p]
    #     text=get_text_of_pages(pd,pn)
    #     print(pn)
    #     print(pages_names)
    #     print("nombre de page traité:",len(text))
    #     print("sauvegarde de la page pages ")
    #     save_pages_txt(text,pn,path)
    #     print("fin")
    text=get_text_of_pages(pages_download,pages_names)
    save_pages_txt(text,pages_names,path)





############################################################################################################

def parallelize(num_threads,fn,*args):
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        result= executor.map(fn,*args)
    return result



if __name__=="__main__":

    adress = "https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html"
    my_scrapping_path = "C://Users/isisc/IA/cuda_rag/cuda_rag/Scripts/blendercrew/blender_doc/scrap_doc_/"
    my_parsing_path = "C://Users/isisc/IA/cuda_rag/cuda_rag/Scripts/blendercrew/blender_doc/parse_doc_/"

    num_cores = os.cpu_count()
    num_threads = num_cores-1


    if not os.path.isdir(my_scrapping_path):
        print("scrapping de la doc")
        os.mkdir(my_scrapping_path)
        # complet_links = parallelize(num_threads,get_links_of_other_page_of_same_subject,*[adress,["html"],["https"]])
        complet_links = get_links_of_other_page_of_same_subject(adress,["html"],["https"])
        
        non_saved_pages = [my_scrapping_path+x.split("/")[-1].split(".")[0]+".json"
                          for x in complet_links
                          if not os.path.isfile(my_scrapping_path+x.split("/")[-1]+".json")]
        print(non_saved_pages)
        print("non_saved_pages",len(non_saved_pages))
        # pages_download,pages_names = parallelize(num_threads,get_pages_of_links,*[complet_links])
        pages_download,pages_names = get_pages_of_links(complet_links)
        save_pages_json(pages_download,pages_names,my_scrapping_path)
    else:
        print("parsing de la doc")
        
        print("chargement des pages")
        pages_download,pages_names = load_pages(my_scrapping_path)
        print("type de page chargé:",type(pages_download[0]))
        print("nombre de page chargé:",len(pages_download))
        print("nombre de nom de page chargé:",len(pages_download))

        # print("traitement des pages ")
        # texte = list(parallelize(num_threads,get_text_of_pages,*[pages_download,pages_names]))
        # print("nombre de page traité:",len(texte))

        # print("sauvegarde des pages ")
        # # texte=get_text_of_pages(pages_download)
        # parallelize(num_threads,save_pages_txt,*[texte,pages_names,my_parsing_path])
        # save_pages_txt(texte,pages_names,my_parsing_path)
        pg = pages_download[:2]
        pn = pages_names[:2]
       
        # parallelize(num_threads,extract_text ,[pg,pn,my_parsing_path])

        # with ThreadPoolExecutor(max_workers=num_threads) as executor:
        #     result= executor.map(extract_text,pages_download[:2],pages_names[:2],my_parsing_path)

        for page in range(len(pages_download)):
            extract_text(pages_download[page],pages_names[page],my_parsing_path)
        

    # pages_download = load_pages(my_scrapping_path)
    # print([type(x) for x in pages_download][0])
    # print([x for x in pages_download][0])



















    

