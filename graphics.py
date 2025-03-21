import pandas as pd
import plotly.express as px


# Данные для DataFrame (получили из файла calculations.py)
data = {
    "Район": [
        "Пушкино", "Ногинск", "Подольск", "Балашиха", "Серпухов", "Долгопрудный",
        "Лобня", "Реутов", "Красногорск", "Старая_Купавна", "Видное",
        "Сергиев_Посад", "Мытищи", "Химки", "Люберцы"
    ],
    "Цена": [
        15600.0, 15600.0, 12294.5, 12600.0, 16500.0, 26415.5,
        15500.0, 16000.0, 15000.0, 10200.0, 15800.0,
        9910.0, 14635.0, 13200.0, 14572.0
    ],
    "Расстояние": [
        32.83, 52.13, 36.09, 20.45, 93.86, 21.50,
        30.29, 14.89, 19.20, 35.77, 23.01,
        68.87, 19.71, 18.71, 18.98
    ],
    "Долгота": [
        37.860000, 38.433330, 37.544440, 37.933330, 37.400000, 37.500000,
        37.474440, 37.855194, 37.333330, 38.183330, 37.700000,
        38.133330, 37.733330, 37.448000, 37.893890
    ],
    "Широта": [
        56.016670, 55.860000, 55.429720, 55.800000, 54.916670, 55.933330,
        56.011940, 55.766611, 55.816670, 55.800000, 55.550000,
        56.300000, 55.916670, 55.889170, 55.681390
    ]
}


df = pd.DataFrame(data)

df.set_index("Район", inplace=True)
df.reset_index(inplace=True)

fig = px.scatter_map(  # по медианной цене
    df,
    lat="Широта",
    lon="Долгота",
    hover_name="Район",
    size="Цена",
    color="Цена",
    color_continuous_scale=px.colors.sequential.Viridis,
    size_max=20,
    zoom=8,  #
    title="Карта Москвы (цены)"
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
)

fig.show()

fig = px.scatter_map(  # по расстоянию
    df,
    lat="Широта",
    lon="Долгота",
    hover_name="Район",
    size="Расстояние",
    color="Расстояние",
    color_continuous_scale=px.colors.sequential.Viridis,
    size_max=20,
    zoom=8,  #
    title="Карта Москвы (расстояния)"
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
)

fig.show()



# сделаем предположение о том что средняя цена за километр доставки 10 рублей, а размер склада 50 квадратных метров, 200 заказов в месяц
# Расчет общей цены на логистику
df["Логистика"] = (df["Расстояние"] * 10 * 200) + (50 * df["Цена"])

# Создание карты с помощью plotly.express
fig = px.scatter_map(
    df,
    lat="Широта",
    lon="Долгота",
    hover_name="Район",
    size="Логистика",
    color="Логистика",
    color_continuous_scale=px.colors.sequential.Viridis,
    size_max=20,
    zoom=8,
    title="Карта Москвы (логистика)"
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
)

fig.show()

min_logistics_index = df["Логистика"].idxmin()
min_logistics_row = df.loc[min_logistics_index]
print("Район с минимальной ценой за логистику в месяц:")
print(min_logistics_row)



