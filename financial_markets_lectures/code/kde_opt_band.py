from sklearn.model_selection import GridSearchCV

params = {'bandwidth' : np.linspace(0.001, 0.01, 50)}
grid = GridSearchCV(KernelDensity(), 
                    param_grid=params, 
                    cv=20,
                    n_jobs=-1).fit(train_returns_arr)

print (grid.best_params_)

best_kde = KernelDensity(bandwidth=grid.best_params_['bandwidth']) \
           .fit(train_returns_arr)

log_probs = best_kde.score_samples(xs.reshape(-1,1))
best_kde_pdf = np.exp(log_probs)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15,5))
for i in range(3):
    ax[i].hist(train_returns, density=True, color='green', bins=50, alpha=0.5, 
               histtype='stepfilled', label='True Distribution')
    ax[i].plot(xs, normal_pdf.pdf(xs), color='red', 
         linestyle='--', label='Normal Distribution')
    ax[i].plot(xs, best_kde_pdf, label='Cross Validated KDE Distribution')

ax[0].set_ylabel('Density')
ax[1].set_xlabel('Daily Returns')

ax[1].set_xlim([-0.07, -0.02])
ax[1].set_ylim([0, 6])
ax[2].set_xlim([0.02, 0.07])
ax[2].set_ylim([0, 6])

ax[2].legend()
plt.show()