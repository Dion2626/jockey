import random
import streamlit as st
st.title("Jockey Boost")
st.write("This is a Monte Carlo simulation for betting odds. It calculates the expected value of different betting strategies based on the given odds.")

with st.form("form"):
    st.write("Enter the betting odds for back and lay bets:")
    bet365 = st.number_input("Bet365 Odds", value=1.65)
    required = st.number_input("Required Wins", value=2)
    trials = st.number_input("Trials", value=1000000)
    back_odds = {}
    lay_odds = {}
    col1, col2 = st.columns(2)
    with col1:
        st.write("Back Odds")
        for i in range(1, 12):
            back_odds[i] = st.number_input(f"Race {i}", value=0, key=f"back_{i}")
    with col2:
        st.write("Lay Odds")
        for i in range(1, 12):
            lay_odds[i] = st.number_input(f"Race {i}", value=0, key=f"lay_{i}")

    submitted = st.form_submit_button("Submit")

x = random.Random()

# bet365 = 1.65
# required = 2
# back_odds[1] = 6.8
# back_odds[2] = 3.05
# back_odds[3] = 2.86
# back_odds[4] = 2.42
# back_odds[5] = 8.4
# back_odds[6] = 3.41
# back_odds[7] = 2.18

# lay_odds[1] = 8.6
# lay_odds[2] = 3.59
# lay_odds[3] = 3.45
# lay_odds[4] = 3.7
# lay_odds[5] = 23
# lay_odds[6] = 8.4
# lay_odds[7] = 2.57

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
    for i in range(trials):
        wins = 0

        for j in range(1, len(prob) + 1):
            if not prob[j]:
                continue
            if x.random() < prob[j]:
                wins += 1
        if wins >= required:
            payouts += 1
            money += (bet365 - 1)
        else:
            money -= 1
    st.write(setting)
    st.write("Odds", str(round(trials / payouts, 4)))
    st.write("ev" , str(round(money / trials * 100, 2)), "%")
if submitted:
    calculate("Probability Midpoint")
    calculate("Odds Midpoint")
    calculate("Lay Odds")
