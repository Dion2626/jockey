import random
import streamlit as st
st.title("Jockey Boost")
st.write("This is a Monte Carlo simulation for betting odds. It calculates the expected value of different betting strategies based on the given odds. Made by @shiina4904.")

with st.form("form"):
    st.write("Enter the betting odds for back and lay bets:")
    bet365 = st.number_input("Bet365 Odds", value=2.00, format="%.2f")
    required = st.number_input("Required Wins", value=1)
    trials = st.number_input("Trials", value=1000000)
    back_odds = {}
    lay_odds = {}
    col1, col2 = st.columns(2)
    for i in range(1, 13):
        col1, col2 = st.columns(2)
        with col1:
            if i == 1:
                st.write("Back Odds")
            back_odds[i] = st.number_input(f"Race {i}", value=0.00, key=f"back_{i}", format="%.2f")
        with col2:
            if i == 1:
                st.write("Lay Odds")
            lay_odds[i] = st.number_input(f"Race {i}", value=0.00, key=f"lay_{i}", format="%.2f")



    submitted = st.form_submit_button("Submit")

x = random.Random()

def calculate(setting):
    money = 0
    prob = {}
    for i in range(1, len(back_odds) + 1):
        if back_odds[i] == 0 or lay_odds[i] == 0:
            continue
        if setting == "Probability Midpoint":
            prob[i] = (1 / back_odds[i] + 1 / lay_odds[i]) / 2
        elif setting == "Odds Midpoint":
            prob[i] = 1 / ((back_odds[i] + lay_odds[i]) / 2)
        elif setting == "Lay Odds":
            prob[i] = 1 / lay_odds[i]

    payouts = 0
    if len(prob) < required:
        st.write("Please try harder. You need at least ", str(required), " races for the jockey boost to be possible.")
        return
    for i in range(trials):
        wins = 0

        for j in prob.values():
            if x.random() < j:
                wins += 1
        if wins >= required:
            payouts += 1
            money += (bet365 - 1)
        else:
            money -= 1
    explanation = ""
    if setting == "Probability Midpoint":
        explanation = "This is the average of the back and lay probabilities. More aggressive than odds midpoint."
    elif setting == "Odds Midpoint":
        explanation = "This is the average of the back and lay odds. More conservative than probability midpoint."
    elif setting == "Lay Odds":
        explanation = "This is the lay odds. This is the most conservative strategy."
    st.markdown(f"**{setting}**", help=explanation)
    true = round(trials / payouts, 4)
    p = 1 / true
    q = 1 - p
    b = bet365 - 1
    st.write("Odds", str(true))
    st.write("ev" , str(round(money / trials * 100, 2)), "%")
    st.write("Kelly", str(round((p * b - q) / b * 100, 2)), "%")
if submitted:
    col1, col2, col3 = st.columns(3)
    with col1:
        calculate("Probability Midpoint")
    with col2:
        calculate("Odds Midpoint")
    with col3:
        calculate("Lay Odds")
st.info("Made by @shiina4904.")
