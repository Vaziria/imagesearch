import io
import requests
import psycopg2
import psycopg2.extras

DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % ('localhost', 'postgres', 'postgres', 'heri7777')
dbConn = psycopg2.connect(DB_CONNECTION_STRING)
cur = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)

def get_images(limit = 300):
	qSelect = "SELECT images from product LIMIT {}".format(limit)
	cur.execute(qSelect)
	results = cur.fetchmany(50)
	
	while len(results) > 0:
		for row in results:
			for image in row['images']:

				fname = image.split('/')[-1]

				try:
					yield {
						'fname': fname,
						'data': req_image(image),
						'url': image
					}
				except Exception as e:
					print(e)

		results = cur.fetchmany(100)


def req_image(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
	}

	req = requests.get(url, headers = headers)
	if req.status_code == 200:
		return req.content

	return False

if __name__ == '__main__':

	for c in get_images():
		print(c)


