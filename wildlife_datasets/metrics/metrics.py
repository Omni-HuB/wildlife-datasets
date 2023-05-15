import numpy as np
import sklearn.metrics as skm
from typing import List, Tuple, Union

# TODO: add documentation
# TODO: check all code

def unify_types(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str],
    ) -> Tuple[List, List, Union[int, str]]:
    """Unifies label types.

    If `new_class` is string and labels integers (or the other way round),
    it converts them to integers to allow to us numpy arrays.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Unified label types.
    """

    y_all = list(set(y_true).union(set(y_pred)) - set([new_class]))        
    y_types = set([type(y) for y in y_all])
    if len(y_types) > 1:
        raise(Exception('Labels have mixed types. Convert all to int or str.'))
    if str in y_types and isinstance(new_class, int):
        encoder = {new_class: new_class}
        for i, y in enumerate(y_all):
            encoder[y] = new_class + 1 + i
        y_true = [encoder[y] for y in y_true]
        y_pred = [encoder[y] for y in y_pred]
    if int in y_types and isinstance(new_class, str):
        encoder = {new_class: np.min(y_all) - 1}
        for i, y in enumerate(y_all):
            encoder[y] = y
        y_true = [encoder[y] for y in y_true]
        y_pred = [encoder[y] for y in y_pred]
        new_class = encoder[new_class]
    return y_true, y_pred, new_class


def accuracy(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str] = None,
    ) -> float:
    """Computes the accuracy.

    If `new_class` is specified, it handles it as a additional class.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Computed accuracy.
    """

    y_true, y_pred, new_class = unify_types(y_true, y_pred, new_class)
    return np.mean(np.array(y_pred) == np.array(y_true))

def balanced_accuracy(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str] = None,
    ) -> float:
    """Computes the balanced accuracy.

    If `new_class` is specified, it handles it as a additional class.
    Each class has the same weight irregardless of the number of samples.
    If equals to macro recall unless there are predictions
    contain classes not in the true labels.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Computed balanced accuracy.
    """

    y_true, y_pred, new_class = unify_types(y_true, y_pred, new_class)    
    C = skm.confusion_matrix(y_true, y_pred)
    with np.errstate(divide="ignore", invalid="ignore"):
        per_class = np.diag(C) / C.sum(axis=1)
    return np.mean(per_class[~np.isnan(per_class)])

def class_average_accuracy(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str] = None,
    ) -> float:
    """Computes the class average accuracy.

    If `new_class` is specified, it handles it as a additional class.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Computed class average accuracy.
    """
    
    y_true, y_pred, new_class = unify_types(y_true, y_pred, new_class)
    C = skm.multilabel_confusion_matrix(y_true, y_pred)
    return np.mean([C_i[0,0]+C_i[1,1] for C_i in C]) / np.sum(C[0])

def precision(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str] = None,
    ) -> float:
    """Computes the (macro-averaged) precision.

    If `new_class` is specified, it handles it as a additional class.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Computed precision.
    """

    y_true, y_pred, new_class = unify_types(y_true, y_pred, new_class)
    return skm.precision_score(y_true, y_pred, average='macro')

def recall(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str] = None,
        ignore_empty: bool = False
    ) -> float:
    """Computes the (macro-averaged) recall.

    If `new_class` is specified, it handles it as a additional class.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.
        ignore_empty (bool): Whether classes not in true labels should be ignored for averaging.

    Returns:
        Computed recall.
    """

    y_true, y_pred, new_class = unify_types(y_true, y_pred, new_class)
    if ignore_empty:
        C = skm.multilabel_confusion_matrix(y_true, y_pred)
        return np.mean([C_i[1,1]/(C_i[1,0]+C_i[1,1]) for C_i in C if C_i[1,0]+C_i[1,1] > 0])
    else:
        return skm.recall_score(y_true, y_pred, average='macro')

