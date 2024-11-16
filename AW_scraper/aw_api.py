import requests
import json
import pandas as pd
import os
import datetime


url_parliaments = "https://www.abgeordnetenwatch.de/api/v2/parliaments"
url_parliament_periods = "https://www.abgeordnetenwatch.de/api/v2/parliament-periods"
url_politicians = "https://www.abgeordnetenwatch.de/api/v2/politicians"
url_candidacies_mandates = "https://www.abgeordnetenwatch.de/api/v2/candidacies-mandates"


def get_path():
    if os.path.isdir(os.path.join(os.getcwd(), "files")):
        save_path = os.path.join(os.getcwd(), "files")
    else:
        save_path = os.path.join(os.getcwd(), "AW_scraper","files")
    return save_path

def load_data(link, range_ = 50):
    x = 0
    json_list = list()
    while x >= 0:
        url_parliament_periods = link+f"?id[gte]={x}&id[lt]={x+range_}"
        myResponse = requests.get(url_parliament_periods)
        print(x)
        jData = json.loads(myResponse.content)
        if x == 0: 
#            print(jData)
            json_list.append(jData)
            x += 50
        else:
            if not json_list[-1]["data"]:
                z = x
                x = -1                
            else:
                x += 50
                json_list.append(jData)
    print(f"loaded {50*z} lines")
    return json_list()


def get_candidacies_mandates(save_path):
    print(f"candidacies mandates start: {datetime.datetime.now()}")
    url_candidacies_mandates = f"https://www.abgeordnetenwatch.de/api/v2/candidacies-mandates"
    json_list = load_data(url_candidacies_mandates)
    df_list = list()
    for i in json_list:
        candidacies_mandates_df = pd.DataFrame()
        counter = 0
        for key, value in i.items():
            if key == "data":
                for element in value:
                        if counter == 0:
                            try:
                                if element['parliament_period']['label'] != None:
                                    parliament_row = pd.DataFrame(element['parliament'], index=[counter])
                                    parliament_df = pd.concat([parliament_df, parliament_row], ignore_index=True)
                                    element = element | {'party': element['parliament']['label'] }
                                if element["politician"] != None:
                                    element = element | {'politician': element['politician']['label'] }
                            except:
                                pass
                            candidacies_mandates_df = pd.DataFrame(element, index = [counter])
                        else:
                            try:
                                if element['parliament']['label'] != None:
                                    parliament_row = pd.DataFrame(element['parliament'], index=[counter])
                                    parliament_df = pd.concat([parliament_df, parliament_row], ignore_index=True)
                                    element = element | {'party': element['parliament']['label'] }
                                if element["politician"] != None:
                                    element = element | {'politician': element['politician']['label'] }
                            except:
                                pass
                            row = pd.DataFrame(element, index = [counter])
                            candidacies_mandates_df = pd.concat([candidacies_mandates_df, row], ignore_index=True)
                        counter += 1
        df_list.append(candidacies_mandates_df)
    final_df = pd.concat(df_list)
    final_df.to_excel(os.path.join(save_path,"candidacies_mandate.xlsx"))
    print(f"candidacies mandates end: {datetime.datetime.now()} \n")



def get_parliament_periods(save_path):
    print(f"parliament periods start: {datetime.datetime.now()}")
    url_parliament_periods = f"https://www.abgeordnetenwatch.de/api/v2/parliament-periods"#?id[gte]={x}&id[lt]={x+50}"
    json_list = load_data(url_parliament_periods)
    df_list = list()
    for i in json_list:
        parliaments_periods_df = pd.DataFrame()
        counter = 0
        for key, value in i.items():
            if key == "data":
                for element in value:
                        if counter == 0:
                            try:
                                if element['parliament']['label'] != None:
                                    parliament_row = pd.DataFrame(element['parliament'], index=[counter])
                                    parliament_df = pd.concat([parliament_df, parliament_row], ignore_index=True)
                                    element = element | {'party': element['parliament']['label'] }
                                if element["previous_period"] != None:
                                    element = element | {'previous_period': element['previous_period']['label'] }
                            except:
                                pass
                            parliaments_periods_df = pd.DataFrame(element, index = [counter])

                        else:
                            try:
                                if element['parliament']['label'] != None:
                                    parliament_row = pd.DataFrame(element['parliament'], index=[counter])
                                    parliament_df = pd.concat([parliament_df, parliament_row], ignore_index=True)
                                    element = element | {'party': element['parliament']['label'] }
                                if element["previous_period"] != None:
                                    element = element | {'previous_period': element['previous_period']['label'] }
                            except:
                                pass

                            row = pd.DataFrame(element, index = [counter])
                            parliaments_periods_df = pd.concat([parliaments_periods_df, row], ignore_index=True)
                        counter += 1
        df_list.append(parliaments_periods_df)
    final_df = pd.concat(df_list)
    final_df.to_excel(os.path.join(save_path,"parliament_period.xlsx"))
    print(f"parliament periods end: {datetime.datetime.now()}\n")



