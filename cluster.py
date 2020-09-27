from annoy import AnnoyIndex
from scipy import spatial
import time
import os
import glob
import numpy as np

dims = 1792
n_nearest_neighbors = 20
trees = 10000

fname = 'index.ann'

t = AnnoyIndex(dims, metric='angular')

if os.path.exists(fname):
	t.load(fname)

def add_cluster(index, vectornya):
	# file_vector = np.loadtxt(path)
	t.add_item(index, vectornya)


def create_index():
	allfiles = glob.glob('features/*.npz')

	for file_index, i in enumerate(allfiles):
		print(file_index)
		file_vector = np.loadtxt(i)
		t.add_item(file_index, file_vector)


def save():
	t.build(trees)
	t.save(fname)

# nearest_neighbors = t.get_nns_by_item(i, n_nearest_neighbors)
# similarity = 1 - spatial.distance.cosine(master_vector, neighbor_file_vector)


if __name__ == '__main__':

	create_index()
	save()