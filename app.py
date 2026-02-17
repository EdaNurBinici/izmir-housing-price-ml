"""
Izmir Housing Project - Streamlit Application
Senior-level refactored version
"""

import sys
from pathlib import Path

# src klasörünü path'e ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

# Import project modules
from src.config_loader import ConfigLoader
from src.data_processor import DataProcessor
from src.logger_setup import get_logger, setup_logging
from src.luxury_score import LuxuryScoreCalculator
from src.model_loader import ModelLoader
from src.predictor import PricePredictor
from src.validators import InputValidator

# Initialize logging
setup_logging(log_level="INFO", log_file="logs/app.log")
logger = get_logger(__name__)

# Load config
try:
    config = ConfigLoader("config/config.yaml")
except Exception as e:
    st.error(f"⚠️ Config file could not be loaded: {e}")
    st.stop()

# Streamlit page settings
st.set_page_config(
    page_title=config.get("streamlit.page_title", "Izmir Housing Project Presentation"),
    layout=config.get("streamlit.layout", "wide"),
    initial_sidebar_state=config.get("streamlit.sidebar_state", "expanded"),
)


# Model and data loading
@st.cache_resource
def initialize_app():
    """Initializes the application and loads necessary objects"""
    try:
        logger.info("Application starting...")

        # Model loader
        model_loader = ModelLoader(config)
        if not model_loader.load_all():
            return None

        # Luxury calculator
        luxury_calculator = LuxuryScoreCalculator(config)

        # Validator
        cleaning_config = config.get_cleaning_config()
        validator = InputValidator(
            price_min=cleaning_config.get("price_min", 100000),
            price_max=cleaning_config.get("price_max", 50000000),
            area_min=cleaning_config.get("area_min", 20),
            area_max=cleaning_config.get("area_max", 1000),
        )

        # Predictor
        predictor = PricePredictor(model_loader, luxury_calculator, validator)

        # Data processor
        data_processor = DataProcessor(config)

        logger.info("Application started successfully")

        return {
            "model_loader": model_loader,
            "predictor": predictor,
            "data_processor": data_processor,
            "config": config,
        }

    except Exception as e:
        logger.error(f"Application initialization error: {e}")
        return None


# Start the application
app_data = initialize_app()

if app_data is None:
    st.error("⚠️ Files are missing! Please run 'model_egitim.py'.")
    st.info("💡 Run this command in terminal: `python model_egitim.py`")
    st.stop()

model_loader = app_data["model_loader"]
predictor = app_data["predictor"]
data_processor = app_data["data_processor"]
config = app_data["config"]

# Sidebar menu
st.sidebar.title("📌 Project Presentation Menu")

menu = st.sidebar.radio(
    "Sections:",
    [
        "1. About the Project & Objective",
        "2. Data Preprocessing Process",
        "3. Advanced Data Analysis (EDA)",
        "4. Live Application (Demo)",
        "5. Model Performance",
        "6. Conclusion & Outcomes",
    ],
)

st.sidebar.divider()
project_info = config.get("project", {})
st.sidebar.caption(
    f"**Developer:** Eda Nur BİNİCİ\n\n**Course:** {project_info.get('course', 'Introduction to Artificial Intelligence')}"
)