def f1(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str] = None,
    ) -> float:
    """Computes the (macro-averaged) F1 score.

    If `new_class` is specified, it handles it as a additional class.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Computed F1 score.
    """

    y_true, y_pred, new_class = unify_types(y_true, y_pred, new_class)
    return skm.f1_score(y_true, y_pred, average='macro')

def accuracy_known_samples(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str],
    ) -> float:
    """Computes the accuracy on known samples.

    Samples of new (unknown) class are ignored.
    Returns `np.nan` if there are no known samples.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Computed accuracy on known samples.
    """

    y_true, y_pred, new_class = unify_types(y_true, y_pred, new_class)
    y_true = np.array(y_true)    
    y_pred = np.array(y_pred)
    known = y_true != new_class
    if sum(known) > 0:
        return np.mean(y_true[known] == y_pred[known])
    else:
        return np.nan

def accuracy_unknown_samples(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str],
    ) -> float:
    """Computes the accuracy on new (unknown) samples.

    Samples of known classes are ignored.
    Returns `np.nan` if there are no unknown samples.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Computed accuracy on unknown samples.
    """

    y_true, y_pred, new_class = unify_types(y_true, y_pred, new_class)
    y_true = np.array(y_true)    
    y_pred = np.array(y_pred)
    unknown = y_true == new_class
    if sum(unknown) > 0:
        return np.mean(y_true[unknown] == y_pred[unknown])
    else:
        return np.nan
    
def normalized_accuracy(
        y_true: List,
        y_pred: List,
        new_class: Union[int, str],
        mu: float
    ) -> float:
    """Computes the normalized accuracy.

    It is mu*accuracy on known samples + (1-mu)*accuracy on unknown samples.
    Returns `np.nan` if there are no known samples or no unknown samples.

    Args:
        y_true (List): List of true labels.
        y_pred (List): List of predictions.
        new_class (Union[int, str]): Name of the new class.
        mu (float): Coefficient of the convex combination.

    Returns:
        Computed normalized accuracy.
    """

    aks = accuracy_known_samples(y_true, y_pred, new_class)
    aus = accuracy_unknown_samples(y_true, y_pred, new_class)
    return mu*aks + (1-mu)*aus

def average_precision(
        y_true: Union[int, str],
        y_pred: List
    ) -> float:
    """Computes the average precision (for one sample).

    It computes AP@K, where K is the length of `y_pred`.

    Args:
        y_true (Union[int, str]): The true label.
        y_pred (List): Ranked predictions. First elements have a better rank.

    Returns:
        Computed average precision.
    """

    unify_types([y_true], y_pred, None)
    a = np.array(y_pred) == y_true
    b = np.linspace(1, 0, len(y_pred))
    if sum(a) == 0:
        return 0
    else:
        return skm.average_precision_score(a, b)

def mean_average_precision(
        y_true: List,
        y_pred: List[List]
    ):
    """Computes the mean average precision (for multiple samples).

    It computes MAP@K, where K is the length of `y_pred[0]`.

    Args:
        y_true (List): List of true labels.
        y_pred (List[List]): List of ranked predictions. First elements have a better rank.

    Returns:
        Computed mean average precision.
    """

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean([average_precision(y_t, y_p) for y_t, y_p in zip(y_true, y_pred)])

def auc_roc_new_class(
        y_true: List,
        y_score: List,
        new_class: Union[int, str],
    ) -> float:
    """Computes the area under ROC curve for detecting new individuals.

    High score suggests known individual.
    Low score suggests new (unknown) individual.
    It converts the problem to binary (is it new individual or not)
    and computes AUC for it.

    Args:
        y_true (List): List of true labels.
        y_score (List): List of scores.
        new_class (Union[int, str]): Name of the new class.

    Returns:
        Computed arena under ROC curve.
    """

    y_true, _, new_class = unify_types(y_true, [], new_class)    
    a = np.array(y_true) == new_class
    b = -np.array(y_score)
    return skm.roc_auc_score(a, b)
