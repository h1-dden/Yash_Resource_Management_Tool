import streamlit as st
from database import db_operations
from view import employee_plots

def display_employee_data():

    """ Display employee data in the Streamlit app"""

    st.markdown(" ")

    # Fetch data from the database for employees
    employee_df = db_operations.fetch_employee_data()
    training_schedule_df = db_operations.fetch_training_schedule_data()
    
    # Set up the layout with two columns: filters on the left, table on the right
    col1, col2 = st.columns([1, 3])  # Make the filter column narrower than the table column
    
    with col1:
        st.markdown("### Filters")
        # Add filters for various columns
        grade_filter = st.multiselect("Grade", 
                                      options=employee_df['Grade'].unique(), 
                                      default=employee_df['Grade'].unique()
                                      )
        #Communication filter(begginer,intermediate,advanced)
        comm_level_filter = st.multiselect("Communication Level", 
                                           options=employee_df['Communication_Level'].unique(), 
                                           default=employee_df['Communication_Level'].unique()
                                           )
        #Employment status filter(probation,permanent)
        employment_filter = st.multiselect("Employee Status", 
                                           options=employee_df['Employment_Status'].unique(), 
                                           default=employee_df['Employment_Status'].unique()
                                           )
        #Bench status(benched,deployed,notice_period)
        bench_status_filter = st.selectbox("Bench Status", 
                                           options=['All'] + list(employee_df['Bench_Status'].unique())
                                           )
        #
        experience_min = st.slider("Minimum Experience (Years)", 
                                   min_value=int(employee_df['Experience'].min()), 
                                   max_value=int(employee_df['Experience'].max()), 
                                   value=int(employee_df['Experience'].min())
                                   )
        experience_max = st.slider("Maximum Experience (Years)", 
                                   min_value=int(employee_df['Experience'].min()), 
                                   max_value=int(employee_df['Experience'].max()), 
                                   value=int(employee_df['Experience'].max())
                                   )
        stack_filter = st.multiselect("Stack", 
                                      options=employee_df['Stack'].unique(), 
                                      default=employee_df['Stack'].unique()
                                      )
        
        skill_filter = st.multiselect("Skills",
                                      options=employee_df['Skill_Level'].unique(),
                                      default=employee_df['Skill_Level'].unique()
                                      )
        
        # Apply filters to the DataFrame
        filtered_employee_df = employee_df[
            (employee_df['Grade'].isin(grade_filter)) &
            (employee_df['Communication_Level'].isin(comm_level_filter)) &
            (employee_df['Employment_Status'].isin(employment_filter)) &
            ((employee_df['Bench_Status'] == bench_status_filter) if bench_status_filter != 'All' else True) &
            (employee_df['Experience'] >= experience_min) &
            (employee_df['Experience'] <= experience_max) &
            (employee_df['Stack'].isin(stack_filter)) &
            (employee_df['Skill_Level'].isin(skill_filter)) &
            (employee_df['Stack'].isin(stack_filter)) &
            (employee_df['Skill_Level'].isin(skill_filter))
        ]
        
        # Download button for filtered data
        st.markdown(" ")
        st.markdown(" ")
        st.download_button(
            label="Download Filtered Employee Data",
            data=filtered_employee_df.to_csv(index=False).encode('utf-8'),
            file_name="filtered_employee_data.csv",
            mime="text/csv"
        )

    # Display filtered table in the second column
    with col2:
        st.dataframe(filtered_employee_df, use_container_width=True)
        # Filtered Data Visualization
        st.markdown(" ")
        employee_plots.visualize_filtered_employee_data(filtered_employee_df)
