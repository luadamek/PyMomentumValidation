import os
import ROOT
import glob
from filelists import *
import numexpr as ne
import uproot as ur

#def f1(a, b) :
#a, b = 2 * a, 3 * b
#return ne.evaluate('2*a + 3*b + c',
#local_dict={'c' : np.arange(30, 40)})
#def calc_mass(pts, etas, phis, masses=0.0):
#    

def get_dataframe(root_file, start, stop,  variables, selection):
    #calculate what bin events belong in
    df = ur.open(root_file)["MuonMomentumCalibrationTree"].pandas.df(branches = variables, entrystart = start, entrystop = stop)
    if selection: df = df.query(selection) #apply the selection
    return df

import numpy as np
from numpy import array, average, dot

def cov(m, y=None, rowvar=True, bias=False, ddof=None, fweights=None,
        aweights=None):
    """
    Estimate a covariance matrix, given data and weights.
    Covariance indicates the level to which two variables vary together.
    If we examine N-dimensional samples, :math:`X = [x_1, x_2, ... x_N]^T`,
    then the covariance matrix element :math:`C_{ij}` is the covariance of
    :math:`x_i` and :math:`x_j`. The element :math:`C_{ii}` is the variance
    of :math:`x_i`.
    See the notes for an outline of the algorithm.
    Parameters
    ----------
    m : array_like
        A 1-D or 2-D array containing multiple variables and observations.
        Each row of `m` represents a variable, and each column a single
        observation of all those variables. Also see `rowvar` below.
    y : array_like, optional
        An additional set of variables and observations. `y` has the same form
        as that of `m`.
    rowvar : bool, optional
        If `rowvar` is True (default), then each row represents a
        variable, with observations in the columns. Otherwise, the relationship
        is transposed: each column represents a variable, while the rows
        contain observations.
    bias : bool, optional
        Default normalization (False) is by ``(N - 1)``, where ``N`` is the
        number of observations given (unbiased estimate). If `bias` is True,
        then normalization is by ``N``. These values can be overridden by using
        the keyword ``ddof`` in numpy versions >= 1.5.
    ddof : int, optional
        If not ``None`` the default value implied by `bias` is overridden.
        Note that ``ddof=1`` will return the unbiased estimate, even if both
        `fweights` and `aweights` are specified, and ``ddof=0`` will return
        the simple average. See the notes for the details. The default value
        is ``None``.
        .. versionadded:: 1.5
    fweights : array_like, int, optional
        1-D array of integer frequency weights; the number of times each
        observation vector should be repeated.
        .. versionadded:: 1.10
    aweights : array_like, optional
        1-D array of observation vector weights. These relative weights are
        typically large for observations considered "important" and smaller for
        observations considered less "important". If ``ddof=0`` the array of
        weights can be used to assign probabilities to observation vectors.
        .. versionadded:: 1.10
    Returns
    -------
    out : ndarray
        The covariance matrix of the variables.
    See Also
    --------
    corrcoef : Normalized covariance matrix
    Notes
    -----
    Assume that the observations are in the columns of the observation
    array `m` and let ``f = fweights`` and ``a = aweights`` for brevity. The
    steps to compute the weighted covariance are as follows::
        >>> m = np.arange(10, dtype=np.float64)
        >>> f = np.arange(10) * 2
        >>> a = np.arange(10) ** 2.
        >>> ddof = 1
        >>> w = f * a
        >>> v1 = np.sum(w)
        >>> v2 = np.sum(w * a)
        >>> m -= np.sum(m * w, axis=None, keepdims=True) / v1
        >>> cov = np.dot(m * w, m.T) * v1 / (v1**2 - ddof * v2)
    Note that when ``a == 1``, the normalization factor
    ``v1 / (v1**2 - ddof * v2)`` goes over to ``1 / (np.sum(f) - ddof)``
    as it should.
    Examples
    --------
    Consider two variables, :math:`x_0` and :math:`x_1`, which
    correlate perfectly, but in opposite directions:
    >>> x = np.array([[0, 2], [1, 1], [2, 0]]).T
    >>> x
    array([[0, 1, 2],
           [2, 1, 0]])
    Note how :math:`x_0` increases while :math:`x_1` decreases. The covariance
    matrix shows this clearly:
    >>> np.cov(x)
    array([[ 1., -1.],
           [-1.,  1.]])
    Note that element :math:`C_{0,1}`, which shows the correlation between
    :math:`x_0` and :math:`x_1`, is negative.
    Further, note how `x` and `y` are combined:
    >>> x = [-2.1, -1,  4.3]
    >>> y = [3,  1.1,  0.12]
    >>> X = np.stack((x, y), axis=0)
    >>> np.cov(X)
    array([[11.71      , -4.286     ], # may vary
           [-4.286     ,  2.144133]])
    >>> np.cov(x, y)
    array([[11.71      , -4.286     ], # may vary
           [-4.286     ,  2.144133]])
    >>> np.cov(x)
    array(11.71)
    """
    # Check inputs
    if ddof is not None and ddof != int(ddof):
        raise ValueError(
            "ddof must be integer")

    # Handles complex arrays too
    m = np.asarray(m)
    if m.ndim > 2:
        raise ValueError("m has more than 2 dimensions")

    if y is None:
        dtype = np.result_type(m, np.float64)
    else:
        y = np.asarray(y)
        if y.ndim > 2:
            raise ValueError("y has more than 2 dimensions")
        dtype = np.result_type(m, y, np.float64)

    X = array(m, ndmin=2, dtype=dtype)
    if not rowvar and X.shape[0] != 1:
        X = X.T
    if X.shape[0] == 0:
        return np.array([]).reshape(0, 0)
    if y is not None:
        y = array(y, copy=False, ndmin=2, dtype=dtype)
        if not rowvar and y.shape[0] != 1:
            y = y.T
        X = np.concatenate((X, y), axis=0)

    if ddof is None:
        if bias == 0:
            ddof = 1
        else:
            ddof = 0

    # Get the product of frequencies and weights
    w = None
    if fweights is not None:
        fweights = np.asarray(fweights, dtype=float)
        if not np.all(fweights == np.around(fweights)):
            raise TypeError(
                "fweights must be integer")
        if fweights.ndim > 1:
            raise RuntimeError(
                "cannot handle multidimensional fweights")
        if fweights.shape[0] != X.shape[1]:
            raise RuntimeError(
                "incompatible numbers of samples and fweights")
        if any(fweights < 0):
            raise ValueError(
                "fweights cannot be negative")
        w = fweights
    if aweights is not None:
        aweights = np.asarray(aweights, dtype=float)
        if aweights.ndim > 1:
            raise RuntimeError(
                "cannot handle multidimensional aweights")
        if aweights.shape[0] != X.shape[1]:
            raise RuntimeError(
                "incompatible numbers of samples and aweights")
        if w is None:
            w = aweights
        else:
            w *= aweights

    avg, w_sum = average(X, axis=1, weights=w, returned=True)
    w_sum = w_sum[0]

    # Determine the normalization
    if w is None:
        fact = X.shape[1] - ddof
    elif ddof == 0:
        fact = w_sum
    elif aweights is None:
        fact = w_sum - ddof
    else:
        fact = w_sum - ddof*sum(w*aweights)/w_sum

    if fact <= 0:
        warnings.warn("Degrees of freedom <= 0 for slice",
                      RuntimeWarning, stacklevel=3)
        fact = 0.0

    X -= avg[:, None]
    if w is None:
        X_T = X.T
    else:
        X_T = (X*w).T
    print("Dotting")
    c = dot(X, X_T.conj())
    c *= np.true_divide(1, fact)
    print("Done")
    return c.squeeze()


