import os

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw_data')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_data')

MODEL_DIR = os.path.abspath(os.path.join(__file__, "..",".."))
SAVE_MODEL_DIR = os.path.join(MODEL_DIR, "saved")  

print(SAVE_MODEL_DIR)
print(RAW_DATA_PATH)
print(PROCESSED_DATA_PATH)


import joblib

model = joblib.load(os.path.join(SAVE_MODEL_DIR, "model_latest.pkl"))
text = "Cum se intampla ?"
prediction = model.predict([text])[0]

print("Intenție:", prediction)


