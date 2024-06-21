# Evaluation

## Evaluation Baseline

Baseline = Most and least Popular

- [eval_most_popular](./eval_most_popular.ipynb)

### Results

Anzahl Recommendations: 65

- **Precision**: 0.0014736855769637218
- **Recall**: 0.01508688529585272
- **nDCG**: 0.2610353210675939

# Evaluation Faktorisierungsmaschine

- [evaluation_all](./evaluation.ipynb)
- [eval_ranmetrik](./rankmetric_fm.ipynb)

### Results

Anzahl Recommendations: 10 per User (because of performance issues - takes too much time)  
Available users and books can be found in [known_users](./known_users), [users](./users) and [books](./books)

- **Precision**: 0.0262411855626625
- **Recall**: 0.019863213285777084
- **nDCG**: 0.41146381789729336
- **Hit Rate**: 0.16548891382672223
- **RMSE**:
  - not done because we do not predict rating values
  - the FM recommends items directly with intern real value scores which have nothing to do with the values from the rating set
  - as RankFM aims to optimize ranks of the items in the recommendation list, we decided to use a Rankmetric (nDCG) to measure the performance

### Result Log

```
user f age, country
item f age
rating / 10 als weight
0er und avg+ ratings

precision:  0.013470196290293534
recall:     0.011826408493971203
```

```
user f age, country
item f age
no weight
0er und avg+ ratings

precision:  0.015685215198991537
recall:     0.02015197914663626
```

```
user f age, country
no item f
no weight
0er und avg+ ratings

precision: 0.01559517377993877
recall: 0.020342086518964825
```

```
user f age, country
with item f
no weight
avg+ ratings

precision: 0.008052276559865094
recall: 0.017104661404281886
```

```
no user f age, country
no item f
no weight
avg+ ratings

precision: 0.00851602023608769
recall: 0.01837799664369502
```

```
no user f age, country
no item f
with binary weight
all cleaned ratings

precision: 0.017743919251920894
recall: 0.02208053985730808
```

```
user f: age, country
item f: age in months, tags
with binary weight
all cleaned ratings

precision: 0.02490240841697551
recall: 0.025399523273584326
```

```4-KFold
user f: age, country
item f: age in months, tags
with binary weight
all cleaned ratings

precision: 0.02505245972073694
recall: 0.017487273512267913
```

```4-KFold
user f: age, country
item f: age in months, tags
with weights [0-2]
all cleaned ratings

precision: 0.0262411855626625
recall: 0.019863213285777084
nDCG: 0.41146381789729336
hit rate: 0.16548891382672223
```
