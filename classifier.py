import math
import random

def read_list(file_path):
    with open(file_path) as f:
        sample = f.read().splitlines()

    return sample

def load_original_data():
    e = [0] * 100
    m = [0] * 100
    z = [0] * 100
    
    e = read_list("e.txt")
    m = read_list("m.txt")
    z = read_list("z.txt")
    
    fcemz = [0] * 100

    for i in range(0, 100):
        if(i < 50):
            file_name = "silence_" + str(i).zfill(2)
            class_name = "silence"
        else:
            file_name = "speech_" + str(i).zfill(2)
            class_name = "speech"
            
        fcemz[i] = [file_name, class_name, e[i], m[i], z[i]]

    return fcemz

def split_data_into_groups(data, cross_validation_k, items_per_group):
    groups = [[]] * cross_validation_k

    # Randomly shuffle the original data
    random.shuffle(data)

    # With the original data now random
    # Make k groups of length k items
    for i in range(0, cross_validation_k):
        groups[i] = data[i * items_per_group : (i+1) * items_per_group]

    return groups
        
def train_classifier():
    global known_classes
    global training_groups

    total = {}
    values = {}

    for item in training_groups:
        # item[0] = file_name
        # item[1] = class_name
        # item[2] = e
        # item[3] = m
        # item[4] = z
        
        if any(item[1] in s for s in known_classes) == False:
            # Discovered a new class (i.e. speech, silence)
            # Therefore, add it to known classes
            known_classes += [str(item[1])]
                
        for i in range(2, 5):
            # For every attribute e, m, z
            # Store its total and each value
            # To later calculate mean and stdev
            attribute_name = "e"
            
            if(i == 3):
                attribute_name = "m"
            if(i == 4):
                attribute_name = "z"

            if(str(item[1]) + attribute_name not in total.keys()):
                total[str(item[1]) + attribute_name] = 0
                
            if(str(item[1]) + attribute_name not in values.keys()):
                values[str(item[1]) + attribute_name] = []

            total[str(item[1]) + attribute_name] += float(item[i])
            values[str(item[1]) + attribute_name] += [float(item[i])]
                
    for class_attribute in total.keys():
        # For every class and attribute combination
        # Compute the mean and standard deviation 
        p = len(values[class_attribute])
        mean[class_attribute] = total[class_attribute] / p

        variance = 0

        for value in values[class_attribute]:
            variance += math.pow(value - mean[class_attribute], 2)

        variance = variance / p
        stdev[class_attribute] = math.sqrt(variance)

def compute_probability(class_name, attribute, val):
    # Compute probability of the attribute having
    # a value val in class class_name
    mu = float(mean[class_name + attribute])
    std = float(stdev[class_name + attribute])
    val = float(val)

    return (1/math.sqrt(2 * math.pi * std)) * math.exp((-math.pow(val - mu, 2)) / (2 * math.pow(std, 2)))

def test_classifier(e, m, z): 
    max_probability = 0
    result = []
    probabilities = []
    class_name_result = ""

    # We were given 50/50 speech/silence files
    prior_probability_of_each_class = 0.5

    for class_name in known_classes:
        # Compute probability of audio clip having a class of speech, then a class of silence
        probability = compute_probability(class_name, "e", e) * compute_probability(class_name, "m", m) * compute_probability(class_name, "z", z) * prior_probability_of_each_class

        if(probability > max_probability):
            class_name_result = class_name
            max_probability = probability

        probabilities += [[class_name, "%.5f" % probability]]

    return [class_name_result, probabilities]

known_classes = []
training_groups = []

mean = {}
stdev = {}

fcemz = load_original_data()
cross_validation_k = 10 # k groups used for k-fold validation
items_per_group = len(fcemz) / cross_validation_k
groups = split_data_into_groups(fcemz, cross_validation_k, items_per_group)

current_fold_correct = 0
total_correct = 0

print "Running K-fold validation with k =", cross_validation_k, "\n"

for i in range(0, cross_validation_k):
    print "Running fold", i

    # Start training from scratch
    known_classes = []
    training_groups = []
    
    # Train with k - 1 groups
    # So we can later use 1 group for validation
    for j in range(0, cross_validation_k):
        # Keep 1 group for validation
        if(i != j):
            print "Using group", j, "for training"

            for k in range(0, items_per_group):
                training_groups += [groups[j][k]]
    
    print "Training the classifier with", len(training_groups), "items"

    train_classifier()
    
    print "Classifying data from group", i
    
    current_fold_correct = 0

    for j in range(0, len(groups[i])):
        response = test_classifier(groups[i][j][2], groups[i][j][3], groups[i][j][4])

        result = response[0]
        probabilities = response[1]

        print "Choosing", result.ljust(7), "for file", groups[i][j][0].ljust(10), "(Probability for", probabilities[0][0], "was:", probabilities[0][1], "and for", probabilities[1][0], "was:", probabilities[1][1] + ")", "X" if result != groups[i][j][1] else ""
        
        if(result == groups[i][j][1]):
            current_fold_correct += 1
            
    print "Result for fold", str(i) + ":", current_fold_correct," out of ", items_per_group, "correct classifications (loss for fold:", str(1.0 * (items_per_group - current_fold_correct) / cross_validation_k) + ")\n"
    
    total_correct += current_fold_correct
    
print "Classifier finished running with an average classification accuracy of", 1.0 * total_correct / cross_validation_k / items_per_group, "(average loss:", str(1.0 - 1.0 * total_correct / cross_validation_k / items_per_group) + ")"
