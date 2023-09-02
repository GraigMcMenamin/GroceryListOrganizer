from flask import Flask, render_template, request

import directory_file

sorted_list = []
sorted_list_no_ranks = []
extra_items = []

def organize_groceries(user_list):
    sorted_list.clear()
    extra_items.clear()
    #strip carriage returns (\r) from the users list
    user_list = [item.strip() for item in user_list]
    #increment through user list
    i = 0
    #incrementation will stop when i = the length of the list
    while i < len(user_list):
        #check if list item is in directory by incrementing through directory
        j = 0
        while j < len(directory_file.directory):
            #when there's an i before a variable name, that refers to the current increment in that list
            #this next line creates a variable for each increment item in the directory so we can check just the item in the string not the rank
            i_directory = directory_file.directory[j]
            if (i_directory[2:] in user_list[i]) == True:
                #if so, create a variable that has the user's item with the associated rank
                item_with_rank = (i_directory[0:2]) + user_list[i]
                item_rank = int(item_with_rank[0:2])
                #check if sorted list is empty,
                if len(sorted_list) == 0:
                    #if so, append the first item with it's rank
                    sorted_list.append(item_with_rank)
                else:
                    #is not, increment through the sorted list
                    k = 0
                    while k < len(sorted_list):
                        #for each item in the sorted list, create a variable that has its rank
                        i_sorted_item = sorted_list[k]
                        i_sorted_item_rank = int(i_sorted_item[0:2])
                        #check if the rank of the item we're sorting is lower or equal to the rank of the current item in sorted_list
                        if item_rank <= i_sorted_item_rank:
                            #if so, insert the item with rank at index 'k' which is our current incrementation spot
                            sorted_list.insert(k, item_with_rank)
                            break
                        #check if were at the end of the list and put the item at the end if so
                        elif k == ((len(sorted_list))-1):
                            sorted_list.append(item_with_rank)
                            break
                        k += 1
                break
            # check if we got to the end of the directory, if so add to separate list
            elif j == ((len(directory_file.directory))-1):
                extra_items.append(user_list[i])
            j += 1
        i += 1


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize():
    raw_user_list = request.form['grocery_list']
    split_user_list = raw_user_list.split('\n')
    organize_groceries(split_user_list)
    sorted_list_no_ranks = [string[2:] for string in sorted_list]
    return render_template('results.html', sorted_list_no_ranks=sorted_list_no_ranks, extra_items=extra_items)

if __name__ == '__main__':
    app.run(debug=True)