import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy.signal import savgol_filter


def excel_to_python(file, sheet):
    column_delete = "Timestamp"
    driverExcelFile = pd.ExcelFile("{}".format(file))
    df = pd.read_excel(driverExcelFile, "{}".format(sheet), usecols=lambda x: x not in column_delete)
    return df


def smoothing(dataframe):
    data_smoothed = dataframe.apply(lambda x: savgol_filter(x, window_length=51, polyorder=3))
    return data_smoothed


def standardization(dataframe):
    standscaler = StandardScaler()
    scaledscaler_df = standscaler.fit_transform(dataframe)
    standarised_df = pd.DataFrame(scaledscaler_df, columns=df.columns)
    return standarised_df


def normalisation(dataframe):
    norm = MinMaxScaler()
    norm_df = norm.fit_transform(dataframe)
    normalised_df = pd.DataFrame(norm_df, columns=df.columns)
    return normalised_df


def feature_scaling(smoothed_data, action):
    if action == 'N':
        return normalisation(smoothed_data)
    elif action == 'S':
        return standardization(smoothed_data)


def plot(dataframe, scaled, title):
    fig, axs = plt.subplots(2)
    fig.suptitle("[1] RAW DATA, [2] {}".format(title))
    axs[0].plot(dataframe)
    axs[1].plot(scaled)
    fig.text(0.5, 0.04, 'Sequence number', ha='center')
    fig.text(0.08, 0.55, 'Value', va='center', rotation='vertical')
    plt.legend(['X', 'Y', 'Z'], loc='upper right', bbox_to_anchor=(1.07, 2))
    plt.savefig('{}.png'.format(title))
    plt.show()


if __name__ == "__main__":
    df = excel_to_python("kierowcaA.xlsx", "Acceleration")
    print(df)

    data_smoothed = smoothing(df)
    data_normalised = feature_scaling(data_smoothed, 'N')
    data_standarised = feature_scaling(data_smoothed, 'S')

    plot(df, data_normalised, 'NORMALISED')
    plot(df, data_standarised, 'STANDARISED')