def glob_all_files(raw_files):
    import glob
    files = []
    for f in raw_files:
        if "*" in f: files += glob.glob(f)
        else: files.append(f)
    return files


def get_files(flavour):
    '''
    Get a list of files associated with a given type of file (e.g. the inclusive files on eos)
    '''
    assert flavour in directories
    assert flavour in files

    directory = directories[flavour]
    all_files = files[flavour]

    to_return = {}
    for key in all_files:
        to_return[key] =  glob_all_files([os.path.join(directory, f) for f in all_files[key]])

    return to_return


def draw_text(x, y, text, color=ROOT.kBlack, size=0.05):
    '''Draw text.
    Parameters
    ----------
    x : float
        x position in NDC coordinates
    y : float
        y position in NDC coordinates
    text : string, optional
        The text
    color : int, optional
        Text colour (the default is 1, i.e. black).
        See https://ROOT.cern.ch/doc/master/classTColor.html.
        If you know the hex code, rgb values, etc., use ``ROOT.TColor.GetColor()``
    size : float, optional
        Text size
        See https://ROOT.cern.ch/doc/master/classTLatex.html
    '''
    l = ROOT.TLatex()
    l.SetTextSize(size)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x, y, text)


def tchain_files_together(tree_name, channel_to_filelist, on_eos = False):
    '''
    Given a tree_name, and a dictionary of channel to file list, return a dictionary of channel to filename to tchain.
    '''
    trees = {}
    print("\n"*10)
    print("Chaining files together for {}".format(list(trees.keys())))
    for channel in channel_to_filelist:
        trees[channel] = {}
        files = channel_to_filelist[channel]

        print("For channel {}, found files {}".format(channel, files))
        trees[channel] = ROOT.TChain(tree_name)
        for f in files:
            #check if this file was a directory or a file
            if os.path.isfile(f):
                print("For channel {}, and file {}, found files {}".format(channel, f, f))
                if on_eos:
                    trees[channel].Add('root://eosatlas.cern.ch/' + f)
                else:
                    trees[channel].Add(f)

            else: #this was a directory
                #go and get all of the files in the directory
                if not on_eos:
                    wildcards = ["*.root", "*.root*"]
                    files = []
                    for wild_card in wildcards:
                        files += glob.glob(os.path.join(f, wild_card))
                    files = list(set(files))
                else:
                    from XRootD import client
                    from XRootD.client.flags import DirListFlags
                    xrootd_client = client.FileSystem('root://eosatlas.cern.ch')
                    files = [el.name for el in  xrootd_client.dirlist(f, DirListFlags.STAT)[1] if ".root" in os.path.split(el.name)[-1]]
                    files = [os.path.join(f, el) if f not in el else el for el in files]

                unique_files = []
                for file_with_path in files:
                    assert "//" not in file_with_path
                    print("Found file {}".format(file_with_path))
                    if on_eos:
                       trees[channel].Add('root://eosatlas.cern.ch/' + file_with_path)
                    else:
                       trees[channel].Add(file_with_path)
    print("Retrieved Trees")
    return trees

