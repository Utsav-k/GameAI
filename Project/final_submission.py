import gym
import random
import numpy as np

import tflearn

from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter

import csv

LR = 1e-3
env = gym.make('CartPole-v0')
env.reset()
goal_steps = 400

score_requirement = 50
initial_games = 10000


def writeToCsv(msg):
    row = [ msg ]
    with open('AfterTrainingScores.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()



def randomGame():
	for episode in range(5):
		env.reset()
		for t in range(goal_steps):
			env.render()
			action = env.action_space.sample()
			observation, reward, done, info = env.step(action)
			if done:
				break



# randomGame()
def initialPopulation():
	training_data = []
	scores = []
	accepted_scores = []
	for _ in range(initial_games):
		score = 0
		env.reset()
		game_memory = []
		prev_observation = []
		for _ in range(goal_steps):
			# env.render()
			action = random.randrange(0,2)
			observation, reward, done, info = env.step(action)

			if len(prev_observation)>0:
				game_memory.append([prev_observation, action])
			prev_observation = observation

			score += reward
			if done:
				break

		if score>= score_requirement:
			accepted_scores.append(score)
			for data in game_memory:
				if data[1] == 1:
					output = [0,1]
				elif data[1] == 0:
					output = [1,0]

				training_data.append([data[0],output])
		env.reset()
		writeToCsv(score)
		scores.append(score)


	training_data_save = np.array(training_data)
	np.save('saved.np', training_data_save)
	print('Average accepted score:', mean(accepted_scores))
	print('Median accepted score:', median(accepted_scores))
	print(Counter(accepted_scores))
	return training_data





def neuralNetworkModel(input_size):
	network = input_data(shape = [None, input_size, 1], name = 'input')

	network = fully_connected(network, 128, activation='relu')
	network = dropout(network,0.8)    # keep rate in the second argument

	network = fully_connected(network, 256, activation='relu')
	network = dropout(network,0.8)    # keep rate in the second argument


	network = fully_connected(network, 512, activation='relu')
	network = dropout(network,0.8)    # keep rate in the second argument

	network = fully_connected(network, 256, activation='relu')
	network = dropout(network,0.8)    # keep rate in the second argument

	network = fully_connected(network, 128, activation='relu')
	network = dropout(network,0.8)    # keep rate in the second argument

	network = fully_connected(network,2,activation='softmax')

	network = regression(network, optimizer='adam', learning_rate=LR,
						loss='categorical_crossentropy', name='targets')


	model = tflearn.DNN(network,tensorboard_dir='log')

	return model

def trainModel(training_data, model=False):
	
	X = np.array( [i[0] for i in training_data] ).reshape(-1, len(training_data[0][0]), 1)
	Y = [i[1] for i in training_data]

	if not model:
		model = neuralNetworkModel(input_size=len(X[0]))

	model.fit({'input':X}, {'targets':Y}, n_epoch=3, snapshot_step=500, show_metric=True,
				run_id='OpenAI')

	return model

training_data =  initialPopulation()

model = trainModel(training_data)


scores = []
choices =[]
writeToCsv("Scores After Training: ")

for each_game in range(10):

	score = 0
	game_memory = []
	prev_obs = []
	env.reset()

	for _ in range(goal_steps):
		
		env.render()

		if len(prev_obs) == 0:
			action = random.randrange(0,2)
		else:
			action = np.argmax(model.predict(prev_obs.reshape(-1, len(prev_obs), 1)) [0])

		choices.append(action)

		new_observation, reward, done, info = env.step(action)
		prev_obs = new_observation
		game_memory.append([new_observation,action])
		score+=reward
		
		if done:
			break
	
	writeToCsv(score)
	scores.append(score)


print('Average Score', sum(scores)/len(scores))
print('Choice 1: {}, Choice 0: {}'.format(choices.count(1)/len(choices),
		choices.count(0)/len(choices)))


