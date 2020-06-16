import requests
import json
import sys
import argparse
import os.path
from collections import OrderedDict

downloads_path = "./downloads"
stl_path = os.path.join(downloads_path, "stls")
json_path = os.path.join(downloads_path, "json")

if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)
if not os.path.exists(stl_path):
    os.makedirs(stl_path)
if not os.path.exists(json_path):
    os.makedirs(json_path)

thingiverse_api_base = "https://api.thingiverse.com/"
access_keyword = "?access_token="
# Go to https://www.thingiverse.com/apps/create and create your own Desktop app
api_token = os.environ.get('API_TOKEN')

rest_keywords = {
    "users": "users/",
    "likes": "likes/",
    "things": "things/",
    "files": "/files",
    "search": "search/",
    "pages": "&page=",
    "sort": "&sort={}", # relevant, text, popular, makes, newest
    "license": "&license={}" # cc, cc-sa, cc-nd, cc-nc-sa, cc-nc-nd, pd0, gpl, lgpl, bsd
}

hall_of_fame = []
all_files_flag = False

def load_data():
    # Load the data from the file to a list
    if os.path.isfile("hall_of_fame.list"):
        file = open("hall_of_fame.list", "r")
        hall_of_fame = file.readlines()
        file.close()
        # Removing \n
        hall_of_fame = [x.strip() for x in hall_of_fame]

    # for n in hall_of_fame:
    #     print(n)
    # else:
    #     print("Hall of fame file not found")


def save_data():
    # Save the data
    ordered_halloffame = list(OrderedDict.fromkeys(hall_of_fame))
    ordered_halloffame.sort()
    file = open("hall_of_fame.list", "w")
    for user in ordered_halloffame:
        try:
            file.write(user)
        except:
            print("Error in name: {}".format(user))
            file.write(user)
            continue
    file.close()

def generic_search(term=None, sort_type=None, license=None, n_pages=1):
    for idx in range(n_pages):
        file_name = "search"
        print("\n\nPage: {}".format(idx + 1))
        rest_url = thingiverse_api_base + rest_keywords["search"]
        if term and isinstance(term, str):
            rest_url += term
            file_name += "_"
            file_name += term.replace(" ", "_")
        rest_url += access_keyword + api_token + rest_keywords["pages"] + str(idx + 1)
        if sort_type and isinstance(sort_type, str):
            rest_url += rest_keywords["sort"].format(sort_type)
            file_name += "_"
            file_name += sort_type
        if license and isinstance(license, str):
            rest_url += rest_keywords["license"].format(license)
        file_name += ".json"
        print("url: {}".format(rest_url))
        download_objects(rest_url, file_name, "search")

def relevant(n_pages=1):
    generic_search(sort_type="relevant", n_pages=n_pages)

def text(n_pages=1):
    generic_search(sort_type="text", n_pages=n_pages)

def popular(n_pages=1):
    generic_search(sort_type="popular", n_pages=n_pages)

def makes(n_pages=1):
    generic_search(sort_type="makes", n_pages=n_pages)

def newest(n_pages=1):
    generic_search(sort_type="newest", n_pages=n_pages)


def user(username, n_pages=1):
    # /users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url = thingiverse_api_base + \
            rest_keywords["users"]+username+"/"+rest_keywords["things"] + \
            access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        print(rest_url)
        download_objects(rest_url, str(username+".json"))


def likes(username, n_pages=1):
    # /users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url = thingiverse_api_base + \
            rest_keywords["users"]+username+"/"+rest_keywords["likes"] + \
            access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        # print(rest_url)
        download_objects(rest_url, str(username+"_likes.json"))


