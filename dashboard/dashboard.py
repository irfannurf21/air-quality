import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("main_data.csv")

# Pastikan format datetime benar
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



# Streamlit UI: Pilih lokasi
selected_location = st.selectbox("Pilih Lokasi:", ["All"] + list(df["location"].unique()))

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
sns.barplot(x="season", y="PM2.5", data=seasonal_pm25, ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("PM2.5")
ax.set_title("Rata-rata PM2.5 per Musim")
st.pyplot(fig)

# Heatmap Korelasi PM2.5 dengan Faktor Cuaca
st.subheader("Korelasi PM2.5 dengan Faktor Cuaca ")
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