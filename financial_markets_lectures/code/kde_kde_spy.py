from sklearn.neighbors import KernelDensity

train_returns_arr = np.array(train_returns).reshape(-1, 1)
kde = KernelDensity(bandwidth = 0.001).fit(train_returns_arr)

mu, sigma = train_returns.mean(), train_returns.std()
xs = np.linspace(-0.06, 0.06, 1000)

log_probs = kde.score_samples(xs.reshape(-1, 1))
kde_pdf = np.exp(log_probs)
normal_pdf = norm(*params)

plt.hist(train_returns, density=True, color='xkcd:green', bins=50, alpha=0.5, 
         histtype='bar', label='True Distribution')
plt.plot(xs, normal_pdf.pdf(xs), color='red', linestyle='--', 
         label='Normal Distribution')
plt.plot(xs, kde_pdf, label='KDE Fitted Distribution')
plt.ylabel('Density')
plt.xlabel('Daily Returns')
plt.legend(loc='best')
plt.show()