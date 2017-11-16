from __future__ import print_function

import numpy as np

from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest


class FeatureListUnion(FeatureUnion, TransformerMixin):
    """
    Class for a registration pipeline, to merging the extracted keypoints and
    descriptors of the input images.
    """

    def __init__(self, transformer_list, **kwargs):
        """
        :param transformer_list: List of transformer objects to be applied to
                                 the data. The first half of each tuple is the
                                 name of the transformer
        """
        super(FeatureListUnion, self).__init__(transformer_list, **kwargs)

    def fit_transform(self, X, y=None, **fit_params):
        """Fit all transformers, transform the data and lists results.
        Parameters
        ----------
        X : iterable or array-like, depending on transformers
            Input data to be transformed.
        y : array-like, shape (n_samples, ...), optional
            Targets for supervised learning.
        Returns
        -------
        result: list of tuples (keypoints, descriptors).
        """
        self._validate_transformers()

        result = []
        for name, transformer in self.transformer_list:
            if hasattr(transformer, 'fit_transform'):
                res = transformer.fit_transform(X, y, **fit_params)
            else:
                res = transformer.fit(X, y, **fit_params).transform(X)

            result.append(res)

        return np.asarray(result)

    def transform(self, X):
        """Transform X separately by each transformer, lists results.
        Parameters
        ----------
        X : iterable or array-like, depending on transformers
            Input data to be transformed.
        Returns
        -------
        result: list of tuples (keypoints, descriptors).
        """
        result = []
        for name, transformer in self.transformer_list:
            result.append(transformer.transform(X))

        return result

    @property
    def result(self):
        result = []
        for name, transformer in self.transformer_list:
            if isinstance(transformer, TransformerMixin):
                if transformer.result:
                    result.append(transformer.result)
            elif isinstance(transformer, Pipeline):
                for sub_transformer in transformer.named_steps.itervalues():
                    if sub_transformer.result:
                        result.append(sub_transformer.result)
            else:
                raise Exception("Not familiar transformer type!")

        return result


def main(*argv):
    iris = load_iris()

    X_main, y_main = iris.data, iris.target

    # This dataset is way too high-dimensional. Better do PCA:
    pca = PCA(n_components=2)

    # Maybe some original features where good, too?
    selection = SelectKBest(k=1)

    # Build estimator from PCA and Univariate selection:

    combined_features = FeatureListUnion([("pca", pca), ("univ_select", selection)])

    # Use combined features to transform dataset:
    X_features = combined_features.fit(X_main, y_main).transform(X_main)

    # svm = SVC(kernel="linear")
    #
    # # Do grid search over k, n_components and C:
    #
    # pipeline = Pipeline([("features", combined_features), ("svm", svm)])
    #
    # param_grid = dict(features__pca__n_components=[1, 2, 3],
    #                   features__univ_select__k=[1, 2],
    #                   svm__C=[0.1, 1, 10])
    #
    # grid_search = GridSearchCV(pipeline, param_grid=param_grid, verbose=10)
    # grid_search.fit(X_main, y_main)
    # print(grid_search.best_estimator_)

    print('TEST PASSED')
    return 0

if __name__ == "__main__":
    main()