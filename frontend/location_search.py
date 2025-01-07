import requests

def location_search(classification_response, data):
    address = classification_response.location
    response = requests.get(f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={address}&returnGeom=Y&getAddrDetails=Y&pageNum=1")
    lat = response.json()["results"][0]["LATITUDE"]
    lon = response.json()["results"][0]["LONGITUDE"]

    # Get 5 closest events based on location
    data['distance'] = ((data['lat'] - float(lat))**2 + (data['lon'] - float(lon))**2)**0.5
    output = data.sort_values(by='distance').head(20)

    # give a score of 0 to 1 based on distance
    output['score_location'] = 1 - output['distance'] / output['distance'].max()
    return output