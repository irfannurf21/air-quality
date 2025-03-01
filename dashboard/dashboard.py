import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Menentukan path file CSV secara dinamis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "main_data.csv")

try:
    df = pd.read_csv(data_path)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Fungsi menentukan musim
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

df["season"] = df["month"].apply(get_season)

# Definisi kategori kualitas udara berdasarkan PM2.5
bins = [0, 50, 100, 150, 200, 300, float('inf')]
labels = ["Baik", "Sedang", "Tidak Sehat (Sensitif)", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"]
df["PM2.5_Category"] = pd.cut(df["PM2.5"], bins=bins, labels=labels, include_lowest=True)

# Streamlit UI: Pilih lokasi
df_locations = ["All"] + list(df["location"].unique())
selected_location = st.selectbox("Pilih Lokasi:", df_locations)

# Filter dataset berdasarkan lokasi
if selected_location != "All":
    filtered_df = df[df["location"] == selected_location]
else:
    filtered_df = df  # Gunakan semua data jika "All" dipilih

# Hitung rata-rata PM2.5 per musim setelah filtering
seasonal_pm25 = filtered_df.groupby("season")["PM2.5"].mean().reset_index()

# Plot rata-rata PM2.5 per musim
st.subheader(f"Rata-rata PM2.5 per Musim ({selected_location})")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y="PM2.5", data=seasonal_pm25, ax=ax, palette="coolwarm")
ax.set_xlabel("Musim")
ax.set_ylabel("PM2.5")
ax.set_title("Rata-rata PM2.5 per Musim")
st.pyplot(fig)

# Visualisasi distribusi kategori PM2.5
st.subheader(f"Distribusi Kategori PM2.5 ({selected_location})")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(y=filtered_df["PM2.5_Category"], order=labels, palette="coolwarm", ax=ax)
ax.set_xlabel("Jumlah Data")
ax.set_ylabel("Kategori PM2.5")
st.pyplot(fig)

# Heatmap Korelasi PM2.5 dengan Faktor Cuaca
st.subheader("Korelasi PM2.5 dengan Faktor Cuaca")
weather_corr = filtered_df[["PM2.5", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]].corr()
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(weather_corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.subheader("Visualisasi hubungan antara faktor cuaca dengan tingkat polusi udara (PM2.5)")

# Buat scatter plot dalam satu row
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.scatterplot(data=filtered_df, x="TEMP", y="PM2.5", alpha=0.3, ax=axes[0])
axes[0].set_title("Suhu vs PM2.5")
axes[0].set_xlabel("Suhu (°C)")
axes[0].set_ylabel("PM2.5")

sns.scatterplot(data=filtered_df, x="WSPM", y="PM2.5", alpha=0.3, ax=axes[1])
axes[1].set_title("Kecepatan Angin vs PM2.5")
axes[1].set_xlabel("Kecepatan Angin (m/s)")
axes[1].set_ylabel("PM2.5")

sns.scatterplot(data=filtered_df, x="DEWP", y="PM2.5", alpha=0.3, ax=axes[2])
axes[2].set_title("Dew Point vs PM2.5")
axes[2].set_xlabel("Dew Point (°C)")
axes[2].set_ylabel("PM2.5")

plt.tight_layout()
st.pyplot(fig)
