import streamlit as st
import itertools
import math

st.title("To Ley from Dion")

with st.form("form"):
    st.write("Enter the betting odds for back and lay bets:")
    bet365 = st.number_input("Bet365 Odds", value=2.00, format="%.2f")
    required = st.number_input("Required Wins", value=1)
    trials = st.number_input("Trials", value=1000000)
    
    back_odds = {}
    lay_odds = {}
    
    # Create 5 races
    for race_num in range(1, 6):
        st.subheader(f"Race {race_num}")
        
        # Create 15 back/lay odds inputs for each race
        for i in range(1, 16):
            col1, col2 = st.columns(2)
            with col1:
                if i == 1:
                    st.write("Back Odds")
                back_odds[f"race_{race_num}_horse_{i}"] = st.number_input(
                    f"Horse {i}", 
                    value=0.00, 
                    key=f"back_{race_num}_{i}", 
                    format="%.2f"
                )
            with col2:
                if i == 1:
                    st.write("Lay Odds")
                lay_odds[f"race_{race_num}_horse_{i}"] = st.number_input(
                    f"Horse {i}", 
                    value=0.00, 
                    key=f"lay_{race_num}_{i}", 
                    format="%.2f"
                )
        
        # Add a separator between races
        st.markdown("---")

    submitted = st.form_submit_button("Submit")

if submitted:
    # Create two columns for results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Using Lay Odds")
        # Get valid horses for each race (those with non-zero lay odds)
        valid_horses_lay = {}
        for race_num in range(1, 6):
            valid_horses_lay[race_num] = []
            for i in range(1, 16):
                key = f"race_{race_num}_horse_{i}"
                if lay_odds[key] > 0:
                    valid_horses_lay[race_num].append((i, lay_odds[key]))

        # Find all possible combinations using lay odds
        good_combinations_lay = []
        total_combinations_lay = 0
        
        # Generate all possible combinations
        for combo in itertools.product(*[valid_horses_lay[race] for race in range(1, 6)]):
            total_combinations_lay += 1
            # Calculate true odds for this combination
            true_odds = 1.0
            for horse_num, lay_odd in combo:
                true_odds *= lay_odd
            
            if true_odds < 2500:
                good_combinations_lay.append(combo)
        
        # Calculate probability of at least one good combination winning (lay odds)
        if good_combinations_lay:
            combo_probabilities_lay = []
            for combo in good_combinations_lay:
                prob = 1.0
                for horse_num, lay_odd in combo:
                    prob *= (1/lay_odd)
                combo_probabilities_lay.append(prob)
            
            prob_none_lay = 1.0
            for prob in combo_probabilities_lay:
                prob_none_lay *= (1 - prob)
            prob_at_least_one_lay = 1 - prob_none_lay
            
            # Display lay odds results
            st.write(f"Total combinations analyzed: {total_combinations_lay}")
            st.write(f"Number of combinations with true odds < $2500: {len(good_combinations_lay)}")
            st.write(f"Probability of at least one good combination winning: {prob_at_least_one_lay:.4%}")
            
            # Display the good combinations
            st.write("\nGood Combinations (true odds < $2500):")
            for combo in good_combinations_lay:
                combo_str = " + ".join([f"Race {race+1} Horse {horse} ({odds:.2f})" 
                                      for race, (horse, odds) in enumerate(combo)])
                true_odds = math.prod(odds for _, odds in combo)
                st.write(f"{combo_str} = {true_odds:.2f}")
        else:
            st.write("No combinations found with true odds < $2500")

    with col2:
        st.subheader("Using Midpoint Odds")
        # Get valid horses for each race (those with at least one non-zero odds)
        valid_horses_mid = {}
        for race_num in range(1, 6):
            valid_horses_mid[race_num] = []
            for i in range(1, 16):
                key = f"race_{race_num}_horse_{i}"
                back = back_odds[key] if back_odds[key] > 0 else 0
                lay = lay_odds[key] if lay_odds[key] > 0 else 0
                
                # If at least one odds value exists, calculate midpoint
                if back > 0 or lay > 0:
                    midpoint = (back + lay) / 2
                    valid_horses_mid[race_num].append((i, midpoint))

        # Find all possible combinations using midpoint odds
        good_combinations_mid = []
        total_combinations_mid = 0
        
        # Generate all possible combinations
        for combo in itertools.product(*[valid_horses_mid[race] for race in range(1, 6)]):
            total_combinations_mid += 1
            # Calculate true odds for this combination
            true_odds = 1.0
            for horse_num, midpoint in combo:
                true_odds *= midpoint
            
            if true_odds < 2500:
                good_combinations_mid.append(combo)
        
        # Calculate probability of at least one good combination winning (midpoint)
        if good_combinations_mid:
            combo_probabilities_mid = []
            for combo in good_combinations_mid:
                prob = 1.0
                for horse_num, midpoint in combo:
                    prob *= (1/midpoint)
                combo_probabilities_mid.append(prob)
            
            prob_none_mid = 1.0
            for prob in combo_probabilities_mid:
                prob_none_mid *= (1 - prob)
            prob_at_least_one_mid = 1 - prob_none_mid
            
            # Display midpoint results
            st.write(f"Total combinations analyzed: {total_combinations_mid}")
            st.write(f"Number of combinations with true odds < $2500: {len(good_combinations_mid)}")
            st.write(f"Probability of at least one good combination winning: {prob_at_least_one_mid:.4%}")
            
            # Display the good combinations
            st.write("\nGood Combinations (true odds < $2500):")
            for combo in good_combinations_mid:
                combo_str = " + ".join([f"Race {race+1} Horse {horse} ({odds:.2f})" 
                                      for race, (horse, odds) in enumerate(combo)])
                true_odds = math.prod(odds for _, odds in combo)
                st.write(f"{combo_str} = {true_odds:.2f}")
        else:
            st.write("No combinations found with true odds < $2500") 