def generate_partitions(trees, NPartitions):
    '''
    generate a dictionary of channel to file to list of tuples with information about what events to read for each partition
    '''
    partitions = {}
    for channel in trees:
        assert channel not in partitions
        partitions[channel] = []
        tree = trees[channel] 
        entries = tree.GetEntries()
        #OK we need to create n event splits from 0 to entries
        step = int(float(entries)/float(NPartitions)) - 1 
        cuts = []
        #are there enough entires to warrant a split?
        if step > 50:
            cuts.append((0, step))
            while cuts[-1][-1] < entries:
                last_value = cuts[-1][-1]
                cuts.append( (last_value, last_value + step))
            cuts = cuts[:-2]
            cuts.append( (cuts[-1][-1], entries))
            assert len(cuts) == NPartitions
        else:
            cuts.append((0.0, entries))
            for i in range(1, NPartitions):
                cuts.append( (entries, entries) )
            print("Found partitions for channel {}, and file {}, and they were {}".format(channel, f, cuts))
        partitions[channel] = cuts

    print("Generated partitions")
    print(partitions)
    return partitions

import ROOT
def get_entry_steps(root_file, step_size = 10000, tree_name = "tree_incl_all"):
    tfile = ROOT.TFile(root_file, "READ")
    ttree = tfile.Get(tree_name)
    all_entries = ttree.GetEntries()
    last_entry = 0
    steps = []
    while last_entry < all_entries:
        steps.append((last_entry, last_entry + step_size))
        last_entry = steps[-1][-1]
    steps[-1] = (steps[-1][0], all_entries)
    return steps

def get_setup_commands():
    commands  = []
    commands.append("cd {}".format(os.getenv("MomentumValidationDir")))
    commands.append("export USER={}".format(os.getenv("USER")))
    commands.append("echo $PWD")
    commands.append("source ./setup.sh")
    return commands

