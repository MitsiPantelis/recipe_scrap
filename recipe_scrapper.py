from  bs4 import BeautifulSoup
import requests
import time
import os

def find_recipes():
    site = 'https://akispetretzikis.com'

    # create new directory for the results
    parent_dir = os.path.dirname(os.path.abspath("top_level_file.txt"))
    # Directory
    directory = "Matched Recipes"

    # Path
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

    print("Search the website: akispetretzikis.com ")
    print("Insert up to 3 ingredients to filter all the recipes")


    first_ing=''
    second_ing=''
    while(first_ing == ''):
        first_ing= input("Give the main ingredient\n>")
    while( second_ing == ''):
        second_ing = input('Give a second ingredient\n>')
    third_ing = input('Give a third ingredient if you want\n>')


    search = '&search=' + first_ing
    page_counter = 1



    url='https://akispetretzikis.com/en/search?from=admin' + '&page=' +str(page_counter)+ search+'&utf8=%E2%9C%93'
    html_text=requests.get(url).text
    soup = BeautifulSoup(html_text,'lxml')
    show_more_button=soup.find(id='next_page_link')




    if(show_more_button is None):
        print('NO RESULTS FOR THE MAIN INGREDIENT')

    while (show_more_button is not None):
        print("searching...")
        texts = soup.find_all('div', class_='texts')
        for i in texts:

            recipe_url = site + i.find('a')['href']

            recipe_html_text = requests.get(recipe_url).text
            recipe_soup = BeautifulSoup(recipe_html_text, 'lxml')

            ingredients = recipe_soup.find('div', class_='text ingredients-list')
            # check if other ingrediens are in the same recipe
            if (((second_ing and third_ing) in str(ingredients)) is True):

                # Recipe url

                # for the Recipe Name
                recipe_name = i.find('h4').text

                # Time till we feast
                hands_on_time = recipe_soup.find('ul', class_='new-times').find('h5').text

                # print ingredients
                ing_li = ingredients.find_all(['li', 'p'])


                # for the recipe method
                method_box = recipe_soup.find('div', class_='method')
                method_list = method_box.find_all('li')



                # select directory



                with open(f'Matched Recipes/{recipe_name}.txt', 'w',encoding='utf-8') as f:
                    f.write('Recipe link\t'+recipe_url+'\n')
                    f.write(recipe_name+'\n')
                    f.write('Hands on Time:\t'+hands_on_time+'\n')
                    f.write('Ingredients\n')
                    for i in ing_li:
                        f.write(i.text+'\n')
                    #f.write('\n')
                    f.write('Ingredients\n')
                    for m in method_list:
                        f.write(m.text+'\n')


            else:
                continue






        #increments for while
        page_counter = page_counter + 1
        url = 'https://akispetretzikis.com/en/search?from=admin' + '&page=' + str(page_counter) + search + '&utf8=%E2%9C%93'
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        show_more_button = soup.find(id='next_page_link')



if __name__  ==  '__main__':



    find_recipes()
    print("Search completed\nOpen Matched Recipes directory to view them")
    print("Goodbye!")
