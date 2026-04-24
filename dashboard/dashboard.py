import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')  

df = pd.read_csv("dashboard/main_data.csv")
df["date"] = pd.to_datetime(df["date"])  

st.title("Bike Sharing Dashboard")

st.sidebar.header("Filter Data")

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(df["date"].min(), df["date"].max()), 
    min_value=df["date"].min(),
    max_value=df["date"].max()
)

user_type = st.sidebar.selectbox(
    "Pilih Tipe Penyewa",
    ["All", "Casual", "Registered"]
)

filtered_df = df.copy()  

# filter berdasarkan tanggal
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["date"] <= pd.to_datetime(date_range[1]))
    ]

#  kolom target filter
if user_type == "Casual":
    target = "casual"
elif user_type == "Registered":
    target = "registered"
else:
    target = "total_rentals"

col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", int(filtered_df[target].sum()))  # total semua
col2.metric("Rata-rata per Hari", int(filtered_df.groupby("date")[target].sum().mean()))  # rata-rata harian
col3.metric("Max per Hari", int(filtered_df.groupby("date")[target].sum().max()))  # hari tertinggi

st.subheader("Pola Penyewaan per Jam")

hourly = filtered_df.groupby("hour")[target].mean().reset_index()  # rata-rata per jam
peak_hour = hourly.loc[hourly[target].idxmax(), "hour"]  # jam puncak

fig, ax = plt.subplots()
sns.lineplot(data=hourly, x="hour", y=target, marker="o", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

st.caption(f"Puncak penyewaan terjadi pada jam {int(peak_hour)}.")

st.subheader("Penyewaan per Musim")

daily_df = filtered_df.groupby("date")[target].sum().reset_index()  # total per hari
daily_df["season"] = filtered_df.groupby("date")["season"].first().values  # season per hari

season_daily = daily_df.groupby("season")[target].mean().reset_index()  # rata-rata per hari per season
lowest_season = season_daily.loc[season_daily[target].idxmin(), "season"]  # season terendah

fig, ax = plt.subplots()
sns.barplot(data=season_daily, x="season", y=target, ax=ax)
ax.set_ylabel("Rata-rata Penyewaan per Hari")
st.pyplot(fig)

st.caption(f"Musim dengan penyewaan terendah adalah {lowest_season}.")

st.subheader("Pengaruh Cuaca")

daily_df["weather_condition"] = filtered_df.groupby("date")["weather_condition"].first().values  #  cuaca per hari

weather_daily = daily_df.groupby("weather_condition")[target].mean().reset_index()  # rata-rata per hari per cuaca
worst_weather = weather_daily.loc[weather_daily[target].idxmin(), "weather_condition"]  # cuaca terendah

fig, ax = plt.subplots()
sns.barplot(data=weather_daily, x="weather_condition", y=target, ax=ax)
ax.set_ylabel("Rata-rata Penyewaan per Hari")
st.pyplot(fig)

st.caption(f"Penyewaan terendah terjadi pada kondisi cuaca: {worst_weather}.")

st.subheader("Insight Utama")

st.markdown("""
- Jam adalah faktor paling dominan. Pada pengguna registered, puncak penyewaan terjadi pada jam sibuk yaitu jam keberangkatan dan pulang bekerja. Sementara pada pengguna casual, penyewaan memuncak di siang hari.
- Cuaca memiliki pengaruh besar terhadap penyewaan sepeda.
- Musim mempengaruhi jumlah penyewaan dengan musim spring sebagai musim dengan penyewaan terendah.
""")