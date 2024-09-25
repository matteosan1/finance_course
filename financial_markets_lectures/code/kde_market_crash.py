from scipy.stats import norm

actual_data_prob = np.sum(train_returns < -0.04) / len(train_returns)

crash_range = np.linspace(-0.1, -0.04, 1000)
best_kde_probs = np.exp(best_kde.score_samples(crash_range.reshape(-1,1)))
best_kde_probs_integrated = np.trapz(best_kde_probs, x=crash_range)

normal_probs = norm.cdf(-0.04, train_returns_arr.mean(), train_returns_arr.std())

print(f'Actual probability:              {actual_data_prob:.3%}')
print(f'Best Fit KDE probability:        {best_kde_probs_integrated:.3%}')
print(f'Normal distribution probability: {normal_probs:.3%}')