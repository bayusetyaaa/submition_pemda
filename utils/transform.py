import pandas as pd
import numpy as np
from datetime import datetime

def transform_data(data_product):
    if not data_product:
        return pd.DataFrame(columns=['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp'])

    df = pd.DataFrame(data_product)

    if 'title' in df.columns:
        df = df[~df['title'].str.lower().str.contains('unknown', na=False)]

    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
    df['price'] = df['price'].replace('', np.nan).infer_objects(copy=False)
    df.dropna(subset=['price'], inplace=True)
    df['price'] = df['price'].astype(float) * 16000

    df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True)
    df['rating'] = df['rating'].replace('', np.nan).infer_objects(copy=False)
    df.dropna(subset=['rating'], inplace=True)
    df['rating'] = df['rating'].astype(float)

    df['colors'] = df['colors'].replace(r'\D', '', regex=True)
    df['colors'] = df['colors'].replace('', np.nan).infer_objects(copy=False)
    df.dropna(subset=['colors'], inplace=True)
    df['colors'] = df['colors'].astype(int)

    df['size'] = df['size'].replace(r'Size:\s*', '', regex=True)
    df['gender'] = df['gender'].replace(r'Gender:\s*', '', regex=True)

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df
