from  bs4 import BeautifulSoup
import requests
import time


def find_recipes():
    site = 'https://akispetretzikis.com'
    first_ing = 'eggs'
    second_ing = 'bread'
    third_ing = 'ham'

    search = '&search=' + first_ing
    page_counter = 1


    url='https://akispetretzikis.com/en/search?from=admin' + '&page=' +str(page_counter)+ search+'&utf8=%E2%9C%93'
    html_text=requests.get(url).text
    soup = BeautifulSoup(html_text,'lxml')
    show_more_button=soup.find(id='next_page_link')




    if(show_more_button is None):
        print('NO RESULTS FOR THE MAIN INGREDIENT')

    while (show_more_button is not None):

        texts = soup.find_all('div', class_='texts')
        for i in texts:

            recipe_url = site + i.find('a')['href']

            recipe_html_text = requests.get(recipe_url).text
            recipe_soup = BeautifulSoup(recipe_html_text, 'lxml')

            ingredients = recipe_soup.find('div', class_='text ingredients-list')
            # check if other ingrediens are in the same recipe
            if (((second_ing and third_ing) in str(ingredients)) is True):
                print('MATCH')

                # Recipe url
                print(recipe_url)

                # for the Recipe Name
                recipe_name = i.find('h4').text
                print(recipe_name)

                # Time till we feast
                hands_on_time = recipe_soup.find('ul', class_='new-times').find('h5').text
                print(hands_on_time)

                # print ingredients
                ing_li = ingredients.find_all(['li', 'p'])
                for i in ing_li:
                    print(i.text)

                # for the recipe method
                method_box = recipe_soup.find('div', class_='method')
                method_list = method_box.find_all('li')

                for m in method_list:
                    print(m.text)

                # select directory

                with open(f'recipe_results/{recipe_name}.txt', 'w',encoding='utf-8') as f:
                    f.write(recipe_url+'\n')
                    f.write(recipe_name+'\n')
                    f.write(hands_on_time+'\n')
                    for i in ing_li:
                        f.write(i.text+'\n')
                    #f.write('\n')
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
    while True:
        find_recipes()
