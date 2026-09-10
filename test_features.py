# paste this at the bottom of models/train.py temporarily, or run in a python shell

from data.fetch import get_price_history
from features.engineer import engineer_features

df = get_price_history("RELIANCE.NS", period="2y")
df = engineer_features(df)

print(df.columns.tolist())
print(df.shape)