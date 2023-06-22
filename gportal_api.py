import requests
from utils import inside_polygon
import json
import numpy as np

DATASETS = {
  "l1b_VNR": "10001003",
  "l2_NWLR": "10002000",
  "l2_IWPR": "10002001"
}

class GportalApi:
  def __init__(self, token, type="l1b_VNR"):
    self.token = token
    self.baseurl = "https://gportal.jaxa.jp/gpr/search/catalog_records.json"
    self.headers = {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      "Host": "gportal.jaxa.jp",
      "Origin": "https://gportal.jaxa.jp",
      "Refer": "https://gportal.jaxa.jp/gpr/search?tab=1",
      "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"macOS\"",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",   
      "Sec-Fetch-Site": "same-origin",
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest",
      "Accept": "*/*",
      "Postman-Token": "bc583896-9316-4f49-af95-778359420bbf",
      "Accept-Encoding": "gzip, deflate, br",
      "Connection": "keep-alive",
      "Cookie": "fuel_csrf_token=%s"%token
    }
    self.dataset = DATASETS[type]

  def temp_fn(self):
    temp_body = {
      "dataset[0][id]": "10001003",
      "obsdate[0][from]": "2023/01/31",
      "obsdate[0][to]": "2023/02/07",
      "mapProjection": "EQ",
      "count": "1000",
      "fuel_csrf_token": self.token
    }
    return requests.post(self.baseurl, data=temp_body, headers=self.headers)

  def construct_polygon_coordinates(self, lat, long):
    lat1 = str(lat - 0.5)
    lat2 = str(lat + 0.5)
    long1 = str(long - 0.5)
    long2 = str(long + 0.5)
    polygon = "POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))"%(lat1, long1, lat2, long1, lat2, long2, lat1, long2, lat1, long1)
    return polygon
  
  def filter(self, coordinates, results):
    res = []
    for f in results['features']:
      poly = f['geometry']['coordinates']
      poly = np.array(poly)
      poly = poly.reshape((poly.shape[1], poly.shape[2]))
      poly = poly.T
      if inside_polygon(poly[0], poly[1], coordinates[0], coordinates[1]) == 1:
        res.append(f)
    return res

  def search(self, from_date, to_date, cloud=None, coordinates = None, identifier=None, count=1000, path_number=None, scene_number=None, resolution=None):
    body = {
      "dataset[0][id]": self.dataset,
      "obsdate[0][from]": from_date,
      "obsdate[0][to]": to_date,
      "mapProjection": "EQ",
      "count": "%i"%count,
      "fuel_csrf_token": self.token
    }
    if cloud:
      body["dataset[0][cloudCoverPercentage][value]"] = cloud
    if coordinates:
      body["coordinates"] = self.construct_polygon_coordinates(coordinates[0], coordinates[1])

    if identifier:
      body["dataset[0][Identifier][value]"] = identifier
    if path_number:
      body["dataset[0][OrbitNumber][op]"] = "="
      body["dataset[0][OrbitNumber][value]"] = path_number
      # body["dataset[0][OrbitNumber][to]"] = path_number
    if scene_number:
      body["dataset[0][sceneNumber][op]"] = "="
      body["dataset[0][sceneNumber][value]"] = scene_number
      # body["dataset[0][sceneNumber][to]"] = scene_number
    if resolution:
      body["dataset[0][Resolution][op]"] = "="
      body["dataset[0][Resolution][value][]"] = resolution
    
    res = requests.post(self.baseurl, data=body, headers=self.headers)
    results = json.loads(res.content)
    return self.filter(coordinates, results)
  
  def auth(self, account, password):
    body = {
      "account": account,
      "password": password,
      "fuel_csrf_token": self.token
    } 
    auth_url = "https://gportal.jaxa.jp/gpr/auth/authenticate.json"
    res = requests.post(auth_url, body, headers = self.headers)
    return res