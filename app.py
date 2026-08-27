import os
import joblib
import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MPLAD AI Risk Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛡️ AI Risk Analyzer")

    st.caption(
        "MPLAD AI-powered anomaly detection system"
    )

    st.divider()

    st.markdown("### 🔎 How it works")

    st.markdown(
        """
        **1. 📂 Upload Dataset**  
        Upload your MPLAD Excel or CSV file.

        **2. 🤖 AI Screening**  
        Machine learning checks records for unusual patterns.

        **3. 📊 Risk Scoring**  
        Each record receives a risk score from **0–100**.

        **4. 🚨 Review**  
        High-risk records are highlighted for further inspection.
        """
    )

    st.divider()

    st.warning(
        "An anomaly indicates a statistically unusual "
        "pattern and does not by itself prove fraud."
    )

# ============================================================
# MAIN HEADER
# ============================================================

st.title("🛡️ MPLAD AI Risk Analyzer")

st.subheader(
    "AI-powered anomaly detection & risk analytics "
    "for MPLAD allocation records"
)

st.caption(
    "MACHINE LEARNING  •  ANOMALY DETECTION  •  RISK ANALYTICS"
)

st.divider()

# ============================================================
# UPLOAD DATASET
# ============================================================

st.header("📂 Upload Dataset")

st.write(
    "Upload your MPLAD Excel or CSV dataset for AI-based risk analysis."
)

uploaded_file = st.file_uploader(
    "Choose an Excel or CSV file",
    type=["xlsx", "xls", "csv"],
    help="Supported formats: XLSX, XLS and CSV"
)

# ============================================================
# PROCESS DATASET
# ============================================================

