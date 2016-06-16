import pandas as pd
import numpy as np

def oversample(X, y, target):
    """
    INPUT:
    X, y - your data: X ndarray of all datatypes & y array of the
    positive and negative classes
    target - the percentage of positive class
             observations in the output
    OUTPUT:
    X_oversampled, y_oversampled - oversampled data
    `oversample` randomly replicates positive observations
    in X, y to achieve the target proportion
    """
    if target < sum(y) / float(len(y)):
        return X, y
    # determine how many new positive observations to generate
    positive_count = sum(y)
    negative_count = len(y) - positive_count
    target_positive_count = target * negative_count / (1. - target)
    target_positive_count = int(round(target_positive_count))
    number_of_new_observations = target_positive_count - positive_count
    # randomly generate new positive observations
    positive_obs_indices = np.where(y == 1)[0]  # np.where returns a tuple containing an array of indices
    new_obs_indices = np.random.choice(positive_obs_indices,
                                       size=number_of_new_observations,
                                       replace=True)
    X_new, y_new = X[new_obs_indices], y[new_obs_indices]
    X_positive = np.vstack((X[positive_obs_indices], X_new))
    y_positive = np.concatenate((y[positive_obs_indices], y_new))
    X_negative = X[y == 0]
    y_negative = y[y == 0]
    X_oversampled = np.vstack((X_negative, X_positive))
    y_oversampled = np.concatenate((y_negative, y_positive))

    return X_oversampled, y_oversampled


def featurize_data(jsonfile, target=0.4):
    # Read JSON File
    df = pd.read_json(jsonfile)

    # Create fraud column
    df['fraud'] = (df['acct_type'] == 'fraudster_event') | \
                  (df['acct_type'] == 'fraudster') | \
                  (df['acct_type'] == 'fraudster_att')

    # If currency is a certain value, set boolean
    df['currency_grp'] = df['currency'].isin(['GBP','USD','EUR','CAD'])

    # If delivery method is Nan, set to some value. Deserves review because the value is arbitrary
    df.loc[df['delivery_method'].isnull() == True, 'delivery_method'] = 2

    # create initial feature matrix
    df['has_country'] = df['venue_country'].isnull()
    df['has_state'] = df['venue_state'].isnull()
    df['has_name'] = df['venue_name'].isnull()
    df['has_latitude'] = df['venue_latitude'].isnull()
    df['has_longitude'] = df['venue_longitude'].isnull()
    df['has_address'] = df['venue_address'].isnull()

    # change X to match uncorrelated features
    y = df.pop('fraud')
    # X = df[['has_country', 'has_state', 'has_name', 'has_address', 'num_payouts', 'show_map']]

    X = pd.concat([df['num_payouts'],df['fb_published'],df['has_analytics'], \
                              df['show_map'],df['delivery_method'],df['currency_grp'], \
                             df['has_latitude']], axis=1)
    return X.values,y.values
