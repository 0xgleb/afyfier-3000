# Weights

Download `model_CWI_full.h5` and put it in `./backend/assets`

# Dependencies
```shell
pip install tensorflow
pip install wordfreq
pip install transformers
pip install torch
pip install scikit-learn
pip install sentence-transformers # this dependency requires Rust
pip install nltk
pip install flask
```

# Run the backend
```shell
FLASK_APP=server.py flask run &
```

you can test it with:
```shell
curl -XPOST -F text='this is some simple text' localhost:5000/afyfy
```

# Examples

- Fraud prevention agencies - we will let fraud prevention agencies know if you give us false or fraudulent information.
- This will involve checking the following information about you
  ->
  This will include checking the following information about you
- Where Habito is the relevant lender, we will also carry out the above actions. Where you have applied for one of Habito’s mortgage products through a third party intermediary...
  ->
  Where Habito is the relevant lender, we will also carry out the above actions. Where you have applied for one of your's mortgage ##s through a third party intermediary...
- Fraud prevention agencies can hold your personal data for different periods of time. If you are considered to pose a risk of fraud or money laundering, your personal data can be held for up to six years.
  ->
  Ffraud prevention organizations can hold your personal data for different amounts of time. If you are considered to present a risk of fraud or money laundering, your personal data can be held for up to six years.
- To determine the appropriate retention period for personal data, we consider the amount, nature and sensitivity of the personal data, the potential risk of harm from unauthorised use or disclosure of your personal data, the purposes for which we process your personal data and whether we can achieve those purposes through other means, and the applicable legal, regulatory, tax, accounting or other requirements."
  ->
  To decide the proper storage period for personal data, we consider the amount, nature and sensitivity of the personal data, the potential risk of harm from unauthorised use or disclosure of your personal data, the reasons for which we process your personal data and whether we can achieve those uses through other means, and the applicable legal, regulatory, tax, accounting or other requirements.


