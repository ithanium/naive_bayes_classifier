import matplotlib.pyplot as plt
import lab1
import os
import math

def plot(list1, list2, label):
    plt.scatter(list1, list2)    
    plt.xlabel(label)
    plt.show()
    
def average(the_list):
    sum = 0
    
    for i in range(0, len(the_list)):
        sum += the_list[i]

    return sum/len(the_list)

def log_average(the_list):
    sum = 0

    for i in range(0, len(the_list)):
        sum += the_list[i]
        
    return math.log(sum/len(the_list))

def write_to_file(the_list, file_path):
    the_file = open(file_path, 'w')
    
    for item in the_list:
        the_file.write("%s\n" % item)

def process_files():
    i = 0
    
    for file_name in os.listdir("lab2files/silence_speech"):
        if file_name.endswith(".dat"):
            print "Processing", file_name
            sample = lab1.read_sample("lab2files/silence_speech/" + file_name)

            ms_of_speech = 300
            sample_count = len(sample)
            sampling_rate = lab1.sampling_rate_func(sample_count, ms_of_speech)
            window_size_10 = 10 * sampling_rate # 10ms window
            window_size_30 = 30 * sampling_rate # 30ms window

            energy = lab1.energy_func(sample, window_size_30)
            e[i] = log_average(energy)
            
            magnitude = lab1.magnitude_func(sample, window_size_30)
            m[i] = log_average(magnitude)
            
            zcr = lab1.zcr_func(sample, window_size_30)
            z[i] = average(zcr)
            
            i += 1
            
def main():
    pass

if __name__ == "__main__":
    e = [0] * 100
    m = [0] * 100
    z = [0] * 100
    
    process_files()
    
    write_to_file(e, "e.txt")
    write_to_file(m, "m.txt")
    write_to_file(z, "z.txt")
    
    plot(e, m, "Energy against Magnitude")
    plot(e, z, "Energy against Zero-Crossing Rate")
    plot(m, z, "Magnitude against Zero-Crossing Rate")