def parser_info(rest_url, file_name):
    s = requests.Session()  # It creates a session to speed up the downloads
    r = s.get(rest_url)
    data = r.json()

    # Save the data
    file = open(file_name, "w")
    file.write(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
    file.close()

    # Reading the json file
    file = open(file_name, "r")
    data_pd = json.loads(file.read())

    # The page has objects?
    if (len(data_pd) == 0):
        print("\n\nNo more pages- Finishing the program")
        save_data()
        sys.exit()

    # Is it an error page?
    for n in data_pd:
        if (n == "error"):
            print("\n\nNo more pages- Finishing the program")
            save_data()
            sys.exit()

    print("Parsing data from {} objects from thingiverse".format(len(data_pd)))

    for object in range(len(data_pd)):

        object_id = str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"], data_pd[object]["public_url"]))

        # Name and last name
        print("Name: {} {}".format(data_pd[object]["creator"]
                                   ["first_name"], data_pd[object]["creator"]["last_name"]))

        # If the name and last name are empty, we use the username
        # TODO check if the name is already on the list or is new->call the twitter api
        # 3 in [1, 2, 3] # => True
        if (data_pd[object]["creator"]["first_name"] == "" and data_pd[object]["creator"]["last_name"] == ""):
            hall_of_fame.append(data_pd[object]["creator"]["name"]+"\n")
        else:
            hall_of_fame.append(data_pd[object]["creator"]["first_name"] +
                                " "+data_pd[object]["creator"]["last_name"]+"\n")


def download_objects(rest_url, file_name, mode = "none"):

    s = requests.Session()  # It creates a session to speed up the downloads
    r = s.get(rest_url)
    data = r.json()

    # Save the data
    json_file_path = os.path.join(json_path, file_name)
    json_file = open(json_file_path, "w")

    # print(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False)) # debug print
    json_file.write(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
    json_file.close()

    # Reading the json file
    json_file = open(json_file_path, "r")
    data_pd = json.loads(json_file.read())

    if mode == "search":
        data_pd = data["hits"]

        # The page has objects?
        if (data_pd is None):
            print("\n\nNo more pages- Finishing the program")
            save_data()
            sys.exit()

        # Is it an error page?
        for n in data_pd:
            if (n == "error"):
                print("\n\nNo more pages- Finishing the program")
                save_data()
                sys.exit()
    else:
        data_pd = data

        # The page has objects?
        if (len(data_pd) == 0):
            print("\n\nNo more pages- Finishing the program")
            save_data()
            sys.exit()

        # Is it an error page?
        for n in data_pd:
            if (n == "error"):
                print("\n\nNo more pages- Finishing the program")
                save_data()
                sys.exit()



    print("Downloading {} objects from thingiverse".format(len(data_pd)))
    # print(data_pd)

    for object in range(len(data_pd)):
        # print(object)
        # print(data_pd[object])
        object_id = str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"], data_pd[object]["public_url"]))
        print("Object id: {}".format(object_id))

        file_path = os.path.join(stl_path, data_pd[object]["name"].replace(" ", "_").replace("/", "-"))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        else:
            print("\nSkipping already downloaded object")
            continue

        # User name
        print("{} {}".format(data_pd[object]["creator"]["first_name"],
                             data_pd[object]["creator"]["last_name"]))

        # If the name and last name are empty, we use the username
        if (data_pd[object]["creator"]["first_name"] == "" and data_pd[object]["creator"]["last_name"] == ""):
            hall_of_fame.append(data_pd[object]["creator"]["name"]+"\n")
        else:
            hall_of_fame.append(data_pd[object]["creator"]["first_name"] +
                                " "+data_pd[object]["creator"]["last_name"]+"\n")
            # GET /things/{$id}/files/{$file_id}

        # Get file from a things
        r = s.get(thingiverse_api_base+rest_keywords["things"] +
                  object_id+rest_keywords["files"]+access_keyword+api_token)
        # print(r)
        # print(thingiverse_api_base+rest_keywords["things"]+object_id+rest_keywords["files"]+access_keyword+api_token)
        files_info = r.json()

        for file in range(len(files_info)):

            if (all_files_flag):  # Download all the files
                print("    "+files_info[file]["name"])
                # Download the file
                download_link = files_info[file]["download_url"]+access_keyword+api_token
                print(download_link)
                r = s.get(download_link)
                with open(file_path+"/"+files_info[file]["name"], "wb") as code:
                    code.write(r.content)
            else:  # Download only the .stls
                if(files_info[file]["name"].find(".stl")) != -1:
                    print("    "+files_info[file]["name"])
                    # Download the file
                    download_link = files_info[file]["download_url"]+access_keyword+api_token
                    print(download_link)
                    r = s.get(download_link)
                    with open(file_path+"/"+files_info[file]["name"], "wb") as code:
                        code.write(r.content)


if __name__ == "__main__":

    print("\nTHINGISCRAPE")
    print("Complex Additive Materials Group")
    print("University of Cambridge")

    parser = argparse.ArgumentParser()

    parser.add_argument("--newest", type=bool, dest="newest_true",
                        help="It takes the newest objects uploaded")

    parser.add_argument("--popular", type=bool, dest="popular_true",
                        help="It takes the most popular objects uploaded")

    parser.add_argument("--user", type=str, dest="username",
                        help="Downloads the object of a specified user")

    parser.add_argument("--pages", type=int, default=1,
                        help="Defines the number of pages to be downloaded.")

    parser.add_argument("--all", type=bool, default=False,
                        help="Download all the pages available (MAX 1000).")

    parser.add_argument("--likes", type=str, dest="likes",
                        help="Downloads the likes of a specified user")

    parser.add_argument("--search", type=str, dest="keywords",
                        help="Downloads the objects that match the keywords. 12 objects per page\n Example: --search 'star wars'")
    parser.add_argument("--all-files", type=bool, dest="all_files",
                        help="Download all the files, images, stls and others\n Example: --all-files True")

    args = parser.parse_args()

    load_data()

    if args.all:
        args.pages = 1000
    if args.all_files:
        all_files_flag = True

    if args.newest_true:
        newest(args.newest_true)
    if args.popular_true:
        popular(args.popular_true)
    elif args.username:
        user(args.username, args.pages)
    elif args.likes:
        likes(args.likes, args.pages)
    elif args.keywords:
        generic_search(args.keywords, args.pages)
    else:
        newest(1)