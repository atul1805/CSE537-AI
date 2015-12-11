# To run:  python NaiveBayes.py --trainData trainingimages.txt --trainLabel traininglabels.txt --testData testimages.txt --testLabel testlabels.txt
import argparse
import time
import math
from math import log

# Image Dimensions
imageWidth = 28
imageHeight = 28

# Num of labels(0,1,2,3,4,5,6,7,8,9)
numLabels = 10

# Num of Training images
numTraining = 5000

# Num of test images
numTest = 1000

# Num of values a feature can take(0,1,2,3,4,5,6,7)
numFeatureVal = 8


def main(args):
    tic = time.clock()
    # Get training features and labels
    trainFeatures = getFeatures(args.trainData)
    trainLabels = getLabels(args.trainLabel)

    # Start training
    (prior,likelihood) = train(trainFeatures,trainLabels)

    # Get test features and labels
    testFeatures = getFeatures(args.testData)
    testLabels = getLabels(args.testLabel)

    # Predict test labels
    predictedLabels = classify(testFeatures,prior,likelihood)

    printPerformance(predictedLabels,testLabels)

    toc = time.clock()
    timeItr = toc - tic
    print "Execution Time: " + str(timeItr)
    

# Function to train a Naive Bayes classifier for a given training data, returns prior and likelihood probabilities
def train(trainFeatures,trainLabels):

    # A 2D array storing counts for a particular feature value given a label
    featureImage = [[0 for a in range(numFeatureVal)] for a in range(imageWidth*imageHeight)]

    # A map from label to featureImage
    likelihood = dict()

    # A 1D array containing prior probablities of all the labels
    prior = [0 for x in range(numLabels)]
	
    # A 1D array containing counts of lables in the training data
    countLabels = [0 for x in range(numLabels)]
    for i in range(numTraining):
        countLabels[trainLabels[i]] += 1

    # Iterating over all the images in the datatset and getting count of feature value given a label
    for i in range(numTraining):
        label = trainLabels[i]
        image = trainFeatures[i]
        for j in range(imageWidth*imageHeight):
            featureVal = image[j]
            if label in likelihood:
                featureImage = likelihood[label]
                featureImage[j][featureVal] += 1
                likelihood[label] = featureImage
            else:
                featureImage = [[0 for a in range(numFeatureVal)] for a in range(imageWidth*imageHeight)]
                featureImage[j][featureVal] += 1
                likelihood[label] = featureImage

    # Smoothing parameter
    smoothing = 0.0001
    # Calculating log likelihood probablity with laplacian smoothing to take care of feature values and labels with zero count
    for label in range(numLabels):
        if label in likelihood:
            featureImage = likelihood[label]
        else:
            featureImage = [[0 for a in range(numFeatureVal)] for a in range(imageWidth*imageHeight)]
            countLabels[label] = 0
        for i in range(imageWidth*imageHeight):
            for j in range(numFeatureVal):
                # Laplacian smoothing
                featureImage[i][j] = log(featureImage[i][j] + smoothing) - log(countLabels[label] + smoothing*(imageWidth*imageHeight*numFeatureVal))
        likelihood[label] = featureImage

    # Calculating log prior probabilities of labels
    for i in range(numTraining):
        prior[trainLabels[i]] = log(countLabels[trainLabels[i]]) - log(numTraining)
    return (prior,likelihood)

# Function to classify a given test data and return predicted labels
def classify(testFeatures,prior,likelihood):
    # A 1D array storing the predicted labels
    predictedLabels = [0 for a in range(numTest)]

    # A 1D array to store probabilities of all 10 labels for a given image
    labelProb = [1 for a in range(numLabels)]

    # Iterate over all test images
    for i in range(numTest):
        image = testFeatures[i]
        for label in range(numLabels):
            # Prior probablity for a given label
            priorProb = prior[label]
            # likelihood probablity of feature values guven a label
            featureImage = likelihood[label]
            # Iterate over all feature values
            for j in range (imageWidth*imageHeight):
                featureVal = image[j]
                # Add the log likelihood probablities(Naive Bayes assumption)
                labelProb[label] += featureImage[j][featureVal]
            # Finally add the log prior probablity
            labelProb[label] += priorProb
        # Predicted label will be the label with greatest log probablity
        predictedLabels[i] = labelProb.index(max(labelProb))
        labelProb = [1 for a in range(numLabels)]
    return predictedLabels

