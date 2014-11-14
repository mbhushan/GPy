# Copyright (c) 2013, Ricardo Andrade
# Copyright (c) 2013, the GPy Authors (see AUTHORS.txt)
# Licensed under the BSD 3-clause license (see LICENSE.txt)

from ..core import GP
from .. import likelihoods
from .. import kern
from ..inference.latent_function_inference.expectation_propagation import EP

class OneVsAllClassification(GP):
    """
    Gaussian Process classification: One vs all

    This is a thin wrapper around the models.GPClassification class, with a set of sensible defaults

    :param X: input observations
    :param Y: observed values, can be None if likelihood is not None
    :param kernel: a GPy kernel, defaults to rbf

    .. Note:: Multiple independent outputs are not allowed

    """

    def __init__(self, X, Y, kernel=None,Y_metadata=None):
        if kernel is None:
            kernel = kern.RBF(X.shape[1])

        likelihood = likelihoods.Bernoulli()

        assert Y.shape[1] == 1, 'Y should be 1 column vector'

        labels = np.unique(Y.flatten())

        self.predictions = {}
        for yj in labels:
            Ynew = Y.copy()
            Ynew[Y.flatten()!=yj] = 0
            Ynew[Y.flatten()==yj] = 1

            m = GPy.models.GPClassification(X,Ynew,kernel=kernel,Y_metadata=Y_metadata,inference_method=inference_method)
            m.optimize()
            self.predictions[yj] = m.predict(X)
