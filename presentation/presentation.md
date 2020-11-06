## Afyfier 3000

<img src="http://localhost:5000/presentation/images/team.png" />

---
## We want to drive financial literacy

---
## Problem

There are many financial documents but only one Afy.

---
## Solution

Create a digital version of Afy so that everyone can get help with their confusing documents.

---
## Remove jargon

The first thing we want to do is automatically remove jargon. Before we can remove jargon, we need to identify it.

---
## How to identify jargon?

As the first approximation, let's say that jargon is complex/uncommon words. We can train a neural network that will take a piece of text and identify which words are complex.

---
## How to replace jargon?

This is where BERT will help us.

<img src="http://localhost:5000/presentation/images/bert.png" />

---
## Who is BERT?

BERT was born at Google and his full name is "Bidirectional Encoder Representations from Transformers".

The version of BERT that Afyfier 3000 uses has 340M parameters. It was trained on the BooksCorpus with 800 million words, and the English version of Wikipedia with 2.5 billion words.

---
<img src="http://localhost:5000/presentation/images/bert-transformer.png" />

---
## How did it learn?

BERT learned everything he knows by doing 2 things: reading a piece of text and predicting the next sentence and removing different words from text and guessing the missing word.

---
## This is great

We also want to replace words in text and that's exactly what BERT does.

---
## Need to evaluate suggestions

BERT can generate thousands of suggestions but which ones do we want to use?

---
## Condition 1: high confidence

We will only take suggestions from BERT that he's confident in.

---
## Condition 2: sentence similarity

We can check similarity of sentences by using cosine similarity.

<img src="http://localhost:5000/presentation/images/similarity.png" />

---
## Condition 3: simplification

We are trying to make the text simpler, and not harder. So if BERT suggests words that are more complex than the original then we'll through them away.

---
## Afyfier 3000

What we do:
1. take the input sentence
2. use a neural network to identify complex words
3. for each complex word we get alternatives from BERT
4. take only confident suggestions
---
5. replace the complex word with each suggestion and compare similarity with the original
6. take top 2 most similar suggestions and add the original word to the list
7. take the simplest word out of the (maximum) 3 options
8. replace the target word in the text and repeat for the next complex word

---
## Demo


---
## What's next?

---
## Free stuff

Using transformers we can get things like summarization and question answering with average results essentially for free.

---
## Fine-tuning

We can fine-tune BERT for our specific domain and then it will perform better for us.

---
## True Afy

Afy doesn't just find and replace complex words, she fully re-writes the text. Digital Afy can do the same thing, in a similar way to how language translation works.

---
## Re-use other people's work

There are some scientific papers published about neural text simplification. We can model the more advanced version of the system after them.

---
## Questions?
