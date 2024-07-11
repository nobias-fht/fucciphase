import numpy as np
import pandas as pd
from monotonic_derivative import ensure_monotonic_derivative


def fit_percentages(frames: np.ndarray, percentages: np.ndarray) -> np.ndarray:
    """Fit estimated percentages to function with non-negative derivative."""
    best_fit: np.ndarray = ensure_monotonic_derivative(
        x=frames,
        y=percentages,
        degree=1,
        force_negative_derivative=False,
    )
    return best_fit


def postprocess_estimated_percentages(df: pd.DataFrame, percentage_column: str) -> None:
    """Make estimated percentages continuous."""
    if percentage_column not in df:
        raise ValueError("The name of the percentage column is not in the DataFrame")
    indices = df["TRACK_ID"].unique()
    postprocessed_percentage_column = percentage_column + "_POST"
    df[postprocessed_percentage_column] = np.nan
    for index in indices:
        if index == -1:
            continue
        track = df[df["TRACK_ID"] == index]
        frames = track["FRAME"]
        percentages = track[percentage_column]
        restored_percentages = fit_percentages(frames, percentages)
        df.loc[
            df["TRACK_ID"] == index, postprocessed_percentage_column
        ] = restored_percentages
