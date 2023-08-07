import skopt
from evaluate import train_evaluate

#'epochs': 4,   #done
#    'batch_size': 1, #done
#    'look_back': 252, #done
#    'lstm_layers':1, #done
#    'lstm_neurons':1, #done
#    'dense_layers':1,  #more layers can improve overall accuracy. Can lead to overfitting so needs to be controlled #done
#    'dense_neurons':1, #same for more nodes. Can also lead to overfitting so need to be controlled #done
#    'dropout':0.0

SPACE = [
    skopt.space.Integer(1, 10, name='epochs'),
    skopt.space.Integer(0, 5, name='lstm_layers'),
    skopt.space.Integer(1, 128, name='lstm_neurons'),
    skopt.space.Integer(0, 5, name='dense_layers'),
    skopt.space.Integer(1, 32, name='dense_neurons'),
    skopt.space.Integer(32, 128, name='batch_size'),
    skopt.space.Integer(91, 833, name='look_back'),
    skopt.space.Real(0.0, 0.5, name='dropout'),    
]

@skopt.utils.use_named_args(SPACE)
def objective(**params):
    return train_evaluate(params)
results = skopt.forest_minimize(objective, SPACE, n_calls=30, n_random_starts=10)
best_auc = results.fun
best_params = results.x

print('best result: ', best_auc)
print('best parameters: ', best_params)