if uploaded_file is not None:

    st.success(
        f"✅ Dataset uploaded successfully: {uploaded_file.name}"
    )

    try:

        # ========================================================
        # READ FILE
        # ========================================================

        if uploaded_file.name.lower().endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        else:

            df = pd.read_excel(
                uploaded_file,
                engine="calamine",
                header=1
            )

        # ========================================================
        # REMOVE UNNAMED COLUMNS
        # ========================================================

        df = df.loc[
            :,
            ~df.columns.astype(str).str.startswith("Unnamed")
        ].copy()

        # ========================================================
        # CLEAN COLUMN NAMES
        # ========================================================

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # ========================================================
        # REMOVE GRAND TOTAL ROW
        # ========================================================

        if "Sr. No." in df.columns:

            df = df[
                df["Sr. No."]
                .astype(str)
                .str.strip()
                .str.lower()
                != "grand total"
            ].copy()

        # ========================================================
        # RESET INDEX
        # ========================================================

        df.reset_index(
            drop=True,
            inplace=True
        )

        # ========================================================
        # REQUIRED COLUMN CHECK
        # ========================================================

        required_columns = [
            "State",
            "Hon'ble Members of Parliament",
            "Elected/Nominated"
        ]

        missing_columns = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:

            st.error(
                "❌ Required columns are missing from the uploaded dataset."
            )

            st.write(
                "Missing columns:",
                missing_columns
            )

            st.write(
                "Available columns:",
                list(df.columns)
            )

            st.stop()

        # ========================================================
        # FIND ALLOCATED AMOUNT COLUMN
        # ========================================================

        amount_columns = [
            col
            for col in df.columns
            if (
                "allocated" in str(col).lower()
                and "amount" in str(col).lower()
            )
        ]

        if not amount_columns:

            st.error(
                "❌ Allocated Amount column could not be found."
            )

            st.write(
                "Available columns:",
                list(df.columns)
            )

            st.stop()

        amount_col = amount_columns[0]

        # ========================================================
        # CLEAN TEXT COLUMNS
        # ========================================================

        df["State"] = (
            df["State"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df["Hon'ble Members of Parliament"] = (
            df["Hon'ble Members of Parliament"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df["Elected/Nominated"] = (
            df["Elected/Nominated"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # ========================================================
        # CLEAN ALLOCATED AMOUNT
        # ========================================================

        df[amount_col] = (
            df[amount_col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace("Rs.", "", regex=False)
            .str.strip()
        )

        df[amount_col] = pd.to_numeric(
            df[amount_col],
            errors="coerce"
        )

        # ========================================================
        # EXTRACT MP TERM YEARS
        # ========================================================

        mp_col = "Hon'ble Members of Parliament"

        term_data = df[mp_col].str.extract(
            r"\((\d{4})-(\d{2,4})\)"
        )

        df["Term_Start_Year"] = pd.to_numeric(
            term_data[0],
            errors="coerce"
        )

        end_values = term_data[1].astype(str)

        # Handle formats like 2019-24 and 2019-2024
        df["Term_End_Year"] = end_values.apply(
            lambda x: (
                int("20" + x)
                if x.isdigit() and len(x) == 2
                else (
                    int(x)
                    if x.isdigit() and len(x) == 4
                    else None
                )
            )
        )

        df["Term_End_Year"] = pd.to_numeric(
            df["Term_End_Year"],
            errors="coerce"
        )

        # ========================================================
        # HANDLE MISSING NUMERIC VALUES
        # ========================================================

        if df[amount_col].notna().any():

            df[amount_col] = df[amount_col].fillna(
                df[amount_col].median()
            )

        else:

            df[amount_col] = df[amount_col].fillna(0)

        if df["Term_Start_Year"].notna().any():

            df["Term_Start_Year"] = (
                df["Term_Start_Year"]
                .fillna(
                    df["Term_Start_Year"].median()
                )
            )

        else:

            df["Term_Start_Year"] = 0

        if df["Term_End_Year"].notna().any():

            df["Term_End_Year"] = (
                df["Term_End_Year"]
                .fillna(
                    df["Term_End_Year"].median()
                )
            )

        else:

            df["Term_End_Year"] = 0

        # ========================================================
        # DATASET OVERVIEW
        # ========================================================

        st.divider()

        st.header("📋 Dataset Overview")

        overview_col1, overview_col2, overview_col3 = st.columns(3)

        with overview_col1:
            st.metric(
                "Total Records",
                len(df)
            )

        with overview_col2:
            st.metric(
                "Total Columns",
                len(df.columns)
            )

        with overview_col3:
            st.metric(
                "Allocated Amount",
                f"₹{df[amount_col].sum():,.0f}"
            )

        # ========================================================
        # DATASET PREVIEW
        # ========================================================

        with st.expander("👁️ View Dataset Preview", expanded=False):

            st.dataframe(
                df.head(10),
                use_container_width=True,
                hide_index=True
            )

        # ========================================================
        # MODEL FILES
        # ========================================================

        model_file = "mplad_anomaly_model.pkl"
        scaler_file = "mplad_scaler.pkl"
        features_file = "mplad_model_features.pkl"

        # ========================================================
        # CHECK MODEL
        # ========================================================

        if not os.path.exists(model_file):

            st.error(
                f"❌ Model file not found: {model_file}"
            )

            st.info(
                "Keep the model .pkl files in the same folder as app.py."
            )

            st.stop()

        if not os.path.exists(scaler_file):

            st.error(
                f"❌ Scaler file not found: {scaler_file}"
            )

            st.stop()

        # ========================================================
        # LOAD MODEL
        # ========================================================

        with st.spinner("🤖 Running AI risk analysis..."):

            model = joblib.load(
                model_file
            )

            scaler = joblib.load(
                scaler_file
            )

            # ====================================================
            # LOAD FEATURE NAMES
            # ====================================================

            feature_names = None

            if os.path.exists(features_file):

                feature_names = joblib.load(
                    features_file
                )

                if hasattr(
                    feature_names,
                    "tolist"
                ):

                    feature_names = (
                        feature_names.tolist()
                    )

                feature_names = list(
                    feature_names
                )

            # ====================================================
            # CREATE MODEL INPUT
            # ====================================================

            categorical_cols = [
                "State",
                "Elected/Nominated"
            ]

            numerical_cols = [
                amount_col,
                "Term_Start_Year",
                "Term_End_Year"
            ]

            model_input = df[
                categorical_cols +
                numerical_cols
            ].copy()

            # ====================================================
            # ONE-HOT ENCODING
            # ====================================================

            X = pd.get_dummies(
                model_input,
                columns=categorical_cols,
                drop_first=False
            )

            # ====================================================
            # ALIGN FEATURES
            # ====================================================

            if feature_names is not None:

                X = X.reindex(
                    columns=feature_names,
                    fill_value=0
                )

            # ====================================================
            # NUMERIC DATA
            # ====================================================

            X = X.apply(
                pd.to_numeric,
                errors="coerce"
            )

            X = X.fillna(0)

            # ====================================================
            # SCALE
            # ====================================================

            X_scaled = scaler.transform(
                X
            )

            # ====================================================
            # PREDICTION
            # ====================================================

            prediction = model.predict(
                X_scaled
            )

            # ====================================================
            # ANOMALY SCORE
            # ====================================================

            if hasattr(
                model,
                "decision_function"
            ):

                scores = model.decision_function(
                    X_scaled
                )

            else:

                scores = None

            # ====================================================
            # RESULT DATAFRAME
            # ====================================================

            result_df = df.copy()

            result_df["AI_Anomaly"] = prediction

            if scores is not None:

                result_df["Anomaly_Score"] = scores

            # ====================================================
            # RISK STATUS
            # ====================================================

            result_df["Risk_Status"] = (
                result_df["AI_Anomaly"]
                .apply(
                    lambda x:
                    "HIGH RISK / ANOMALY"
                    if x == -1
                    else "NORMAL"
                )
            )

            # ====================================================
            # RISK SCORE 0-100
            # ====================================================

            if scores is not None:

                min_score = scores.min()
                max_score = scores.max()

                if max_score != min_score:

                    result_df["Risk_Score"] = (
                        (max_score - scores)
                        /
                        (max_score - min_score)
                    ) * 100

                else:

                    result_df["Risk_Score"] = 0

            else:

                result_df["Risk_Score"] = 0

            # ====================================================
            # RISK LEVEL
            # ====================================================

            def risk_level(score):

                if score >= 70:
                    return "High Risk"

                elif score >= 40:
                    return "Medium Risk"

                else:
                    return "Low Risk"

            result_df["Risk_Level"] = (
                result_df["Risk_Score"]
                .apply(risk_level)
            )

        # ========================================================
        # SUMMARY
        # ========================================================

        anomaly_count = int(
            (prediction == -1).sum()
        )

        normal_count = int(
            (prediction == 1).sum()
        )

        total_count = len(
            result_df
        )

        if total_count > 0:

            anomaly_percentage = (
                anomaly_count /
                total_count
            ) * 100

        else:

            anomaly_percentage = 0

        # ========================================================
        # AI SCREENING RESULT
        # ========================================================

        st.divider()

        st.header("🤖 AI Screening Results")

        if anomaly_percentage > 0:

            st.warning(
                f"⚠️ {anomaly_percentage:.2f}% of records "
                "were flagged as statistically unusual "
                "by the anomaly detection model."
            )

        else:

            st.success(
                "✅ No statistically unusual records were detected."
            )

        # ========================================================
        # DASHBOARD METRICS
        # ========================================================

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:

            st.metric(
                "📄 Total Records",
                total_count
            )

        with metric2:

            st.metric(
                "✅ Normal Records",
                normal_count
            )

        with metric3:

            st.metric(
                "🚨 Anomalies",
                anomaly_count
            )

        with metric4:

            st.metric(
                "📈 Anomaly %",
                f"{anomaly_percentage:.2f}%"
            )

        # ========================================================
        # RISK DISTRIBUTION
        # ========================================================

        st.divider()

        st.header("📊 Risk Distribution")

        risk_order = [
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ]

        risk_counts = (
            result_df["Risk_Level"]
            .value_counts()
            .reindex(
                risk_order,
                fill_value=0
            )
        )

        chart_col, info_col = st.columns(
            [2, 1]
        )

        with chart_col:

            st.bar_chart(
                risk_counts,
                use_container_width=True
            )

        with info_col:

            st.subheader(
                "🎯 Risk Classification"
            )

            st.success(
                "🟢 LOW RISK\n\n"
                "Risk score below 40"
            )

            st.warning(
                "🟡 MEDIUM RISK\n\n"
                "Risk score 40–69"
            )

            st.error(
                "🔴 HIGH RISK\n\n"
                "Risk score 70+"
            )

        # ========================================================
        # HIGH RISK RECORDS
        # ========================================================

        st.divider()

        st.header("🚨 High-Risk Records")

        high_risk = (
            result_df[
                result_df["Risk_Level"]
                == "High Risk"
            ]
            .sort_values(
                "Risk_Score",
                ascending=False
            )
        )

        display_columns = [
            col
            for col in [
                "Sr. No.",
                "State",
                "Hon'ble Members of Parliament",
                "Elected/Nominated",
                amount_col,
                "Risk_Score",
                "Risk_Level"
            ]
            if col in high_risk.columns
        ]

        if len(high_risk) > 0:

            st.error(
                f"🚨 {len(high_risk)} high-risk records detected."
            )

            high_risk_display = high_risk[
                display_columns
            ].copy()

            if "Risk_Score" in high_risk_display.columns:

                high_risk_display["Risk_Score"] = (
                    high_risk_display["Risk_Score"]
                    .round(2)
                )

            st.dataframe(
                high_risk_display,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No high-risk records detected."
            )

        # ========================================================
        # COMPLETE ANALYSIS
        # ========================================================

        st.divider()

        st.header("📑 Complete Analysis Results")

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )

        # ========================================================
        # EXPORT ANALYSIS
        # ========================================================

        st.divider()

        st.header("📥 Export Analysis")

        csv_data = result_df.to_csv(
            index=False
        )

        st.download_button(
            label="⬇️ Download AI Analysis CSV",
            data=csv_data,
            file_name="MPLAD_AI_Risk_Analysis.csv",
            mime="text/csv",
            use_container_width=True
        )

        # ========================================================
        # FOOTER
        # ========================================================

        st.divider()

        st.caption(
            "🛡️ MPLAD AI Risk Analyzer | "
            "Machine Learning • Anomaly Detection • Risk Analytics"
        )

    # ============================================================
    # ERROR HANDLING
    # ============================================================

    except Exception as e:

        st.error(
            "❌ Analysis failed."
        )

        with st.expander(
            "🔧 View technical error"
        ):

            st.exception(e)

else:

    # ============================================================
    # BEFORE FILE UPLOAD
    # ============================================================

    st.info(
        "👆 Upload your MPLAD Excel or CSV dataset above "
        "to start the AI risk analysis."
    )

    st.divider()

    st.markdown(
        """
        ### 🔐 What this application does

        **📂 Dataset Upload**  
        Accepts MPLAD Excel and CSV records.

        **🤖 AI Anomaly Detection**  
        Uses the trained machine-learning model to identify
        statistically unusual records.

        **📊 Risk Scoring**  
        Converts anomaly results into a 0–100 risk score.

        **🚨 High-Risk Detection**  
        Highlights records requiring further review.

        ** Analysis Export**  
        Allows the complete AI analysis to be downloaded as CSV.
        """
    )