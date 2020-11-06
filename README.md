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
