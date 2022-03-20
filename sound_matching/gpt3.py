import os
import openai
from icrawler.builtin import GoogleImageCrawler

os.system('mkdir downloaded')

openai.api_key =  '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'

prompt = "(bank, bench) -> a bench near a bank\n(chair, person) -> a person sitting on a chair \n(go, dog) -> the dog goes near the house\n(car, tree) -> the car parks near the tree\n(women, tree) -> a woman holds Christmas tree\n(car, flower) -> there is a flower inside the car \n(wave, grass) -> the wind makes the grass move like waves \n(Money, water) -> water is money in the future \n(Google, chair) -> Google has a chair in its office \n"

# write the query here
prompt += '(cat, star) ->'

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=prompt,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

sentence = response['choices'][0]['text']

sub_images_dir_name = '_'.join(sentence.split(' '))
google_Crawler = GoogleImageCrawler(storage = {'root_dir': r'./downloaded/{}'.format(sub_images_dir_name)})
google_Crawler.crawl(keyword = sentence, max_num = 20)

