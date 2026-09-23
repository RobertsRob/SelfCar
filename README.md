# SelfCar
This is a project where Neural network learns how to traverse optimally in the given track.
But there are some limitations to make task harder:
- car for steering can use only three sensors - front, right and left
- car cannot leave the track - cross white line
- task is to ride as fast and optimally as possible

## How it works?
Each generations there are created N amount of cars and in the end of completing 3 laps or every car crashed into a wall the best one is choosen (car which has most amount of points).
From that best_car is created next generation, making similar models, and choosing the best again. That repeats itself and better and better models are created.

## How best car is choosen?
As I mentioned each generation best car is choosen. And it is choosen based on amount of points (higher ->  better). So how do cars loose and get points:
- +1 point when car croses a checkpoint (dim greenlines all across the track)
- +n point are given when lap is finished (less time it took -> better score, technically its not time but amount of updates that has been made)
- -10 point if crashed (also stops model from continuing race in current generatons)

# How to run this project?
There are two ways to run this project:

## First option (recomended):
Just run this python app. As simple as it sound for this project is not that simple. The thing is that to run this project you need to have pyTorch installed. And its pretty heave. You can choose whether you want cuda coresor cpu calculations, but it is still pretty big.
1. You need to have python installed
2. Install all required libraries: pytorch, numpy and pygame (more details in requirements.txt)
3. Run main.py
Enjoy app.

## Second option 