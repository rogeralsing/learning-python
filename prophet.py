import pandas as pd
from fbprophet import Prophet


def predict(data, params):
    df = pd.DataFrame(data)

    if "ds" not in df.columns or "y" not in df.columns:
        return None

    df.ds = pd.to_datetime(df.ds)
    params = params if params else dict()
    model = Prophet(weekly_seasonality=True, daily_seasonality=False)
    model.fit(df)
    future = model.make_future_dataframe(**params)
    forecast = model.predict(future)
    return forecast
