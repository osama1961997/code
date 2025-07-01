from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ⛔ للسماح بالاتصال من Flutter أو أي متصفح
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # غيّر دي لنطاق تطبيقك في الإنتاج
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ تحميل الموديل المدرب
model = joblib.load("LAT_LONG_Tmax _model.pkl")

# ✅ تعريف الشكل المتوقع للبيانات
class EToInput(BaseModel):
    Tmax: float
    latitude: float
    longitude: float
    J: int  # يوم السنة

@app.post("/predict")
def predict_eto(data: EToInput):
    df = pd.DataFrame([data.dict()])
    eto = model.predict(df)[0]
    return {"eto": round(float(eto), 2)}
