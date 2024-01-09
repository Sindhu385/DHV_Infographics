# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 20:02:28 2024

@author: sindh
"""
# imported required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def process_data(series_name, file_path):
    """
        Process data for a specific series from a CSV file.

        Parameters:
        - series_name (str): The name of the series to be processed.
        - file_path (str): The path to the CSV file containing the data.

        Returns:
        - clean_df (DataFrame): Cleaned DataFrame with specified series data.
        - df_t (DataFrame): Transposed DataFrame for easy plotting.
        """

    df = pd.read_csv(file_path)
    data = df[df['Series Name'] == series_name]
    if data.empty:
        print(f"No data found for series: {series_name}")
        return None
    clean_df = data.drop(['Country Code', 'Series Code',
                         'Series Name'], axis=1).reset_index(drop=True)
    clean_df = clean_df.rename(columns=lambda x: x.split(' [')[0])
    df_t = clean_df.transpose()
    df_t.columns = df_t.iloc[0]

    # Skip the first row and convert the index to numeric values
    df_t = df_t.iloc[1:]
    df_t.index = pd.to_numeric(df_t.index)

    # Add a 'Years' column based on the numeric index
    df_t['Years'] = df_t.index

    # Return the cleaned DataFrame and the transposed DataFrame
    return clean_df, df_t


def subplot_all(df1, df2, df3_t, df4_t, df5, report_text):
    """
    Create a 2x3 subplot with different types of visualizations.

    Parameters:
    - df1 (DataFrame): DataFrame for the first subplot.
    - df2 (DataFrame): DataFrame for the second subplot.
    - df3_t (DataFrame): Transposed DataFrame for the third subplot.
    - df4_t (DataFrame): Transposed DataFrame for the fourth subplot.
    - df5 (DataFrame): DataFrame for the fifth subplot.
    - report_text (str): Text content for the sixth subplot (report).

    Returns:
    - None
    """
    fig, axs = plt.subplots(2, 3, figsize=(30, 12), facecolor='lightblue')

    # Plot 1 - Bar Horizontal
    colors = ['brown', 'pink', 'grey', 'purple', 'yellow']
    ax1 = sns.barplot(x='2010', y='Country Name', data=df1,
                      palette=colors, ax=axs[0, 0])
    ax1.set(xlabel='metric tons', ylabel='Countries')
    ax1.set_xlabel('metric tons', fontsize=16)  # Adjust x-axis label font size
    ax1.set_ylabel('Countries', fontsize=16)    # Adjust y-axis label font size
    ax1.set_title('Agricultural nitrous oxide emissions in 2020 year',
                  fontsize=16, fontweight='bold')
    # Adjust ticks font size
    ax1.tick_params(axis='both', which='both', labelsize=14)

    # Plot 2 - Bar
    colors = ['brown', 'pink', 'grey', 'purple', 'yellow']
    ax2 = sns.barplot(x='Country Name', y='2010', data=df2,
                      palette=colors, width=0.5, ax=axs[0, 1])
    ax2.set(xlabel='Countries', ylabel='% of fertilizer production')
    # Adjust x-axis label font size
    ax2.set_xlabel('Countries', fontsize=16)
    # Adjust y-axis label font size
    ax2.set_ylabel('% of fertilizer production', fontsize=16)
    ax2.set_title('Fertilizer consumption in 2020 year',
                  fontsize=16, fontweight='bold')
    # Adjust ticks font size
    ax2.tick_params(axis='both', which='both', labelsize=12)

    # Plot 3 - Line
    sns.set_style("whitegrid")
    df3_t.plot(x='Years', y=[
        'Australia', 'China', 'India', 'Japan', 'Russian Federation'],
               xlabel='Years', ylabel='percentage', marker='.', ax=axs[0, 2])
    # Adjust x-axis label font size
    axs[0, 2].set_xlabel('Years', fontsize=16)
    # Adjust y-axis label font size
    axs[0, 2].set_ylabel('Percentage', fontsize=16)
    axs[0, 2].set_title(
        'Agricultural raw materials imports (% of merchandise imports)',
        fontsize=16, fontweight='bold')
    axs[0, 2].legend(loc='upper right')
    axs[0, 2].tick_params(axis='both', which='both',
                          labelsize=12)  # Adjust ticks font size

    # Plot 4 - Point
    dot = sns.pointplot(x='Years', y='Value', hue='Country',
                        data=df4_t.melt(id_vars=['Years'],
                                        var_name='Country',
                                        value_name='Value'), ax=axs[1, 0])
    dot.set_xticklabels(dot.get_xticklabels(), rotation=90)
    # Adjust x-axis label font size
    axs[1, 0].set_xlabel('Years', fontsize=16)
    # Adjust y-axis label font size
    axs[1, 0].set_ylabel('Value', fontsize=16)
    axs[1, 0].set_title(
        'Agricultural raw materials exports (% of merchandise exports)',
        fontsize=16, fontweight='bold')
    axs[1, 0].tick_params(axis='both', which='both',
                          labelsize=12)  # Adjust ticks font size

    # Plot 5 - Pie
    label = ['Australia', 'China', 'India', 'Japan', 'Russian Federation']
    explode = [0.1 if country == 'India' else 0 for country in label]

    wedgeprops = {"linewidth": 0, "antialiased": True}
    axs[1, 1].pie(df5['2010'], autopct='%1.0f%%', labels=label, explode=explode,
                  startangle=180, wedgeprops=wedgeprops, pctdistance=0.85)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    axs[1, 1].add_artist(centre_circle)
    axs[1, 1].set_title(
        'Annual freshwater withdrawals, agriculture (% of total freshwater withdrawal)',
        fontsize=16, fontweight='bold')
    axs[1, 1].tick_params(axis='both', which='both',
                          labelsize=12)  # Adjust ticks font size

    # Plot 6 - Your Report
    plt.text(0.0, -0.2, report_text, ha='left',
             va='bottom', fontsize=20, color='black')
    plt.axis('off')  # Hide axes for the report

    plt.suptitle("Agricultural and Environmental Metrics Analysis", fontsize=28,
                 y=1, color='white', fontweight='bold', ha='center',
                 backgroundcolor='black')

    # Adjust layout
    plt.tight_layout()

    #plt.savefig('22077385.png', dpi=300)
    plt.show()


# Specify the file path for the CSV data
file_path = 'Infographics_Data.csv'

# Process data for 'Agricultural nitrous oxide emissions'
df1, df1_t = process_data(
    'Agricultural nitrous oxide emissions (thousand metric tons of CO2 equivalent)',
    file_path)

# Process data for 'Fertilizer consumption'
df2, df2_t = process_data(
    'Fertilizer consumption (% of fertilizer production)', file_path)

# Process data for 'Agricultural raw materials imports'
df3, df3_t = process_data(
    'Agricultural raw materials imports (% of merchandise imports)', file_path)

# Process data for 'Agricultural raw materials exports'
df4, df4_t = process_data(
    'Agricultural raw materials exports (% of merchandise exports)', file_path)

# Process data for 'Annual freshwater withdrawals, agriculture'
df5, df5_t = process_data(
    'Annual freshwater withdrawals, agriculture (% of total freshwater withdrawal)',
    file_path)

# Define a detailed report_text providing insights from the data visualizations,
# highlighting key observations and patterns related to agricultural and environmental metrics.

report_text = """The data visualizations provide valuable insights into agricultural 
and environmental metrics.The pie chart indicates India's significant 
share (21%) in annual freshwater withdrawals for agriculture, contributing 
substantially to total freshwater usage. Nitrous oxide emissions reveal 
a diverse landscape, with Australia leading at 28%, followed closely by 
China (25%).Fertilizer consumption, dominated by China (47%) and India 
(20%), emphasizes their pivotal roles in global agricultural practices. 
Raw material exports showcase Australia and Russia as major contributors, 
each accounting for 25% and 22%, respectively. Overall, the visualizations
highlight distinct regional patterns, emphasizing the importance of tailored
environmental strategies for each country.
                                                                     
                                                                
                                                                
                                                         Name: Sindhu Nadilla           
                                                         Student id: 22077385           
            """

subplot_all(df1, df2, df3_t, df4_t, df5, report_text)

