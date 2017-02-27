from math import log
import matplotlib.pyplot as plt

def show_frequency_by_rank(vocabulary_with_frequencies):
    if "" in vocabulary_with_frequencies:
        del vocabulary_with_frequencies[""]
    ordered_term_values = sorted(vocabulary_with_frequencies, key=vocabulary_with_frequencies.get)
    # Normal values
    y_values = [vocabulary_with_frequencies[term] for term in ordered_term_values]
    y_values.reverse()
    x_values = range(1, len(ordered_term_values) + 1)
    show(x_values, "Rang r", y_values, "Fréquence : f")
    # Values with log
    y_log_values = [log(value, 10) for value in y_values]
    x_log_values = [log(value, 10) for value in x_values]
    show(x_log_values, "Logarithme du rang : log(r)", y_log_values, "Logarithme de la fréquence : log(f)")

def show(x_values, x_label, y_values, y_label):
    plt.plot(x_values, y_values)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.show()