import matplotlib.pyplot as plt
import math

def show_plot(list1, list2, list3, list4):
    line_sample_normalized = plt.plot(list1)[0]
    line_energy_normalized = plt.plot(list2)[0]
    line_magnitude_normalized = plt.plot(list3)[0]
    line_zcr_normalized = plt.plot(list4)[0]
    
    plt.gca().yaxis.grid(True)
    
    ax = plt.subplot(111)
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    plt.legend([line_sample_normalized, line_energy_normalized, line_magnitude_normalized, line_zcr_normalized], ['Input', 'Energy', 'Magnitude', 'Zero-Crossing Rate'], loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.xlabel("Time")
    
    axes = plt.gca()
    axes.set_xlim([0, 2400])
    axes.set_ylim([-0.8, 1.2])
    
    plt.show()

def read_sample(file_path):
    with open(file_path) as f:
        sample = f.read().splitlines()

    sample = [int(i) for i in sample]

    return sample

def normalize(the_list, new_min, new_max):
    old_max = float(max(the_list))

    normalized_list = [0] * len(the_list)

    for i in range(0, len(the_list)):
        normalized_list[i] = the_list[i] / old_max
    
    return normalized_list
    
def sample_point_at_ms_func(ms):
    return int(ms * sampling_rate * 1000)
    
def sampling_rate_func(sample_count, ms_of_speech):
    return sample_count / ms_of_speech
    
def ideal_delay_func(original, delay):
    n0 = int(delay * sampling_rate * 1000)

    # fill in the delay with zeros
    ideal_delay = [0] * n0

    for i in range(n0, len(original)):
	ideal_delay.append(original[i - n0])

    return ideal_delay

def moving_average_func(sample, k1_ms, k2_ms):
    moving_average = [0] * len(sample)

    sum = 0

    k1 = sample_point_at_ms_func(k1_ms)
    k2 = sample_point_at_ms_func(k2_ms)

    for i in range(0, sample_count):
        for j in range(i - k1, i + k2 + 1):
            if(j >= 0 and j < len(sample)):
                sum += sample[j]

        sum = sum / (k1 + k2 + 1)

        moving_average[i] = sum
        
        sum = 0
        
    return moving_average

def convolution_func(sample, window):
    convolution = [0] * len(sample)

    sum = 0

    for i in range(0, len(sample)):
        for j in range(i - window + 2, i + 1):
            if(j >= 0):
                sum += sample[j]

        convolution[i] = sum
        
        sum = 0
        
    return convolution

def energy_func(sample, window):
    energy = [0] * len(sample)

    sum = 0

    for i in range(0, len(sample)):
        for j in range(i - window + 1, i + 1):
            if(j >= 0):
                sum += sample[j] * sample[j]

        energy[i] = sum

        sum = 0
       
    return energy

def magnitude_func(sample, window):
    magnitude = [0] * len(sample)

    sum = 0

    for i in range(0, len(sample)):
        for j in range(i - window + 1, i + 1):
            if(j >= 0):
                sum += abs(sample[j])

        magnitude[i] = sum
        
        sum = 0
        
    return magnitude

def zcr_func(sample, window):
    zcr = [0] * len(sample)

    sum = 0.0

    for i in range(0, len(sample)):
        for j in range(i - window + 1, i + 1):
            if(j > 0):
                sum += math.fabs(float(sign_func(sample[j]) - sign_func(sample[j - 1])))
        
        sum = float(sum / (2 * window))
        
        zcr[i] = sum

        sum = 0
        
    return zcr

def sign_func(number):
    if(number >= 0):
        return 1
    else:
        return 0
    
def main():
    pass

if __name__ == "__main__":
    sample = read_sample('lab1files/laboratory.dat')

    ms_of_speech = 300
    sample_count = len(sample)
    sampling_rate = sampling_rate_func(sample_count, ms_of_speech)
    window_size_10 = 10 * sampling_rate # 10ms window
    window_size_30 = 30 * sampling_rate # 30ms window
    
    # 5ms delay
    ideal_delay = ideal_delay_func(sample, 0.005)
    
    # 10ms delay
    ideal_delay = ideal_delay_func(sample, 0.01)
    
    # 15ms delay
    ideal_delay = ideal_delay_func(sample, 0.015)
    
    # moving average with 5ms for k1, k2
    moving_average = moving_average_func(sample, 0.005, 0.005)
    
    # moving average with 10ms for k1, k2
    moving_average = moving_average_func(sample, 0.01, 0.01)
    
    # moving average with 15ms for k1, k2
    moving_average = moving_average_func(sample, 0.015, 0.015)
    
    # convolution with window length 10ms
    convolution = convolution_func(sample, window_size_10)
    
    # short-term energy signal with window length 30ms
    energy = energy_func(sample, window_size_30)
    
    # short-term magnitude signal with window length 30ms
    magnitude = magnitude_func(sample, window_size_30)
    
    # short-term zero crossing rate signal with window length 30ms
    zcr = zcr_func(sample, window_size_30)
    
    # normalize values
    sample_normalized = normalize(sample, -1, 1)
    ideal_delay_normalized = normalize(ideal_delay, -1, 1)
    moving_average_normalized = normalize(moving_average, -1, 1)
    convolution_normalized = normalize(convolution, -1, 1)
    energy_normalized = normalize(energy, 0, 1)
    magnitude_normalized = normalize(magnitude, 0, 1)
    ideal_delay_normalized = normalize(ideal_delay, -1, 1)
    zcr_normalized = normalize(zcr, 0, 1)
    
    print "ms_of_speech", ms_of_speech
    print "sample_count", sample_count
    print "sampling_rate", sampling_rate
    
    show_plot(sample_normalized, energy_normalized, magnitude_normalized ,zcr_normalized)
