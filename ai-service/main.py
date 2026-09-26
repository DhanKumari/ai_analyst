from fastapi import FastAPI, UploadFile, File, HTTPException 
import pandas as pd

app = FastAPI(title="AI Service")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-service"
    }



@app.post("/profile/")
async def profile_excel(file:UploadFile = File(...)):
    # UploadFile → What is the data represented as?
    # File(...)   → Where/how should FastAPI receive it?
    
    #check file extension
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException( 
            status_code=400, 
            detail="Only .xlsx Excel files are allowed." )

    try:
        # here file is the FastAPI uploadFile object
        #read the Excel file that FastAPI received.
        df = pd.read_excel(file.file, engine="openpyxl")
        # Detect columns that can be interpreted as dates
        date_columns = []

        for column in df.columns:

            # Skip numeric columns
            if pd.api.types.is_numeric_dtype(df[column]):
                continue

            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                dayfirst=True
            )

            non_empty_count = df[column].notna().sum()

            if non_empty_count > 0:
                valid_date_count = converted.notna().sum()

                # If at least 80% of the non-empty values in a column can be interpreted as dates, classify the column as a date column.
                # eg 100 values, 80-valid dates, 20-invalid dates 
                if valid_date_count / non_empty_count >= 0.8:
                    date_columns.append(column)

        # Create dataset profile contianing info about the dataset, The profile describes the dataset.
        profile={
            "row_count":len(df),
            "column_count":len(df.columns),
            "columns":df.columns.tolist(),   # tolist()->normal Python list.
            "data_types":{column:str(dtype) 
                          for column, dtype in df.dtypes.items()
                          },

            "missing_values":{
                column: int(count) for column, count in df.isnull().sum().items()
            },
            "duplicate_rows":int(df.duplicated().sum()),
            "numeric_summary":{
                column: {
                    "min": float(df[column].min()),
                    "max": float(df[column].max()),
                    "mean": float(df[column].mean()),
                    "sum": float(df[column].sum()),
                }
                for column in df.select_dtypes(include="number").columns
            },
            "categorical_columns":{
                column:{
                    "unique_count": int(df[column].nunique()),
                    "unique_values": df[column].dropna().unique().tolist(), #dropna() -> removes null values before considereing them as unique 
                    } for column in df.select_dtypes(include="object").columns
            },
            "date_columns": date_columns,

        }

        return {
            "message":"Dataset Profiled Successfully",
            "profile":profile,
        }


    except Exception as e: 
        raise HTTPException( 
            status_code=400, 
            detail=f"Unable to read Excel file: {str(e)}" )

    