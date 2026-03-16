# Test script to verify library installations
try:
    import pandas as pd
    print("pandas imported successfully")
except ImportError as e:
    print(f"pandas import failed: {e}")

try:
    import numpy as np
    print("numpy imported successfully")
except ImportError as e:
    print(f"numpy import failed: {e}")

try:
    import matplotlib.pyplot as plt
    print("matplotlib.pyplot imported successfully")
except ImportError as e:
    print(f"matplotlib.pyplot import failed: {e}")

try:
    import seaborn as sns
    print("seaborn imported successfully")
except ImportError as e:
    print(f"seaborn import failed: {e}")

try:
    from sklearn.model_selection import KFold
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    print("scikit-learn modules imported successfully")
except ImportError as e:
    print(f"scikit-learn import failed: {e}")

print("All import tests completed.")
