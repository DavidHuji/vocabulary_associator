import os
import openai
from icrawler.builtin import GoogleImageCrawler

os.system('mkdir downloaded')
os.system('mkdir examples')
openai.api_key = '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'
context_prompt = "(bank, bench) -> a bench near a bank\n(chair, person) -> a person sitting on a chair \n(to go, dog) -> the dog goes near the house\n(car, tree) -> the car parks near the tree\n(women, tree) -> a woman holds Christmas tree\n(car, flower) -> there is a flower inside the car \n(wave, grass) -> the wind makes the grass move like waves \n(Money, water) -> water is money in the future \n(Google, chair) -> Google has a chair in its office \n"


def gen_sentence_and_image(word_1, word_2):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=context_prompt + str(f'({word_1}, {word_2}) ->'),
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    sentence = response['choices'][0]['text']

    sub_images_dir_name = '_'.join(sentence.split(' '))
    path_to_images = r'./downloaded/{}'.format(sub_images_dir_name)
    google_Crawler = GoogleImageCrawler(storage={'root_dir': path_to_images})
    google_Crawler.crawl(keyword=sentence, max_num=4)
    return sentence, path_to_images


def deployment_get_sentence_and_image(word_1, word_2, string_prefix):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=context_prompt + str(f'({word_1}, {word_2}) ->'),
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    sentence = response['choices'][0]['text']

    sub_images_dir_name = '_'.join(sentence.split(' '))
    path_to_images = r'./examples/{}'.format(string_prefix + sub_images_dir_name)
    google_Crawler = GoogleImageCrawler(storage={'root_dir': path_to_images})
    google_Crawler.crawl(keyword=sentence, max_num=3)
    return sentence, path_to_images


def score_matches_with_clip(images, text):
    pass


if __name__ == '__main__':
    sentence, path_to_images = gen_sentence_and_image('rightly', 'staunchest')
    print(sentence)