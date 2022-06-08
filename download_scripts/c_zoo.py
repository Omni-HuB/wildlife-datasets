import os
import argparse
import utils
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default='../datasets',  help="Output folder")
parser.add_argument("--name", type=str, default='CZoo',  help="Dataset name")
args = parser.parse_args()

directory = os.path.join(args.output, args.name)
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(directory)

# Download and extract
url = 'https://github.com/cvjena/chimpanzee_faces/archive/refs/heads/master.zip'
archive = 'master.zip'
utils.download_url(url, archive)
utils.extract_archive(archive, delete=True)

# Cleanup
shutil.rmtree('chimpanzee_faces-master/datasets_cropped_chimpanzee_faces/data_CTai')
