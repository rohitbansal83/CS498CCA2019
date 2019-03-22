# ------------------------------------ Attribute Information ----------------------------------- #
#   age      -> age in years                                                                     #
#   sex      -> sex (1 = male; 0 = female)                                                       #
#   cp       -> chest pain type                                                                  #
#                   -- Value 1: typical angina                                                   #
#                   -- Value 2: atypical angina                                                  #
#                   -- Value 3: non-anginal pain                                                 #
#                   -- Value 4: asymptomatic                                                     #
#   trestbps -> resting blood pressure (in mm Hg on admission to the hospital)                   #
#   chol     -> serum cholestoral in mg/dl                                                       #
#   fbs      -> fasting blood sugar > 120 mg/dl  (1 = true; 0 = false)                           #
#   restecg  -> resting electrocardiographic results                                             #
#                   -- Value 0: normal                                                           #
#                   -- Value 1: having ST-T wave abnormality (T wave inversions and/or ST        #
#                               elevation or depression of > 0.05 mV)                            #
#                   -- Value 2: showing probable or definite left ventricular hypertrophy        #
#                               by Estes' criteria                                               #
#   thalach  -> maximum heart rate achieved                                                      #
#   exang    -> exercise induced angina (1 = yes; 0 = no)                                        #
#   oldpeak  -> ST depression induced by exercise relative to rest                               #
#   slope    -> the slope of the peak exercise ST segment                                        #
#                   -- Value 1: upsloping                                                        #
#                   -- Value 2: flat                                                             #
#                   -- Value 3: downsloping                                                      #
#   ca      ->  number of major vessels (0-3) colored by flourosopy                              #
#   thal    ->  3 = normal; 6 = fixed defect; 7 = reversable defect                              #
#   num     ->  diagnosis of heart disease (angiographic disease status)                         #
#                   -- Value 0: < 50% diameter narrowing                                         #
#                   -- Value 1: > 50% diameter narrowing                                         #
#                   (in any major vessel: attributes 59 through 68 are vessels)                  #
# ---------------------------------------------------------------------------------------------- #

import numpy as np


def CleanData(data, remove_nan=True, indices=[]):
    if noChangeRequired(remove_nan, indices):
        return data
    if remove_nan:
        mask = np.isnan(data).any(axis=1)
        return data[~mask]
    return data


def noChangeRequired(remove_nan, indices):
    return remove_nan == False and len(indices) == 0


def ReadFile(path):
    with open(path, 'r') as f:
        reader = np.genfromtxt(f, delimiter=',')
        data = np.array(reader)
    return data


def Combine(files):
    with open(files[0], 'r') as f:
        reader = np.genfromtxt(f, delimiter=',')
        data = np.array(reader)

    for file in files[1:]:
        with open(file, 'r') as f:
            reader = np.genfromtxt(f, delimiter=',')
            data = np.append(data, reader, axis=0)

    return(data)


def main():
    attributes = ["age", "sex", "cp", "trestbps", "chol",
                  "fbs", "restecg", "thalach", "exang",
                  "oldpeak", "slope", "ca", "thal", "num"]

    files = ['data/processed.cleveland.data',
             'data/processed.hungarian.data',
             'data/processed.switzerland.data',
             'data/processed.va.data']

    # data = Combine(files)
    data = ReadFile('data/processed.cleveland.data')
    print(data.shape)
    data = CleanData(data, remove_nan=True)
    print(data)
    print(data.shape)


if __name__ == "__main__":
    main()
