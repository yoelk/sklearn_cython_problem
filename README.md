#Steps for reproducing:

- Create a new venv (e.g. feature_union):

    $ mkvirtualenv feature_union
    
- Install the requirements

    $ cd <CLONE_DIR>/feature_union
    $ pip install -r requirements.txt
    
- Create the wheel and install it to the venv

    $ python setup.py bdist_wheel
    $ pip install -I dist/<THE WHEEL'S NAME>.whl
    
- Run the test code:

    $ python run_cython_test.py
    

You should see the following error, which doesn't happen if you run the test code normally (without cythonization):
```
Traceback (most recent call last):
  File "run_cython_test.py", line 16, in <module>
    sys.exit(main())
  File "src/feature_union/cli.py", line 99, in feature_union.cli.main (build/src/feature_union/cli.c:2626)
    combined_features = FeatureListUnion([("pca", pca), ("univ_select", selection)])
  File "src/feature_union/cli.py", line 26, in feature_union.cli.FeatureListUnion.__init__ (build/src/feature_union/cli.c:1237)
    super(FeatureListUnion, self).__init__(transformer_list, **kwargs)
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/pipeline.py", line 630, in __init__
    self._validate_transformers()
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/pipeline.py", line 664, in _validate_transformers
    self._validate_names(names)
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/utils/metaestimators.py", line 65, in _validate_names
    invalid_names = set(names).intersection(self.get_params(deep=False))
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/pipeline.py", line 646, in get_params
    return self._get_params('transformer_list', deep=deep)
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/utils/metaestimators.py", line 26, in _get_params
    out = super(_BaseComposition, self).get_params(deep=False)
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/base.py", line 227, in get_params
    for key in self._get_param_names():
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/base.py", line 197, in _get_param_names
    init_signature = signature(init)
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/externals/funcsigs.py", line 59, in signature
    sig = signature(obj.__func__)
  File "/home/joel/.virtualenvs/feature_union/local/lib/python2.7/site-packages/sklearn/externals/funcsigs.py", line 173, in signature
    raise ValueError('callable {0!r} is not supported by signature'.format(obj))
ValueError: callable <cyfunction FeatureListUnion.__init__ at 0x7f14db64f410> is not supported by signature
```

#Steps for running without cythonization:

- Work on the virtualenv

    $ workon feature_union
    
- Run the code directly:

    $ python src/feature_union/cli.py

