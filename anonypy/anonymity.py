def is_k_anonymous(partition, k):
    return len(partition) >= k


def is_l_diverse(df, partition, sensitive_column, l):
    diversity = len(df.loc[partition][sensitive_column].unique())
    return diversity >= l


def is_t_close(df, partition, sensitive_column, global_freqs, p):
    total_count = float(len(partition))
    d_max = None
    group_counts = df.loc[partition].groupby(sensitive_column, observed=False)[sensitive_column].agg("count")

    for value, count in group_counts.to_dict().items():
        prob = count / total_count
        d = abs(prob - global_freqs[value])
        if d_max is None or d > d_max:
            d_max = d
    return d_max <= p


def get_global_freq(df, sensitive_column):
    global_freqs = {}
    total_count = float(len(df))
    group_counts = df.groupby(sensitive_column, observed=False)[sensitive_column].agg("count")


    for value, count in group_counts.to_dict().items():
        p = count / total_count
        global_freqs[value] = p
    return global_freqs
