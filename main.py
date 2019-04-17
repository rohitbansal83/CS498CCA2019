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


def Clean(data, remove_nan=True, indices=[]):
    if noChangeRequired(remove_nan, indices):
        return data
    if len(indices) > 0:
        data = data[:, indices]
    if remove_nan:
        mask = np.isnan(data).any(axis=1)
        data = data[~mask]
    return data


def noChangeRequired(remove_nan, indices):
    return remove_nan == False and len(indices) == 0


def ReadSingle(path):
    with open(path, 'r') as f:
        data = getData(f)
    return data


def Combine(files):
    set_id = 0
    with open(files[0], 'r') as f:
        data = getData(f, set_id)
    for file in files[1:]:
        set_id += 1
        with open(file, 'r') as f:
            data = np.append(data, getData(f, set_id), axis=0)
    return(data)


def getData(f, set_id=-1):
    reader = np.genfromtxt(f, delimiter=',')
    data = np.array(reader)
    if set_id >= 0:
        data = insertSetID(data, set_id)
    return data


def insertSetID(data, set_id):
    data = np.insert(data, data.shape[1]-1, set_id, axis=1)
    return data


def removeOutliers(data, outliers):
    data = np.delete(data, outliers, axis=0)
    return data


def main():
    attributes = ["age", "sex", "cp", "trestbps", "chol",
                  "fbs", "restecg", "thalach", "exang",
                  "oldpeak", "slope", "ca", "thal", "num"]

    files = ['data/processed.cleveland.data',
             'data/processed.hungarian.data',
             'data/processed.switzerland.data',
             'data/processed.va.data']

    cleveland_data = ReadSingle('data/processed.cleveland.data')
    cleveland_data = Clean(cleveland_data, remove_nan=True)
    np.savetxt('pre_cleveland.txt', cleveland_data)

    # coloumn 13 is new feature coloumn containing the set_id: 0 = cleveland, 1 = hungarian etc.
    features = [0, 1, 2, 6, 7, 8, 13, 14]
    combined_data = Combine(files)
    combined_data = Clean(
        combined_data, remove_nan=True, indices=features)
    np.savetxt("pre_combined.txt", combined_data)

    # outliers identified using standarised residuals with significantly high deviaiton (R)
    outliers = [90, 151, 208]
    cleveland_data = removeOutliers(cleveland_data, outliers)

    outliers = [211]
    combined_data = removeOutliers(combined_data, outliers)

    np.savetxt('cleveland_data.txt', cleveland_data, delimiter=',')
    np.savetxt('combined_data.txt', combined_data, delimiter=',')


if __name__ == "__main__":
    main()
