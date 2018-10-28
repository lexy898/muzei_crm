from difflib import SequenceMatcher
from common import request_utility
import db_helper
import json
import io

URL = "https://catalog.api.2gis.ru/3.0/items"

restaurants = db_helper.get_all_restaurants()

params = {"viewpoint1": "30.299884814697247,59.93814922241865", "viewpoint2": "30.331127185302716,59.92876411369677",
          "type": "street,adm_div.city,crossroad,adm_div.settlement,station,building,adm_div.district,road,"
                  "adm_div.division,adm_div.region,adm_div.living_area,attraction,adm_div.place,"
                  "adm_div.district_area,branch,parking,gate,route",
          "page": "1", "page_size": "12", "locale": "ru_RU",
          "fields": "request_type,items.adm_div,items.context,items.attribute_groups,items.contact_groups,"
                    "items.flags,items.address,items.rubrics,items.name_ex,items.point,items.geometry.centroid,"
                    "items.region_id,items.segment_id,items.external_content,items.org,items.group,items.schedule,"
                    "items.timezone_offset,items.ads.options,items.stat,items.reviews,items.purpose,search_type,"
                    "context_rubrics,search_attributes,widgets,filters",
          "stat[sid]": "2549eaf8-29e2-49d9-be64-4f604874b6a6", "stat[user]": "e4e82969-b688-4206-8789-23bb84b417f8",
          "key": "rulikm8232"}

two_gis_types = []
with io.open('2gis_types.txt', encoding='utf-8') as file:
    for line in file:
        two_gis_types.append(line.replace('\n', ''))

for restaurant in restaurants:
    if restaurant.name != '-':
        params.update({'q': restaurant.name})

        response = request_utility.do_request(url=URL, params=params)
        parsed_string = json.loads(response.content)
        try:
            items = parsed_string.get('result', '').get('items', '')
            if items:
                item = items[0]
                two_gis_name = item.get('name_ex').get('primary')
                try:
                    two_gis_type = item.get('rubrics')[0].get('name')
                except IndexError:
                    two_gis_type = '-'
                entry_type = two_gis_type in two_gis_types
                sm_name = SequenceMatcher(None, restaurant.name.lower(), two_gis_name.lower()).ratio()
                print(restaurant.name + ' и ' + two_gis_name + ' : index = ' + str(sm_name))
                print('entry_type: ' + str(entry_type))
        except AttributeError:
            continue
