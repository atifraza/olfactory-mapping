# -*- coding: utf-8 -*-
"""
Load and preprocess data for Olfactory Mapping

This file loads the VoC mixing ratios and combines them with
the weather data.
The VoC mixing ratios are in two conditions:
    a) with missing values removed before hand
    b) with missing values present
In case missing values are present the script will impute the
values based on interpolation.

Once the VoC mixing ratios have been imported, the weather data
is loaded and merged with the VoC data using the same time
granularity as the VoC data.

Finally, the dataframe is saved in pickle format for compression
and reuse in Jupyter notebooks. Therefore, once preprocessed you
do not need to run this scrip unless you want to experiment with
different options.

Please see the script for these options.

"""
import numpy as np
import pandas as pd

# Mean time duration for mixing ratio readings
mean_time = np.timedelta64(21, 's')

data_dir = './'

mixing_ratios = []

for num in range(12):
    # Load the observed mixing ratios of different *VoC*s (in $ppb$)
    df = pd.read_csv(data_dir + 'VoC_mixing_ratios/mixing_ratios_' + \
                     str(num) + '.csv',  # path
                     header=0,  # Row 0 is header
                     index_col=0,  # Treat Column 0 as index
                     parse_dates=[0],  # Parse Column 0 for dates
                     infer_datetime_format=True,  # Infer format
                     # Do not load columns with huge number of missing values
                     usecols=lambda col: col not in ['m59', 'm121'])
    # Convert *VoC* values from $ppb$ to $ppt$
    df = df.multiply(1000000)
    # Replace negative (garbage) values given out by the PTR-MS with NaN. They
    # will be replaced by interpolated values based on neighboring values
    df[df < 0] = np.NaN
    # Append the current dataframe to the list of mixing ratios dataframes
    mixing_ratios.append(df)

first_mixing_ratios = mixing_ratios

mixing_ratios = []

for num in range(12, 15):
    # Load the observed mixing ratios of different *VoC*s (in $ppb$)
    df = pd.read_csv(data_dir + 'VoC_mixing_ratios/mixing_ratios_' + \
                     str(num) + '.csv',  # path
                     header=0,  # Row 0 is header
                     index_col=0,  # Treat Column 0 as index
                     parse_dates=[0],  # Parse Column 0 for dates
                     infer_datetime_format=True,  # Infer format
                     # Do not load columns with huge number of missing values
                     usecols=lambda col: col not in ['m59', 'm121'])
    # Convert *VoC* values from $ppb$ to $ppt$
    df = df.multiply(1000000)
    # Replace negative (garbage) values given out by the PTR-MS with NaN. They
    # will be replaced by interpolated values based on neighboring values
    df[df < 0] = np.NaN
    # Append the current dataframe to the list of mixing ratios dataframes
    mixing_ratios.append(df)
del num, df

# Concatenate all the mixing ratios' dataframes
mixing_ratios = pd.concat([*first_mixing_ratios, *mixing_ratios])

# Impute missing values using index frequency
mixing_ratios.interpolate(method='index', inplace=True)
# Drop the rows with missing values, basically rows at start or end which
# do not get interpolated values due to open endedness
mixing_ratios.dropna(inplace=True)


# import numpy as np
# import pandas as pd

# # Load data with missing segments
# drop_missing_voc_data_segments = True
# # Impute missing weather data segments with interpolated values
# interpolating_missing_weather = False
# # Use instantaneous weather conditions for merging mixing ratios or
# # use the average values for the duration of mixing ratio reading
# using_avg_weather_conditions = False
# # Mean time duration for mixing ratio readings
# mean_time = np.timedelta64(22, 's')

# data_dir = './'

# voc_directory = 'missing_segments_' + \
#                 ('removed' if drop_missing_voc_data_segments else 'present')

# # List of monitored *VoC*s
# voc_dict = {'m33': 'Methanol',
#             'm42': 'Acetonitrile',
#             'm45': 'Acetaldehyde',
#             # 'm59': 'Acetone',  # Entire column has missing values
#             'm61': 'Acetic acid',
#             'm63': 'DMS (emitted by algea)',
#             'm69': 'MBO (Isoprene)',
#             'm71': 'MVK (Isoprene, oxygenated)',
#             'm73': 'MEK',
#             'm79': 'Benzene',
#             'm81': 'Pinenes',
#             'm93': 'Toluene',
#             'm107': 'Xylene',
#             # 'm121': 'TMB',  # Over 70% missing values
#             'm137': 'a-pinene'
#             }

# mixing_ratios = []

