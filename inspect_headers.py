import pandas as pd
import glob

files = [
    r"api_data_aadhar_enrolment\api_data_aadhar_enrolment\api_data_aadhar_enrolment_0_500000.csv",
    r"api_data_aadhar_biometric\api_data_aadhar_biometric\api_data_aadhar_biometric_0_500000.csv",
    r"api_data_aadhar_demographic\api_data_aadhar_demographic\api_data_aadhar_demographic_0_500000.csv"
]

for f in files:
    try:
        df = pd.read_csv(f, nrows=2)
        print(f"FILE: {f}")
        print(f"COLS: {df.columns.tolist()}")
    except Exception as e:
        print(e)