def printPerformance(predictedLabels,testLabels):
    # A 1D array to store count of true+ve for the labels
    truePositive = [0 for x in range(numLabels)]

    # A 1D array to store total count of each label in test set
    totalTest = [0 for x in range(numLabels)]

    # A 1D array to store total count of each label in predicted set
    totalPredicted = [0 for x in range(numLabels)]

    success = 0
    confusionMatrix = [[0 for x in range(numLabels)] for x in range(numLabels)]
    for i in range(numTest):
        confusionMatrix[testLabels[i]][predictedLabels[i]] += 1
        if predictedLabels[i] == testLabels[i]:
            success += 1
            truePositive[predictedLabels[i]] += 1
        totalPredicted[predictedLabels[i]] += 1
        totalTest[testLabels[i]] += 1
    
    print "Accuracy: " + str(success*100/float(numTest)) + "%\n"
    print "ConfusionMatrix:"
    for i in range(numLabels):
        print "	",i,
    print "	R"
    print ""
    print ""
    for i in range(numLabels):
        print i,
        for j in range(numLabels):
            print "	",confusionMatrix[i][j],
        recall = truePositive[i]/float(totalTest[i])
        recall = "%.4f" % recall
        print "	",recall
    print "P",
    for i in range(numLabels):
        precision = truePositive[i]/float(totalPredicted[i])
        precision = "%.4f" % precision
        print "	",precision,
    print ""

# Function to extract features from a given file containing images
def getFeatures(filePath):
    # A map from image index to features
    features = dict()
	
    digitCount = 0
    x = 0
    image = [0 for a in range(imageWidth*imageHeight)]
    with open(filePath) as f:
        for line in f:
            line = line.strip('\n')
            # Assign numerical values corresponding to type of pixel space -> 0, plus -> 1, hash -> 2
            for c in line:
                if c == ' ':
                    image[x] = 0
                elif c == '+':
                    image[x] = 1
                elif c == '#':
                    image[x] = 2
                x += 1
            # One image processing done, store it and prepare for the next one
            if x == (imageWidth*imageHeight):
                # calculate gradient at each pixel
                gradImage = [0 for a in range(imageWidth*imageHeight)]
                for j in range(imageWidth,(imageWidth*imageHeight) - imageWidth - 1):
                    # calculating derivative in x and y direction using sobel detector 
                    g1x = image[j+1-imageWidth] - image[j-1-imageWidth]
                    g2x = 2*(image[j+1] - image[j-1])
                    g3x = image[j+1+imageWidth] - image[j-1+imageWidth]
                    gx = g1x + g2x + g3x
                    g1y = image[j-1+imageWidth] - image[j-1-imageWidth]
                    g2y = 2*(image[j+imageWidth] - image[j-imageWidth])
                    g3y = image[j+1+imageWidth] - image[j+1-imageWidth]
                    gy = g1y + g2y + g3y
                    # calculate the gradient direction at a given pixel
                    gradient = math.atan2(gy,gx)
                    # Assigning feature values as per the the gradient calculated
                    if gradient > 0 and gradient <= math.pi/4:
                        gradImage[j] = 0
                    elif gradient > math.pi/4 and gradient <= math.pi/2:
                        gradImage[j] = 1
                    elif gradient > math.pi/2 and gradient <= 3*math.pi/4:
                        gradImage[j] = 2
                    elif gradient > 3*math.pi/4 and gradient <= math.pi:
                        gradImage[j] = 3
                    elif gradient >= -math.pi and gradient <= -3*math.pi/4:
                        gradImage[j] = 4
                    elif gradient > -3*math.pi/4 and gradient <= -math.pi/2:
                        gradImage[j] = 5
                    elif gradient > -math.pi/2 and gradient <= -math.pi/4:
                        gradImage[j] = 6
                    elif gradient > -math.pi/4 and gradient <= 0:
                        gradImage[j] = 7
                features[digitCount] = gradImage
                x = 0
                digitCount += 1
                image = [0 for a in range(imageWidth*imageHeight)]
    return features

# Function to get labels from a given file
def getLabels(filePath):
    labels = dict()
    
    digitCount = 0
    x = 0
    with open(filePath) as f:
        for line in f:
            line = line.strip('\n')
            labels[digitCount] = int(line)
            digitCount += 1
    return labels

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HomeWork Five")
    parser.add_argument("--trainData", type=str)
    parser.add_argument("--trainLabel", type=str)
    parser.add_argument("--testData", type=str)
    parser.add_argument("--testLabel", type=str)
    args = parser.parse_args()
    main(args)
