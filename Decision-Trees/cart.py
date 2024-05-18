import csv
from collections import defaultdict
from math import log
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
from sklearn.utils import resample
import matplotlib.pyplot as plt


class DecisionTree:
    def __init__(self, col=-1, value=None, trueBranch=None, falseBranch=None, results=None, summary=None):
        self.col = col
        self.value = value
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch
        self.results = results 
        self.summary = summary


def bootstrap(data, target, n):
    data = data.to_numpy()
    target = target.to_numpy()
    accuracies = []
    for j in range(n):
        trainingData, y_train = resample(data, target, n_samples=200)
        testData, y_test = resample(data, target, n_samples=67)
        
        
        trainingData = pd.concat([pd.DataFrame(trainingData), pd.DataFrame(y_train, columns=['target'])], axis=1)
        testData = pd.concat([pd.DataFrame(testData), pd.DataFrame(y_test, columns=['target'])], axis=1)
        
        decisionTree = growTree(trainingData.values, evaluationFunction=gini)
        prune(decisionTree, 0.8, notify=True)
        
        count = 0
        count1 = 0
        true = []
        pred = []
        
        for i in range(len(testData)):
            count1 += 1
            t = classify(testData.iloc[i, :-1].values, decisionTree)
            for key, value in t.items():
                pred.append(key)
                true.append(y_test[i])
                if key == y_test[i]:
                    count += 1
        accuracies.append(count / count1)
        
        print("\nPredictive accuracy for Bootstrap = ", j + 1, " is ", count / count1)
        print(confusion_matrix(true, pred))
        a, b, c, d = precision_recall_fscore_support(true, pred, average='macro')
        print("Precision = ", a, "\nRecall = ", b, "\nF1-score = ", c)
    # Vẽ biểu đồ cho độ chính xác của 10 lần thử nghiệm
    plt.plot(range(1, n+1), accuracies, marker='o')
    plt.title('Accuracy for each Bootstrap')
    plt.xlabel('Bootstrap iteration')
    plt.ylabel('Accuracy')
    plt.xticks(range(1, n+1))
    plt.grid(True)
    plt.show()


def Unique_Counts(rows):
    results_ = {}
    for row in rows:
        r = row[-1]
        if r not in results_: results_[r] = 0
        results_[r] += 1
    return results_


def entropy(rows):
    log2 = lambda x: log(x) / log(2)
    results_ = Unique_Counts(rows)
    entropy_value = 0.0
    for r in results_:
        prob = float(results_[r]) / len(rows)
        entropy_value -= prob * log2(prob)
    return entropy_value


def divideSet(trows, column_, val):
    splitFn = None
    if isinstance(val, int) or isinstance(val, float): 
        splitFn = lambda row: row[column_] >= val
    else: 
        splitFn = lambda row: row[column_] == val

    lista = [row for row in trows if splitFn(row)]
    listb = [row for row in trows if not splitFn(row)]
    return (lista, listb)


def gini(trows):
    total = len(trows)
    count = Unique_Counts(trows)
    imp_val = 0.0

    for ka in count:
        pa = float(count[ka]) / total

        for kb in count:
            if ka == kb: continue
            pb = float(count[kb]) / total
            imp_val += (pa * pb)

    return imp_val


def growTree(rows, evaluationFunction=entropy):
    if len(rows) == 0: return DecisionTree()
    currScore = evaluationFunction(rows)

    gain_best = 0.0
    bestAttribute = None
    bestSets = None

    columnCount = len(rows[0]) - 1  
    for col_ in range(0, columnCount):
        columnValues = [row_[col_] for row_ in rows]
        lsUnique = list(set(columnValues))

        for value in lsUnique:
            (seta, setb) = divideSet(rows, col_, value)

            prob = float(len(seta)) / len(rows)
            gain = currScore - prob * evaluationFunction(seta) - (1 - prob) * evaluationFunction(setb)
            if gain > gain_best and len(seta) > 0 and len(setb) > 0:
                gain_best = gain
                bestAttribute = (col_, value)
                bestSets = (seta, setb)

    dcY = {'impurity': '%.3f' % currScore, 'samples': '%d' % len(rows)}
    if gain_best > 0:
        trueBranch = growTree(bestSets[0], evaluationFunction)
        falseBranch = growTree(bestSets[1], evaluationFunction)
        return DecisionTree(col=bestAttribute[0], value=bestAttribute[1], trueBranch=trueBranch,
                            falseBranch=falseBranch, summary=dcY)
    else:
        return DecisionTree(results=Unique_Counts(rows), summary=dcY)


def prune(tree, minGain, evaluationFunction=entropy, notify=False):
    if tree.trueBranch.results is None: prune(tree.trueBranch, minGain, evaluationFunction, notify)
    if tree.falseBranch.results is None: prune(tree.falseBranch, minGain, evaluationFunction, notify)

    if tree.trueBranch.results is not None and tree.falseBranch.results is not None:
        ta, fa = [], []

        for v_, c_ in tree.trueBranch.results.items(): ta += [[v_]] * c_
        for v_, c_ in tree.falseBranch.results.items(): fa += [[v_]] * c_

        prob = float(len(ta)) / len(ta + fa)
        delta_val = evaluationFunction(ta + fa) - prob * evaluationFunction(ta) - (1 - prob) * evaluationFunction(fa)
        if delta_val < minGain:
            tree.trueBranch, tree.falseBranch = None, None
            tree.results = Unique_Counts(ta + fa)


def classify(obs, tree):
    def classify_(obs, tree):
        if tree.results is not None:  
            return tree.results
        else:
            val = obs[tree.col]
            branch_ = None
            if isinstance(val, int) or isinstance(val, float):
                if val >= tree.value: branch_ = tree.trueBranch
                else: branch_ = tree.falseBranch
            else:
                if val == tree.value: branch_ = tree.trueBranch
                else: branch_ = tree.falseBranch
        return classify_(obs, branch_)

    return classify_(obs, tree)


if __name__ == '__main__':
    # Read dataset
    data = pd.read_csv("dt_data.csv")

    # Assuming the second column is 'Rank' and columns 'Q1'-'Q9' are the features
    target = data.iloc[:, 1]
    features = data.iloc[:, 2:11]

    print(features)
    
    # Perform bootstrap method
    bootstrap(features, target, 50)
