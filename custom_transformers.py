from sklearn.base import TransformerMixin, BaseEstimator
import numpy as np
import pandas as pd


class DateParser(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        # Handles both strings and already-datetime values
        X["Time"] = pd.to_datetime(X["Time"], errors="raise")
        return X


class WeekendAdder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X["business_day"] = [int(np.is_busday(d)) for d in X["Time"].values.astype("M8[D]")]
        return X


class HourAdder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X["hour"] = [pd.to_datetime(d).hour for d in X["Time"].values]
        return X


class DropTime(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.drop("Time", axis=1)