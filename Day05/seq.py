import sys


"""Reads sequences from multiple files."""
def read_files(filenames):
    sequences = []

    for filename in filenames:
        try:
            with open(filename, 'r') as file:
                content = file.read().strip()
                sequences.append(content)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
    return sequences


    """Counts each type of nucleotide and unknown characters in a sequence."""
def calculate_statistics(sequence):
    counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'Un': 0}

    for char in sequence.upper():
        if char in counts:
            counts[char] += 1
        else:
            counts['Un'] += 1
    return counts


    """Prints the nucleotide statistics for a sequence."""
def display_statistics(counts, total, label=""):
    print(f"\nStatistics for: {label}")

    for nucleotide, count in counts.items():
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"{nucleotide}: {count:>5} ({percentage:>5.1f}%)")
    print(f"Total: {total:>5}")


    """Main function to process files and print statistics."""
def main():
    filenames = sys.argv[1:]
    combined_counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'Un': 0}
    combined_total = 0

    for file_name in filenames:
        sequences = read_files([file_name])
        sequence = sequences[0]  
        counts = calculate_statistics(sequence)
        total = sum(counts.values())  
        combined_total += total

        for key in combined_counts:
            combined_counts[key] += counts[key]  
        display_statistics(counts, total, label=file_name)

    if len(filenames) > 1: #Combined statistics for all files
        display_statistics(combined_counts, combined_total, label="All Files Combined")

# Run the main function
main()
