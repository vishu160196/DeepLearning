from sklearn import svm
import apk_image as converter

data, labels=converter.convert()



train_data=data[:n, :]
train_labels=labels[:n, :]

test_data=data[n:, :]
test_labels=labels[n:, :]

X = train_data
y = train_labels
clf = svm.SVC()
clf.fit(X, y)

res=clf.predict(test_data)