# SVM Novelty Detection

## Requirements. Setup
* Please download in the same place as the notebook https://drive.google.com/file/d/1lwktG1FbJLjKpiPs-VpC4DuofmKtJcyv/view?usp=sharing. This is a data file.
* Please go to the command prompt and **pip install cvxopt**	
* If you use Jupyter Notebook, I recommend you not to run all the cells(I highlighted when) because it might take a lot of time and you will not be able to finish in 1h. Instead if you work in GoogleColab you can run.

## Files
* Main notebook "One_Class_SVM_Novelty_Detection.ipynb"
* Images

## About
The present work is as an attempt to provide an algorithm which is in line
with Vapnik's principle never to solve a problem which is more general than the one that
one is actually interested in. E.g., in situations where one is only interested in detecting
novelty, it is not always necessary to estimate a full density model of the data. Indeed,
density estimation is more difficult than what we are doing, in several respects.
Therefore we need to restrict ourselves to making
a statement about the measure of some sets. Given a small class of sets, the simplest estimator
accomplishing this task is the empirical measure, which simply looks at how many
training points fall into the region of interest. **This algorithm does the opposite. It starts
with the number of training points that are supposed to fall into the region, and then estimates
a region with the desired property.**

## Compulsory
* Enjoy! 



