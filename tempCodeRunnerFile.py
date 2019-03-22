    features = [0, 1, 2, 6, 7, 8, 13, 14]
    combined_data = Combine(files)
    combined_data = Clean(combined_data, remove_nan=True, indices=features)
    np.savetxt('combined_data.txt', combined_data)