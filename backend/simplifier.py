import re
import json
import torch
import numpy as np
import tensorflow as tf
from wordfreq import zipf_frequency
from transformers import BertTokenizer, BertModel, BertForMaskedLM
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk import pos_tag
# from nltk.corpus import stopwords

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

sbert_model = SentenceTransformer('bert-large-nli-mean-tokens')

# # idk if we need all of these, but just to be sure
# nltk.download('brown')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

pretrained_model_path = "./assets/model_CWI_full.h5"
model_cwi = tf.keras.models.load_model(pretrained_model_path)

# stop_words_ = set(stopwords.words('english'))
def cleaner(word):
  #Remove links
  word = re.sub(
    r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
    '', word, flags=re.MULTILINE
  )
  word = re.sub('[\W]', ' ', word)
  word = re.sub('[^a-zA-Z]', ' ', word)
  return word.lower().strip()

with open('assets/word2index.json', 'r') as fp:
  word2index = json.load(fp)

sent_max_length = 103 # from the training code from the google colab
def process_input(input_text):
  input_text = cleaner(input_text)
  clean_text = []
  index_list =[]
  input_token = []
  index_list_zipf = []
  for i, word in enumerate(input_text.split()):
    if word in word2index:
      clean_text.append(word)
      input_token.append(word2index[word])
    else:
      index_list.append(i)
  input_padded = pad_sequences(maxlen=sent_max_length, sequences=[input_token], padding="post", value=0)
  return input_padded, index_list, len(clean_text)

def complete_missing_word(pred_binary, index_list, len_list):
  list_cwi_predictions = list(pred_binary[0][:len_list])
  for i in index_list:
    list_cwi_predictions.insert(i, 0)
  return list_cwi_predictions

bert_model = 'bert-large-uncased'
tokenizer = BertTokenizer.from_pretrained(bert_model)
model = BertForMaskedLM.from_pretrained(bert_model)
model.eval()


with open('./assets/easy-word-list.txt', 'r') as file:
  simple_words = file.read().split(sep='\n')

def is_same_word(word_one, word_two):
  return (word_one[:len(word_one) - 1] in word_two) or (word_two[:len(word_two) - 1] in word_one)

def get_simplified_text(input_text, list_cwi_predictions, numb_predictions_displayed = 2):
  list_candidates_bert = []
  input_words = input_text.split()
  for current_word_index, (word, pred) in enumerate(zip(input_words, list_cwi_predictions)):
    isNotSimpleWord = word not in simple_words
    original_frequency = zipf_frequency(word, 'en')
    if (
        isNotSimpleWord and
        ((pred and (pos_tag([word])[0][1] in ['NNS', 'NN', 'VBP', 'RB', 'VBG','VBD' ])
        ) or
        (original_frequency < 3.1)
        )
    ):
      # remove punctuation
      word, punctuation = (word[:-1], word[len(word) - 1]) if word.endswith(',') or word.endswith('.') else (word, '')
      word, punctuation = (word.replace("'s", ''), "'s") if word.endswith("'s") else (word, '')
      print(word)

      # prepare the text
      replace_word_mask = input_words.copy()
      replace_word_mask[current_word_index] = '[MASK]' # maybe + punctuation
      space = " "

      # do the prediction
      text = f'[CLS]{space.join(replace_word_mask)} [SEP] {space.join(input_words)} [SEP] '
      tokenized_text = tokenizer.tokenize(text)
      masked_index = [i for i, x in enumerate(tokenized_text) if x == '[MASK]'][0]
      indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
      segments_ids = [0]*len(tokenized_text)
      tokens_tensor = torch.tensor([indexed_tokens])
      segments_tensors = torch.tensor([segments_ids])
      # Predict all tokens
      with torch.no_grad():
        outputs = model(tokens_tensor, token_type_ids=segments_tensors)
        predictions = outputs[0][0][masked_index]

      predicted_ids = torch.argsort(predictions, descending=True)
      numberAboveThreshold = len([
        pred for pred in torch.index_select(predictions, -1, predicted_ids) if pred > 15
      ])
      unfiltered_predicted_tokens = tokenizer.convert_ids_to_tokens(
        list(predicted_ids[:numberAboveThreshold])
      )

      predicted_tokens = [
        token for token in unfiltered_predicted_tokens if not is_same_word(token, word)
      ]

      print(predicted_tokens)

      new_options = []
      for token in predicted_tokens:
        replace_word_mask[current_word_index] = token + punctuation
        new_options.append((token, space.join(replace_word_mask)))

      if new_options:
        document_embeddings = sbert_model.encode(
          [input_text] + list(map(lambda tupple: tupple[1], new_options))
        )

        # print(new_options)

        pairwise_similarities = cosine_similarity(document_embeddings)

        options_with_similarity = []
        for i in range(len(new_options)):
          similarity = pairwise_similarities[0][i+1]
          options_with_similarity.append((new_options[i][0], new_options[i][1], similarity))

        options_with_similarity.sort(
          key=lambda tupple: tupple[2],
          reverse=True
        )

        # print(options_with_similarity)

        most_similar_options = [
          (option[0], option[1]) for option in options_with_similarity[:numb_predictions_displayed]
        ]

        most_similar_options.append((word, input_text))

        # print(most_similar_options)

        most_similar_options.sort(
          key=lambda tupple: zipf_frequency(tupple[0], 'en'),
          reverse=True
        )

        # print(most_similar_options)

        input_text = most_similar_options[0][1]
        # print(input_text)
        input_words = input_text.split()

  return input_text


list_texts = [
 'If an event of default occurs we may demand immediate repayment of the Loan in writing.\n While we will always try to work with you to agree a way forward, if a default event occurs and we’re unable to agree a solution with you, we may demand immediate repayment of your Loan.',
 'If you fail to keep to our Agreement, we may appoint a receiver to manage the Property. Although we will appoint the receiver, they will act on your behalf and you will pay their fees. We will, acting reasonably, agree the fees for the receiver’s services and you will be responsible for paying them. We (or a receiver) may also employ and pay agents to undertake some duties.',
 'Where joint receivers are appointed, each of them may act separately and independently, unless the document appointing them states otherwise.',
]

print("\n\n")

for input_text in list_texts:
  input_text = input_text.replace('’', "'")
  new_text = input_text
  input_padded, index_list, len_list = process_input(input_text)
  pred_cwi = model_cwi.predict(input_padded)
  pred_cwi_binary = np.argmax(pred_cwi, axis = 2)
  complete_cwi_predictions = complete_missing_word(pred_cwi_binary, index_list, len_list)

  simplified_text = get_simplified_text(
    input_text,
    complete_cwi_predictions,
  )

  print("\nOriginal text: ", input_text, '\n')
  print("\nSimplified text: ", simplified_text, '\n')

def afyfy(input_text):
  input_text = input_text.replace('’', "'")
  new_text = input_text
  input_padded, index_list, len_list = process_input(input_text)
  pred_cwi = model_cwi.predict(input_padded)
  pred_cwi_binary = np.argmax(pred_cwi, axis = 2)
  complete_cwi_predictions = complete_missing_word(pred_cwi_binary, index_list, len_list)

  simplified_text = get_simplified_text(
    input_text,
    complete_cwi_predictions,
  )
  return simplified_text
