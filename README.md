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
- To determine the appropriate retention period for personal data, we consider the amount, nature and sensitivity of the personal data, the potential risk of harm from unauthorised use or disclosure of your personal data, the purposes for which we process your personal data and whether we can achieve those purposes through other means, and the applicable legal, regulatory, tax, accounting or other requirements.