# for num in range(15):
#     # Load the observed mixing ratios of different *VoC*s (in $ppb$)
#     df = pd.read_csv(data_dir + 'VoC_mixing_ratios/' + voc_directory + \
#                      '/mixing_ratios_' + str(num) + '.csv',  # path
#                      header=0,  # Row 0 is header
#                      index_col=0,  # Treat Column 0 as index
#                      parse_dates=[0],  # Parse Column 0 for dates
#                      infer_datetime_format=True,  # Infer format
#                      # Do not load columns with huge number of missing values
#                      usecols=lambda col: col not in ['m59', 'm121'])
#     # Convert *VoC* values from $ppb$ to $ppt$
#     df = df.multiply(1000000)
#     # Replace negative (garbage) values given out by the PTR-MS with NaN. They
#     # will be replaced by interpolated values based on neighboring values
#     df[df < 0] = np.NaN
#     if drop_missing_voc_data_segments:
#         # Impute missing values using index frequency
#         df.interpolate(method='index', inplace=True)
#         # Drop the rows with missing values, basically rows at start or end which
#         # do not get interpolated values due to open endedness
#         df.dropna(inplace=True)
#     # Append the current dataframe to the list of mixing ratios dataframes
#     mixing_ratios.append(df)
# del num, df

# # Concatenate all the mixing ratios' dataframes
# mixing_ratios = pd.concat(mixing_ratios)

# if not drop_missing_voc_data_segments:
#     # Impute missing values using index frequency
#     mixing_ratios.interpolate(method='index', inplace=True)
#     # Drop the rows with missing values, basically rows at start or end which
#     # do not get interpolated values due to open endedness
#     mixing_ratios.dropna(inplace=True)


# # Load the weather conditions data
# weather_data = pd.read_csv(data_dir + 'weather/weather_data.csv',  # path
#                            header=0,  # Row 0 is header
#                            index_col=0,  # Treat Column 0 as index
#                            parse_dates=[0],  # Parse Column 0 for dates
#                            infer_datetime_format=True)  # Infer format

# if not interpolating_missing_weather:
#     weather_data.dropna(axis=0, how='any', inplace=True)
# else:
#     # Create a DateTimeIndex with the weather data start and end time
#     datetimeindex = pd.date_range(start='2018-05-06 13:04:34',
#                                   end='2018-06-12 10:00:49', freq='S')
#     # Reindex the weather data to incorporate missing segment(s)
#     weather_data = weather_data.reindex(datetimeindex)
#     del datetimeindex
#     # Interpolate the missing values based on index frequency
#     weather_data.interpolate(method='index', inplace=True)
# del interpolating_missing_weather

# if not using_avg_weather_conditions:
#     # merge_asof(left, right, on='a', direction='nearest')
#     merged_df = pd.concat([weather_data, mixing_ratios], axis=1, join='inner')
#     merged_df.index.name = 'DateTime'
# else:
#     merged_df = pd.DataFrame(index=mixing_ratios.index,
#                              columns=[*weather_data.columns,
#                                       *mixing_ratios.columns])
#     prev_ind = None
#     for curr_ind in mixing_ratios.index:
#         if prev_ind is None or prev_ind + mean_time < curr_ind:
#             prev_ind = curr_ind - mean_time
#         weather_segment = weather_data[prev_ind:curr_ind].mean()
#         for col in weather_data.columns:
#             merged_df.at[curr_ind, col] = weather_segment[col]
#         for col in mixing_ratios.columns:
#             merged_df.at[curr_ind, col] = mixing_ratios.at[curr_ind, col]
#         # merged_df.update(weather_segment)
#         # merged_df.update(mixing_ratios.loc[curr_ind])
#         # print(merged_df.loc[curr_ind])
#         prev_ind = curr_ind + np.timedelta64(1, 's')
#     del prev_ind, curr_ind, weather_segment, col
# del using_avg_weather_conditions, mixing_ratios, weather_data

# # Transform the Wind Direction column to int64
# merged_df['WDir_Deg'] = merged_df['WDir_Deg'].astype(np.int64)

# # Add the instantaneous distance travelled by the VoCs during the time of 
# # VoC reading
# time_diff = merged_df.index.to_series().diff()
# time_diff.iloc[0] = mean_time
# val_filter = time_diff[time_diff > mean_time]
# time_diff[val_filter.index] = mean_time

# merged_df.insert(column='Inst_Dist', loc=2,
#                  value=merged_df.WSpeed * (time_diff / np.timedelta64(1, 's')))

# del mean_time, val_filter, time_diff

# merged_df.to_pickle(data_dir + 'merged_df.pkl.xz')
