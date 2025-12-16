import streamlit as st
from abc import ABC, abstractmethod

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "България → Италия": ["София", "Скопие", "Тирана", "Рим"],
}

city_info = {
    "София": {"food": 20, "sight": "Катедралата Александър Невски"},
    "Белград": {"food": 22, "sight": "Калемегдан"},
    "Виена": {"food": 30, "sight": "Дворецът Шьонбрун"},
    "Мюнхен": {"food": 28, "sight": "Мариенплац"},
    "Скопие": {"food": 18, "sight": "Каменният мост"},
    "Тирана": {"food": 19, "sight": "Площад Скандербег"},
    "Рим": {"food": 35, "sight": "Колизеумът"},
}

hotel_categories = {
    "💸 Евтин": 50,
    "🏨 Стандартен": 80,
    "🌟 Луксозен": 120
}

DISTANCE_BETWEEN_CITIES = 300  # км

# ================== OOP ==================

class Transport(ABC):
    def __init__(self, price_per_km):
        self.price_per_km = price_per_km

    @abstractmethod
    def name(self):
        pass

    def travel_cost(self, distance, passengers):
        return distance * self.price_per_km * passengers


class Car(Transport):
    def __init__(self):
        super().__init__(0.25)

    def name(self):
        return "🚗 Кола"


class Train(Transport):
    def __init__(self):
        super().__init__(0.18)

    def name(self):
        return "🚆 Влак"


class Plane(Transport):
    def __init__(self):
        super().__init__(0.45)

    def name(self):
        return "✈️ Самолет"

# ================== STREAMLIT UI ==================

st.set_page_config(page_title="Туристически планер", page_icon="🌍")
st.title("🌍 Интерактивен туристически планер")

route_choice = st.selectbox("🗺️ Маршрут:", list(routes.keys()))
transport_choice = st.selectbox("🚦 Превоз:", ["Кола", "Влак", "Самолет"])
hotel_choice = st.selectbox("🏨 Категория хотел:", list(hotel_categories.keys()))

days = st.slider("📅 Брой дни:", 2, 14, 6)
passengers = st.number_input("👥 Брой пътници:", 1, 10, 2)
budget = st.number_input("💰 Твоят бюджет (лв):", 500, 20000, 3000)

if st.button("Планирай пътуването 🧭"):
    cities = routes[route_choice]

    transport = {
        "Кола": Car(),
        "Влак": Train(),
        "Самолет": Plane()
    }[transport_choice]

    days_per_city = max(1, days // len(cities))

    st.subheader("🗺️ Маршрут")
    st.write(" ➡️ ".join(cities))

    total_food = 0
    total_hotels = 0

    st.subheader("🏙️ Градове")

    for city in cities:
        food_cost = city_info[city]["food"] * days_per_city * passengers
        hotel_cost = hotel_categories[hotel_choice] * days_per_city * passengers

        total_food += food_cost
        total_hotels += hotel_cost

        st.markdown(f"### 📍 {city}")
        st.write(f"🍽️ Храна: {food_cost:.2f} лв")
        st.write(f"🏨 Хотел: {hotel_cost:.2f} лв")
        st.write(f"🏛️ Забележителност: {city_info[city]['sight']}")

    distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(distance, passengers)

    total_cost = total_food + total_hotels + transport_cost

    st.subheader("💰 Разходи")
    st.write(f"{transport.name()} – {transport_cost:.2f} лв")
    st.write(f"🍽️ Храна – {total_food:.2f} лв")
    st.write(f"🏨 Хотели – {total_hotels:.2f} лв")

    st.bar_chart({
        "Транспорт": transport_cost,
        "Храна": total_food,
        "Хотели": total_hotels
    })

    st.markdown("---")
    st.write(f"## 💵 Общо: **{total_cost:.2f} лв**")

    if total_cost <= budget:
        st.success("✅ Бюджетът е достатъчен!")
    else:
        st.error("❌ Бюджетът не достига.")