def get_parliaments(save_path):
    print(f"parliaments start: {datetime.datetime.now()}")
    url_parliaments = f"https://www.abgeordnetenwatch.de/api/v2/parliaments?range_start={x}&range_end={x+50}"
    json_list = load_data(url_parliaments)
    df_list = list()
    df_list_projects = list()
    for i in json_list:
        parliaments_df = pd.DataFrame()
        project_df = pd.DataFrame()
        counter = 0

        for key, value in i.items():
            if key == "data":
                for element in value:
                    if counter == 0:
                        try:
                            if element['current_project']['label'] != None:
                                project_row = pd.DataFrame(element['current_project'], index=[counter])
                                project_df = pd.concat([project_df, project_row], ignore_index=True)
                                element = element | {'current_project': element['current_project']['label'] }
                        except:
                            pass
                        parliaments_df = pd.DataFrame(element, index = [counter])
                    else:
                        try:
                            if element['current_project']['label'] != None:
                                project_row = pd.DataFrame(element['current_project'], index=[counter])
                                project_df = pd.concat([project_df, project_row], ignore_index=True)
                                element = element | {'current_project': element['current_project']['label'] }
                        except:
                            pass
                        row = pd.DataFrame(element, index = [counter])
                        parliaments_df = pd.concat([parliaments_df, row], ignore_index=True)
                    counter += 1
        df_list.append(parliaments_df)
        df_list_projects.append(project_df)

    final_df_parliament = pd.concat(df_list)
    final_df_parliament.to_excel(os.path.join(save_path,"parliaments.xlsx"))
    final_project_df = pd.concat(df_list_projects)
    final_project_df.to_excel(os.path.join(save_path,"project.xlsx"))
    print(f"parliament end: {datetime.datetime.now()}\n")


def get_politicians( save_path):
    print(f"politicians start: {datetime.datetime.now()}")
    url_politicians = f"https://www.abgeordnetenwatch.de/api/v2/politicians"
    json_list = load_data(url_politicians)
    df_list = list()
    df_list_party = list()
    for i in json_list:
        politician_df = pd.DataFrame()
        party_df = pd.DataFrame()
        counter = 0
        for key, value in i.items():
            if key == "data":
                for element in value:
                    if counter == 0:
                        try:
                            if element['party']['label'] != None:
                                party_row = pd.DataFrame(element['party'], index=[counter])
                                party_df = pd.concat([party_df, party_row], ignore_index=True)
                                element = element | {'party': element['party']['label'] }
                            if element["party_past"] != None:
                                past_party_row = pd.DataFrame(element['party_past']['label'], index=[counter])
                                party_df = pd.concat([party_df, past_party_row], ignore_index=True)
                                element = element | {'party_past': element['party_past']['label'] }
                        except:
                            pass
                        politician_df = pd.DataFrame(element, index = [counter])
                    else:
                        try:
                            if element['party']['label'] != None:
                                party_row = pd.DataFrame(element['party'], index=[counter])
                                party_df = pd.concat([party_df, party_row], ignore_index=True)
                                element = element | {'party': element['party']['label'] }
                            if element["party_past"] != None:
                                past_party_row = pd.DataFrame(element['party_past'], index=[counter])
                                party_df = pd.concat([party_df, past_party_row], ignore_index=True)
                                element = element | {'party_past': element['party_past']['label'] }
                        except:
                            pass
                        row = pd.DataFrame(element, index = [counter])
                        politician_df = pd.concat([politician_df, row], ignore_index=True)
                    counter += 1
        df_list.append(politician_df)
        df_list_party.append(party_df)

    final_df_party = pd.concat(df_list)
    final_df_party.to_excel(os.path.join(save_path,"politicians.xlsx"))
    final_party_df = pd.concat(df_list_party)
    final_party_df.to_excel(os.path.join(save_path,"party.xlsx"))
    print(f"politicians end: {datetime.datetime.now()} \n")


save_path = get_path()
get_politicians(save_path)
get_parliament_periods(save_path)
# get_candidacies_mandates(save_path)
get_parliaments(save_path)
