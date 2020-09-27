import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import glob
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# by default we don't sniff, ever
es = Elasticsearch()



from dataset import get_images
import cluster

module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
module = hub.load(module_handle)

def parse_image(data):
	img = tf.io.decode_jpeg(data, channels=3)
	img = tf.image.resize_with_pad(img, 224, 224)
	img = tf.image.convert_image_dtype(img,tf.float32)[tf.newaxis, ...]
	return img


def get_features(image, fname = False):
# def get_features(fname, image):
	# img = load_img(image)
	features = module(image)
	feature_set = np.squeeze(features)

	if fname:
		outfile_name = "features/{}.npz".format(fname)
		out_path = outfile_name
		np.savetxt(out_path, feature_set, delimiter=',')

	return feature_set


def gets():

	c = 0

	for img in get_images(300000):
		print(img['fname'])
		image = parse_image(img['data'])
		data = img['data']
		del img['data']
		fitur = get_features(image, fname = img['fname'])
		img['fitur'] = fitur
		

		yield img


def run():
	datas = gets()
	loop = True
	while loop:
		datbulk = []
		for c in range(0, 10):
			try:
				data = next(datas)
			except StopIteration as e:
				loop = False
				break

			print(data['fname'])

			payload = {
				'_id': data['fname'],
				'_index': 'images',
				'_source': data
			}

			datbulk.append(payload)

		bulk(es, datbulk)




if __name__ == '__main__':
	run()