# --- SECTION 1: ABOUT THE PROJECT ---
if menu == "1. About the Project & Objective":
    st.title(f"🏠 {project_info.get('name', 'Izmir Housing Project')}")
    st.image(
        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
        use_container_width=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Project Objective")
        st.write(
            """
        The main objective of this project is to develop an artificial intelligence-based system
        that predicts the market value of residential properties in Izmir based on their features
        (district, area, number of rooms, etc.) and analyzes the property's **'Luxury Status'**.
        """
        )
    with col2:
        st.subheader("🛠️ Technologies Used")
        st.markdown(
            """
        * **Python:** Main programming language
        * **Scikit-learn:** Machine learning (Gradient Boosting)
        * **Pandas & Seaborn:** Data analysis and visualization
        * **Streamlit:** Interactive web interface
        * **YAML:** Configuration management
        * **Logging:** Advanced logging system
        """
        )

    st.info(
        "💡 **Why Izmir?** It was selected as the most suitable city for model training in terms of data diversity and quality (6,000+ rows)."
    )

    with st.expander("📋 Project Structure"):
        st.code(
            """
Housing_Project/
├── src/              # Source code modules
├── config/           # Configuration files
├── tests/            # Test files
├── logs/             # Log files
├── app.py            # Streamlit application
├── model_egitim.py   # Model training script
└── requirements.txt  # Dependencies
        """
        )

# --- SECTION 2: DATA PREPROCESSING ---
elif menu == "2. Data Preprocessing Process":
    st.title("🛠️ Data Preprocessing and Cleaning")
    st.markdown(
        "For the success of the AI model, we didn't use raw data directly. We processed it through the following steps:"
    )

    with st.expander("Why and How We Did It?", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.info(
                """
            **✂️ Train-Test Split (80% / 20%)**
            * **Why?** The model can memorize the training data.
            * **Solution:** It must be tested with unseen data.
            * **Academic:** "Model performance was measured on test data separate from the training data."
            """
            )
            st.info(
                """
            **⚠️ Outlier Removal**
            * **Why?** Extremely expensive/cheap houses inflate RMSE and mislead the model.
            * **Academic:** "Outliers were removed as they reduce the model's generalization capability."
            """
            )
        with c2:
            st.success(
                """
            **📍 One-Hot Encoding**
            * **Why?** The model doesn't understand texts like "Çankaya", "Buca".
            * **Solution:** Districts were converted to 0-1 matrix. Label Encoding was not used because there's no mathematical superiority between districts.
            """
            )
            st.success(
                """
            **📏 StandardScaler**
            * **Why?** Price (Millions) and Room Count (3-5) are not on the same scale.
            * **Solution:** All were brought to standard scale, so the model distributed weights fairly.
            """
            )

    st.divider()

    st.subheader("1. Raw Data")
    df = model_loader.raw_df
    st.write(f"The initial state of the dataset consists of **{len(df)} rows** of data.")
    st.dataframe(df.head(3))

    st.divider()

    st.subheader("2. Outlier Removal")

    outlier_stats = data_processor.get_outlier_stats(df)

    col1, col2 = st.columns(2)
    with col1:
        st.error("📉 Removed Data")
        st.write(
            f"- Properties with price above {outlier_stats['price_max']:,} TL or below {outlier_stats['price_min']:,} TL."
        )
        st.write(
            f"- Properties with area above {outlier_stats['area_max']} m² or below {outlier_stats['area_min']} m²."
        )
        st.metric(
            "Cleaned Rows",
            f"{outlier_stats['atilan_satir']} Items",
            delta="-Noise",
            delta_color="inverse",
        )

    with col2:
        st.success("✅ Remaining Clean Data")
        st.write("Reliable dataset used in model training and visualizations.")
        st.metric("Training Data", f"{outlier_stats['kalan_satir']} Items", "Quality")

# --- SECTION 3: EDA ---
elif menu == "3. Advanced Data Analysis (EDA)":
    st.title("📊 Advanced Exploratory Data Analysis (EDA)")

    clean_df = data_processor.prepare_eda_data(model_loader.raw_df)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📉 Price Analysis", "📏 Area & Regression", "🏙️ District Analysis", "🔥 Correlation Matrix"]
    )

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1. Standard Price Distribution")
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.histplot(clean_df["price"], kde=True, color="blue", ax=ax1)
            plt.xlabel("Price (TL)")
            plt.ylabel("Frequency")
            st.pyplot(fig1)
            st.caption("Prices are right-skewed.")

        with col2:
            st.subheader("2. Logarithmic Price Distribution")
            fig_log, ax_log = plt.subplots(figsize=(10, 6))
            sns.histplot(np.log1p(clean_df["price"]), kde=True, color="purple", bins=30, ax=ax_log)
            plt.xlabel("Log(Price)")
            plt.ylabel("Frequency")
            st.pyplot(fig_log)
            st.info(
                "💡 **Analysis:** With logarithmic transformation, the data approaches Normal Distribution (Bell Curve)."
            )

    with tab2:
        st.subheader("3. Area - Price Relationship (Regression)")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.regplot(
            x="area",
            y="price",
            data=clean_df,
            scatter_kws={"alpha": 0.5, "color": "green"},
            line_kws={"color": "red"},
            ax=ax2,
        )
        plt.xlabel("Area (m²)")
        plt.ylabel("Price (TL)")
        plt.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig2)
        st.info(
            "💡 **Analysis:** The red line shows the general upward trend of price as area increases."
        )

    with tab3:
        st.subheader("4. District-Based Price Variability (Boxplot)")
        order = clean_df.groupby("district")["price"].median().sort_values(ascending=False).index
        fig_box, ax_box = plt.subplots(figsize=(14, 7))
        sns.boxplot(
            x="district", y="price", data=clean_df, order=order, palette="viridis", ax=ax_box
        )
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Price (TL)")
        st.pyplot(fig_box)

        st.divider()
        st.subheader("5. Most Valuable Districts per Square Meter")
        ilce_m2_deger = (
            clean_df.groupby("district")["m2_fiyat"].mean().sort_values(ascending=False).head(10)
        )
        st.bar_chart(ilce_m2_deger)

    with tab4:
        st.subheader("6. Correlation Matrix (Heatmap)")
        numeric_df = clean_df[["price", "area", "age", "toplam_oda", "m2_fiyat"]]
        numeric_df.columns = ["Price", "Area", "Building Age", "Room Count", "Price per m²"]

        fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            linewidths=1,
            linecolor="white",
            ax=ax_corr,
        )
        st.pyplot(fig_corr)

