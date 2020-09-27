from process_image import get_features, es, parse_image
from dataset import req_image


# {
#   "mappings": {
#     "properties": {
#       "fitur": {
#         "type": "dense_vector",
#         "dims": 1792  
#       }
#     }
#   }
# }

def search(vector):

	payload = {
		"size" : 5,
		"_source": ['url'],
		"query":{
			
			"script_score": {
				"query": {
		        	"match_all": {}
		      	},
				"script":{
					"source": "1 / (1 + l2norm(params.queryVector, 'fitur'))",
			        "params": {
			          "queryVector": vector
			        }
				}
	      	}

		}
	}

	return es.search(index= 'images', body = payload)


if __name__ == '__main__':
	from pprint import pprint

	url = 'https://ecs7.tokopedia.net/img/cache/300/product-1/2018/2/7/0/0_1c83c109-b624-47c3-9850-15c2b02e66fa_1040_585.jpg'
	image = req_image(url)
	image = parse_image(image)
	vector = get_features(image)
	vector = vector.tolist()
	# print(vector.__len__())

	pprint(search(vector))