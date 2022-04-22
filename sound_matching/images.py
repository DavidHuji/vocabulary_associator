from pathlib import Path
import slugify
import clip
import os

from PIL import Image
import numpy as np
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)
model.eval()

texts = []
descriptions = {
    "meme": "a photo of a meme",
    "normal": "a nice photo",
}
texts.append(descriptions['meme'])
texts.append(descriptions['normal'])
text_tokens = clip.tokenize(["This is " + desc for desc in texts])
with torch.no_grad():
    text_features = model.encode_text(text_tokens).float()
text_features /= text_features.norm(dim=-1, keepdim=True)


def check_if_meme(image_path):
    images = []
    image = Image.open(image_path).convert("RGB")
    images.append(preprocess(image))

    image_input = torch.tensor(np.stack(images))

    with torch.no_grad():
        image_features = model.encode_image(image_input).float()

    image_features /= image_features.norm(dim=-1, keepdim=True)
    similarity = text_features.numpy() @ image_features.numpy().T
    return similarity


def generate_image(sentence, max_num=4):
    Path("./examples").mkdir(parents=True, exist_ok=True)
    Path("./downloaded").mkdir(parents=True, exist_ok=True)
    
    from icrawler.builtin import GoogleImageCrawler

    sub_images_dir_name = slugify.slugify(sentence, separator='_')

    images_dir = r'./downloaded/{}'.format(sub_images_dir_name)
    images_dir = os.path.abspath(images_dir)

    google_Crawler = GoogleImageCrawler(storage={'root_dir': images_dir})
    google_Crawler.crawl(keyword=sentence, max_num=max_num * 3)

    # images_path_arr = []
    # if os.path.exists(images_dir):
    #     images_path_arr = os.listdir(images_dir)
    #     images_path_arr = [os.path.join(images_dir, x) for x in images_path_arr]
    #     print("Images are saved in {}".format(images_dir))
    images_path_arr = os.listdir(images_dir)
    images_path_arr = [os.path.join(images_dir,x) for x in images_path_arr]

    none_meme = None
    mem_probability = []
    for idx, candidate in enumerate(images_path_arr):
        res = check_if_meme(candidate)
        is_text = res[0][0]
        mem_probability.append(is_text)
        not_text = res[1][0]
        print("is_text, not_text", is_text, not_text)
        # if is_text <= not_text or idx == len(images_path_arr) - 1:
        #     none_meme = candidate
        #     break
    print("mem_probability", mem_probability)
    best_idx = np.argpartition(mem_probability, max_num)[:max_num]
    # for img in images_path_arr:
    #     if img != none_meme:
    #         print("Deleting {}".format(img))
    #         os.system('rm {}'.format(img))
    images_path_arr = [images_path_arr[best_idx[i]] for i in range(len(best_idx))]
    return images_path_arr


if __name__ == '__main__':
    generate_image("you have to go back this way", max_num=4)