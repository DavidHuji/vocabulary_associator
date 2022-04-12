from icrawler.builtin import GoogleImageCrawler
from pathlib import Path
import os
import slugify

def generate_image(sentence,max_num=4):
    Path("./examples").mkdir(parents=True, exist_ok=True)
    Path("./downloaded").mkdir(parents=True, exist_ok=True)
    
    from icrawler.builtin import GoogleImageCrawler

    sub_images_dir_name = slugify.slugify(sentence, separator='_')

    images_dir = r'./downloaded/{}'.format(sub_images_dir_name)
    images_dir = os.path.abspath(images_dir)

    google_Crawler = GoogleImageCrawler(storage={'root_dir': images_dir})
    google_Crawler.crawl(keyword=sentence, max_num=max_num)

    images_path_arr = os.listdir(images_dir)
    images_path_arr = [os.path.join(images_dir,x) for x in images_path_arr]
    return images_path_arr
    
if __name__ == '__main__':
    generate_image("bunny with carrot")