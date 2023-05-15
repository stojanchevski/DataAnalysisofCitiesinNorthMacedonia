import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://dbpedia.org/sparql"
query = '''
SELECT DISTINCT ?town
WHERE {
  <http://dbpedia.org/resource/List_of_cities_in_North_Macedonia> dbo:wikiPageWikiLink ?town.
}
'''

query2 = '''
SELECT ?populationTotal
WHERE {{
  <{city_url}> dbo:populationTotal ?populationTotal.
}}
'''


params = {
    "format": "json",
    "query": query
}

response = requests.get(url, params=params)
data = response.json()

if "results" in data and "bindings" in data["results"]:
    unique_cities = set()
    for result in data["results"]["bindings"]:
        towns = result["town"]["value"]
        unique_cities.add(towns)

    city_data_list = []

    for city_url in unique_cities:
        params["query"] = query2.format(city_url=city_url)
        response = requests.get(url, params=params)
        city_data = response.json()

        if "results" in city_data and "bindings" in city_data["results"] and len(city_data["results"]["bindings"]) > 0:
            population_total = city_data["results"]["bindings"][0]["populationTotal"]["value"]
            city_data_list.append({"City": city_url, "Population Total": population_total})

            df = pd.DataFrame(city_data_list)
            df_top_5 = df.head(5)

            df_top_5["Population Total"] = pd.to_numeric(df_top_5["Population Total"])

            plt.figure(figsize=(10, 6))
            sns.barplot(y="City", x="Population Total", data=df_top_5, orient="h")
            plt.xlabel("Population Total")
            plt.ylabel("City")
            plt.title("Population Total for the First 5 Cities")
            plt.tight_layout()
            plt.show()