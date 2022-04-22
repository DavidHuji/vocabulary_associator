from enum import EnumMeta
from icrawler.builtin import GoogleImageCrawler
from pathlib import Path
import os
import slugify
import clip
import numpy as np
import torch
from pkg_resources import packaging
import os

from PIL import Image
import numpy as np
from collections import OrderedDict
import torch

def check_if_meme(image_path):
    model, preprocess = clip.load("ViT-B/16")
    model.cuda().eval()
    images = []
    texts  = []
    descriptions = {
        "meme": "an image which contains text",
        "normal" : "an image which does not contains text"
    }
    image = Image.open(image_path).convert("RGB")
    images.append(preprocess(image))
    texts.append(descriptions['meme'])
    texts.append(descriptions['normal'])

    image_input = torch.tensor(np.stack(images))
    text_tokens = clip.tokenize(["This is " + desc for desc in texts])

    with torch.no_grad():
        image_features = model.encode_image(image_input.cuda()).float()
        text_features = model.encode_text(text_tokens.cuda()).float()

    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    similarity = text_features.cpu().numpy() @ image_features.cpu().numpy().T
    return similarity

def generate_image(sentence, max_num=4):
    Path("./examples").mkdir(parents=True, exist_ok=True)
    Path("./downloaded").mkdir(parents=True, exist_ok=True)
    
    from icrawler.builtin import GoogleImageCrawler

    sub_images_dir_name = slugify.slugify(sentence, separator='_')

    images_dir = r'./downloaded/{}'.format(sub_images_dir_name)
    images_dir = os.path.abspath(images_dir)

    google_Crawler = GoogleImageCrawler(storage={'root_dir': images_dir})
    google_Crawler.crawl(keyword=sentence, max_num=max_num * 6)

    # images_path_arr = []
    # if os.path.exists(images_dir):
    #     images_path_arr = os.listdir(images_dir)
    #     images_path_arr = [os.path.join(images_dir, x) for x in images_path_arr]
    #     print("Images are saved in {}".format(images_dir))
    images_path_arr = os.listdir(images_dir)
    images_path_arr = [os.path.join(images_dir,x) for x in images_path_arr]

    none_meme = None
    for idx , candidate in enumerate(images_path_arr):
        if idx == len(images_path_arr) - 1:
            none_meme = candidate
            break
        res = check_if_meme(candidate)
        is_text = res[0][0]
        not_text = res[1][0]
        if is_text <= not_text:
            none_meme = candidate
            break

    for img in images_path_arr:
        if img != none_meme:
            os.system('rm {}'.format(img))
    images_path_arr = [none_meme]
    return images_path_arr
    
if __name__ == '__main__':
    generate_image("bunny with carrot")