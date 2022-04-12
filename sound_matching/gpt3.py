import os
import openai

openai.api_key = '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'
CONTEXT_PROMPT = "Use the words: ({},{}) in one short sentence (no more than 10 words)."

def score_matches_with_clip(images, text):
    pass

def generate_sentance(word_1, word_2,prompt=CONTEXT_PROMPT):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt.format(word_1,word_2),
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    sentence = response['choices'][0]['text']
    return sentence


def try_many(word_1,word_2):
    prompt_arr =["(bank, bench) -> a bench near a bank\n(chair, person) -> a person sitting on a chair \n(to go, dog) -> the dog goes near the house\n(car, tree) -> the car parks near the tree\n(women, tree) -> a woman holds Christmas tree\n(car, flower) -> there is a flower inside the car \n(wave, grass) -> the wind makes the grass move like waves \n(Money, water) -> water is money in the future \n(Google, chair) -> Google has a chair in its office \n({},{})->",
                "(bank, bench) -> a *bench* near a *bank*\n(chair, person) -> a *person* sitting on a *chair* \n(car, tree) -> the *car* parks near the *tree*\n(women, tree) -> a *woman* holds Christmas *tree*\n(car, flower) -> there is a *flower* inside the *car* \n(wave, grass) -> the wind makes the *grass* move like *waves* \n(money, water) -> *water* is *money* in the future \n(Google, chair) -> *Google* has a *chair* in its office \n({},{})->",
                "Use the words: ({},{}) in one sentence.",
                 "Use the words: ({},{}) in one funny sentence.",
                 "Use the words: ({},{}) in one catchy sentence.",
                 "Use the words: ({},{}) in one short sentence.",
                 "Use the words: ({},{}) in one short sentence (no more than 10 words)."]
    prompt_arr_old =["(bank, bench) -> a bench near a bank\n(chair, person) -> a person sitting on a chair \n(to go, dog) -> the dog goes near the house\n(car, tree) -> the car parks near the tree\n(women, tree) -> a woman holds Christmas tree\n(car, flower) -> there is a flower inside the car \n(wave, grass) -> the wind makes the grass move like waves \n(Money, water) -> water is money in the future \n(Google, chair) -> Google has a chair in its office \n({},{})->",
                 "combine the next 2 words to a one sentence: {},{}",
                 "combine the next 2 words to a one funny sentence: {},{}",
                 "combine the next 2 words to a one interesting sentence: {},{}",
                 "give me a sentence that combines the following 2 words: {},{}",
                 "please give me a sentence that combines the following 2 words: {},{}",
                 "give me a sentence that combines the following exact 2 words: {},{}",
                 "give me an easy to remember sentence exact 2 words: {},{}",
                 "give me a catchy sentence of the words: {},{}",
                 "I want a sentence from the following two words: ({},{})",
                 "Use the words: ({},{}) in one sentence."]


    for prompt in prompt_arr:
        print("*prompt*")
        print(prompt.format(word_1, word_2))
        sentence = generate_sentance(word_1, word_2,prompt)
        print("*sentence*")

        print(sentence)

if __name__ == '__main__':
    try_many("mafia", "lipstick")