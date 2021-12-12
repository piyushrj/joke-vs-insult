import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

# load the data
df = pd.read_csv("data/data.csv")
X = df['doc']
y = df['class']

# split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=21)

# model pipeline
pipe_knn = Pipeline([['tfidf', TfidfVectorizer()], ['knn', KNeighborsClassifier()]])

# use grid search to find the optimal number of neighbours
param_range = [2,3,4,5,6,7]
params = {'knn__n_neighbors': param_range}
grid_knn = GridSearchCV(estimator = pipe_knn, 
                    param_grid = params,
                    cv=10,
                    scoring='f1')
grid_knn.fit(X_train, y_train)

# model with optimal parameters
model = grid_knn.best_estimator_

# check model's performance of the test set
y_pred = model.predict(X_test)
clf_report = classification_report(y_test, y_pred)
print(clf_report)
with open("model_performance_report.txt", "w") as text_file:
    text_file.write(clf_report)

# save the model for later use
with open('knn_model.pkl', 'wb') as file:
    pickle.dump(model, file)