# --- SECTION 4: DEMO ---
elif menu == "4. Live Application (Demo)":
    st.title("🚀 Live Prediction Application")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            ilce = st.selectbox("📍 District", model_loader.ilce_listesi)
            ev_tipi = st.selectbox("🏠 Property Type", model_loader.ev_tipleri)
            m2 = st.number_input("📏 Net Area (m²)", 50, 1000, 120)
        with col2:
            oda = st.number_input("🚪 Number of Rooms", 1, 10, 3)
            salon = st.number_input("🛋️ Number of Living Rooms", 1, 5, 1)
            yas = st.number_input("🏗️ Building Age", 0, 100, 5)

        btn = st.button("✨ Calculate", type="primary")

    if btn:
        try:
            result = predictor.predict(
                ilce=ilce, ev_tipi=ev_tipi, m2=m2, oda=oda, salon=salon, yas=yas
            )

            st.divider()
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.subheader("💰 Estimated Value")
                st.success(f"# {result['tahmini_fiyat']:,} TL")
            with c2:
                st.subheader("💎 Luxury Score")
                st.metric(
                    label="Prestige Score",
                    value=f"{result['luxury_score']}/100",
                    delta=result["luxury_category"],
                )

            st.progress(result["luxury_score"] / 100)

            if result["luxury_score"] == 100:
                st.balloons()
                st.success("🏆 CONGRATULATIONS! The most prestigious property in the area.")

            # Show details
            with st.expander("📊 Detailed Analysis"):
                st.json(result["luxury_details"])

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            st.error(f"❌ Error: {e}")

