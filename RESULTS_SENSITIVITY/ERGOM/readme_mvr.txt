Reference:
https://github.com/BoldingBruggeman/parsac/blob/392ab3ffd6521ed16eb3106263e2049b7935cef0/parsac/sensitivity.py

function:

def mvr(names, A, y, verbose=False):
    """Multiple linear regression based on numpy.linalg.lstsq,
    with additional statistics to describe significance of overall model and parameter slopes."""
    import numpy.linalg
    import scipy.stats

    assert A.ndim == 2
    assert A.shape[0] == y.shape[0]
    beta, SS_residuals, rank, s = numpy.linalg.lstsq(A, y, rcond=None)

    # Equivalent expressions for sum of squares.
    #y_hat = numpy.dot(A, beta)
    #SS_residuals = ((y-y_hat)**2).sum(axis=0)
    #SS_residuals = numpy.dot(y.T, y - y_hat)
    #SS_total = numpy.dot(y.T, y -  y.mean(axis=0))
    #SS_explained = numpy.dot(y.T, y_hat - y.mean(axis=0))

    # number of ensemble members, number of parameters
    n, k = A.shape

    # total sum of squares, will equal n if observations are z-score transformed.
    SS_total = ((y -  y.mean(axis=0))**2).sum()

    R2 = 1. - SS_residuals/SS_total

    # Compute F statistic to describe significance of overall model
    SS_explained = SS_total - SS_residuals
    MS_explained = SS_explained/k
    MS_residuals = SS_residuals/(n-k-1)
    F = MS_explained/MS_residuals

    # t test on slopes of individual parameters (testing whether each is different from 0)
    se_scaled = numpy.sqrt(numpy.diag(numpy.linalg.inv(A.T.dot(A))))
    se_beta = se_scaled[:]*numpy.sqrt(MS_residuals)
    t = beta/se_beta
    P = scipy.stats.t.cdf(abs(t), n-k-1)
    p = 2*(1-P)

    if verbose:
        print('-' * 80)
        print('Multiple Linear Regression model fit: R2 = %.5f, F = %.5g' % (R2, F))
        print('Regression coefficients:')
        for curname, curbeta, curse_beta, curt, curp in sorted(zip(names, beta, se_beta, t, p), key=lambda x: -abs(x[1])):
            print('- %s: beta = %.5g (s.e. %.5g), non-zero with p = %.5f (t = %.5g)' % (curname, curbeta, curse_beta, curp, curt))
        print('-' * 80)

    return beta, se_beta, t, p, R2, F

