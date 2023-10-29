import streamlit as st
import numpy as np
from PIL import Image
import joblib

model = joblib.load('models/final_model.pkl')

st.set_page_config(
    page_title="Fraud Prediction App",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

image = Image.open('image.jpg')

st.image(image, use_column_width=True)


def predict_fraud(amt,gender,city_pop,age,trans_month,trans_year,latitudinal_distance,longitudinal_distance,category_food_dining,category_gas_transport,category_grocery_net,category_grocery_pos,category_health_fitness,category_home,category_kids_pets,category_misc_net,category_misc_pos,category_personal_care,category_shopping_net,category_shopping_pos,category_travel):
    input=np.array([[amt,gender,city_pop,age,trans_month,trans_year,latitudinal_distance,longitudinal_distance,category_food_dining,category_gas_transport,category_grocery_net,category_grocery_pos,category_health_fitness,category_home,category_kids_pets,category_misc_net,category_misc_pos,category_personal_care,category_shopping_net,category_shopping_pos,category_travel]]).astype(np.float64)
    
    prediction = model.predict(input)
    
    return int(prediction)


def main():
    #st.title("Credit Card Fraud Prediction") 
    html_temp = """
    <div style="background:#8325be ;padding:10px">
    <h2 style="color:white;text-align:center;">Online Fraud Prediction ML App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)

    amt = st.text_input("Amount")
    city_pop = st.text_input("City Code")
    age = st.text_input("Age")
    trans_month = st.slider("Transaction Month",min_value=1,max_value=12,step=1)
    #trans_year = st.slider("Transaction Year",2019,2020)
    trans_year = st.slider("Transaction Year",min_value=2019,max_value=2022,step=1)
    
    latitudinal_distance = st.slider("Latitudinal Distance",min_value=0.0,max_value=1.0,step=0.001)
    longitudinal_distance = st.slider("Longitudinal Distance",min_value=0.0,max_value=1.0,step=0.001)    
    
    #Gender Male(1) or Female(0)
    gender = st.radio("Gender",('Male','Female'))

    if gender == 'Male':
        gender = 1
    else:
        gender = 0
    
    selected_variable = st.selectbox("Select Transaction Type", 
                                     ["Food Dining", "Gas Transport","Grocery Net", "Grocery Pos",
                                      "Health Fitness", "Home","Personal Care", "Kid Pets","Misc Net", 
                                      "Misc Pos", "Travel","Shopping Net","Shopping Pos"])
    
    category_food_dining = 0 	
    category_gas_transport = 0 	
    category_grocery_net = 0 	
    category_grocery_pos = 0 	
    category_health_fitness = 0 
    category_home = 0 			
    category_kids_pets  = 0 		
    category_misc_net = 0 		
    category_misc_pos = 0 		
    category_personal_care = 0 	
    category_shopping_net = 0 	
    category_shopping_pos = 0 	
    category_travel = 0 		

    if selected_variable == 'Food Dining':
        category_food_dining = 1
    elif selected_variable == 'Gas Transport':
        category_gas_transport = 1
    elif selected_variable == 'Grocery Net':	
        category_grocery_net = 1
    elif selected_variable == 'Grocery Pos':	 	
        category_grocery_pos = 1
    elif selected_variable == 'Health Fitness':	 	
        category_health_fitness = 1
    elif selected_variable == 'Home':	 
        category_home = 1
    elif selected_variable == 'Kid Pets':	 			
        category_kids_pets  = 1
    elif selected_variable == 'Misc Net':	 		
        category_misc_net = 1
    elif selected_variable == 'Misc Pos':	 		
        category_misc_pos = 1
    elif selected_variable == 'Personal Care':	 		
        category_personal_care = 1
    elif selected_variable == 'Shopping Net':	 	
        category_shopping_net = 1
    elif selected_variable == 'Shopping Pos':	 	
        category_shopping_pos = 1
    else:	 	
        category_travel = 1
    
    if st.button("Predict the Fraud"): 
        output = predict_fraud(amt,gender,city_pop,age,trans_month,trans_year,latitudinal_distance,longitudinal_distance,category_food_dining,category_gas_transport,category_grocery_net,category_grocery_pos,category_health_fitness,category_home,category_kids_pets,category_misc_net,category_misc_pos,category_personal_care,category_shopping_net,category_shopping_pos,category_travel)
        if output == 0:
            #st.success("IT'S A VALID TRANSACTION")
            html_temp = """
            <div style="background:#08A04B ;padding:10px ; border-radius:10px ">
            <h3 style="color:white;text-align:center;">IT'S A VALID TRANSACTION</h3>
            </div>
            """
            st.markdown(html_temp, unsafe_allow_html = True)
        else:
            #st.success(output)
            #st.success("IT'S A FRAUD TRANSACTION")
            html_temp = """
            <div style="background:#FF0000 ;padding:10px ; border-radius:10px">
            <h3 style="color:white;text-align:center;">IT'S A FRAUD TRANSACTION</h3>
            </div>
            """
            st.markdown(html_temp, unsafe_allow_html = True)

    
if __name__=='__main__':
    main()