# --- SECTION 5: PERFORMANCE ---
elif menu == "5. Model Performance":
    st.title("📈 Model Performance Analysis")

    with st.expander("🚀 WHY DID WE CHOOSE THIS MODEL AND TECHNIQUES?", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.warning(
                """
            **🔹 Gradient Boosting**
            * **Why?** Not just a simple regression line.
            * **Difference:** Learns complex relationships (District-Price balance, etc.).
            * **Result:** Model became 'smarter' and reduced errors.
            """
            )
        with col2:
            st.warning(
                """
            **🔹 Target Encoding (District Score)**
            * **What We Did?** We taught the district not just as 0-1, but as a "Value Score".
            * **Result:** The model mathematically understood that Çeşme is more valuable than Buca.
            """
            )
        with col3:
            st.warning(
                """
            **🔹 Logarithmic Transformation**
            * **Why?** There was a huge gap between Prices (Millions) and Room Count (3).
            * **Result:** By balancing prices, we prevented the model from drowning in large numbers.
            """
            )

    st.divider()

    metrikler = model_loader.metrikler
    r2_degeri = metrikler.get("R2 Skoru", 0)

    if r2_degeri > 0.85:
        yorum = "Excellent 🌟"
        renk = "normal"
    elif r2_degeri > 0.65:
        yorum = "Very Good ✅"
        renk = "normal"
    elif r2_degeri > 0.50:
        yorum = "Acceptable (Medium) ⚠️"
        renk = "off"
    else:
        yorum = "Needs Improvement 🔻"
        renk = "inverse"

    c1, c2, c3 = st.columns(3)
    c1.metric("R² Score (Accuracy)", f"{r2_degeri:.3f}", yorum, delta_color=renk)
    c2.metric(
        "MAE (Error)", f"{int(metrikler.get('MAE (Ortalama Hata)', 0)):,} TL", delta_color="inverse"
    )
    c3.metric(
        "RMSE", f"{int(metrikler.get('RMSE (Kök Ortalama Hata)', 0)):,} TL", delta_color="inverse"
    )

    st.divider()

    if r2_degeri < 0.65:
        st.warning(
            """
        **💡 Analysis Note:** The current level of R² Score shows the **"Human Factor"** in the real estate market.
        Features not in the dataset such as view, interior structure, urgent sale status affect the price.
        """
        )

    st.subheader("🧠 Model's Decision Mechanism")

    try:
        grafik_verisi = model_loader.onem_duzeyleri.copy()

        def isim_duzelt(metin: str) -> str:
            """Corrects feature names"""
            if "district_" in metin:
                return metin.replace("district_", "") + " District"
            elif "left_" in metin:
                return metin.replace("left_", "") + " (Property Type)"
            elif metin == "area":
                return "Area (m²)"
            elif metin == "age":
                return "Building Age"
            elif metin == "toplam_oda":
                return "Room Count"
            elif metin == "ilce_skoru":
                return "District Value"
            return metin

        if "Özellik" in grafik_verisi.columns:
            grafik_verisi["Özellik"] = grafik_verisi["Özellik"].apply(isim_duzelt)
            st.bar_chart(grafik_verisi.set_index("Özellik"))
        else:
            st.write("Feature importance chart is not available.")
    except Exception as e:
        logger.warning(f"Chart creation error: {e}")
        st.write("Due to model complexity, the feature importance chart cannot be displayed in this model.")

# --- SECTION 6: CONCLUSION ---
elif menu == "6. Conclusion & Outcomes":
    st.title("🏁 Project Evaluation and Conclusion")
    st.info(
        """
    ### 📝 Project Outputs
    In this project developed within the scope of the Introduction to Artificial Intelligence course, I had the opportunity to put my theoretical knowledge into practice. My main achievements:

    1. **Data Analysis:** Izmir real estate data was cleaned and analyzed.
    2. **High Accuracy:** Successful predictions were obtained with advanced algorithms.
    3. **Original Added Value:** A different dimension was added to the project with the "Luxury Score" algorithm.
    4. **User Experience:** The project was transformed into a web application that appeals to end users.
    5. **Code Quality:** Modular structure, logging and error handling were used.
    """
    )
    st.write("---")
    st.success("My project presentation ends here. Thank you for listening! 👏")
    if st.button("Celebrate 🎉"):
        st.balloons()
