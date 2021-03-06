#German
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.model_selection import train_test_split

from amce import AMCE
from prepare_dataset import *

def main():
    # Read Dataset German
    df = prepare_german_dataset("german_credit.csv", "./German/")

    #Get the input features
    columns = df.columns
    class_name = 'default' # default = 0 = "Good class" / default = 1 = "Bad class" 
    columns_tmp = list(columns)
    columns_tmp.remove(class_name)

    x_train, x_test, y_train, y_test = train_test_split(df[columns_tmp], df[class_name], test_size=0.1)

    model = RandomForestClassifier(n_estimators = 120, n_jobs=-1, random_state=0)  
    model.fit(x_train, y_train)

    p = model.predict(x_test)

    print(classification_report(y_test, p))

    #-------Begin Parameter Adjustment--------
    
    algorithm = 'Tree' #The current version of the method uses the Shap TreeExplainer for tree models and the KernelExplainer for all other algorithms
    X = 0 #Indicates the instance's position to be explained in the dataset

    #User preferences
    static_list = [] #List of features that cannot be changed. For example: static_list = ['age']
    K = 3 #Number of counterfactual explanations to be obtained

    #Genetic Algorithm parameters
    num_gen = 30 #number of generations
    pop_size = 100 #population size
    per_elit = 0.1 #percentage of elitism
    cros_proba = 0.8 #crossover probability
    mutation_proba = 0.1 #mutation probability

    #Weights of objective function metrics
    L1 = 1 #lambda 1 - Weight related to distance for class of interest
    L2 = 1 #lambda 2 - Weight related to distance for original instance
    L3 = 1 #lambda 3 - Weight related to the amount of changes to generate the counterfactual

    #copy the original instance
    original_instance = x_test.iloc[X].copy() 

    #-------End Parameter Adjustment--------

    print('Original instance - Class ' + str(p[X]) + '\n')
    print(original_instance)
    print('\nGetting counterfactuals...\n')
            
    #Run AMCE
    explainerAMCE = AMCE(original_instance, p[X], static_list, K, df[columns_tmp], x_train, model, num_gen, pop_size, per_elit, cros_proba, mutation_proba, L1, L2, L3, algorithm)
    
    contrafactual_set, solution = explainerAMCE.explain() #Method returns the list of counterfactuals and the explanations generated from them
    
    #The method returns a list of counterfactual solutions, where each solution, in turn, is a change list (each change has the "column" and "value" to be changed). To implement another output format, see the "printResults" function
    explainerAMCE.printResults(solution)

if __name__ == "__main__":
    main()