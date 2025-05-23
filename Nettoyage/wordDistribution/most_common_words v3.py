import pandas as pd
import matplotlib.pyplot as plt

# Parameters
n_words_graph = 50  # Number of words to plot
n_words_csv = -1  # Number of words to save to CSV (-1 for all)
name_input = "datasets/Reviews.csv"
name_output = "Nettoyage/wordDistribution/most_common_words.csv"

# Functions
def ExtractTextFromDataFrame(texts):
    print("Reading data...")
    
    text_stripped = list(texts.str.replace('[^a-zA-Z0-9]', ' ', regex=True).str.lower().str.split().tolist())
    text_punctuation = list(texts.str.replace('[^!?]', ' ', regex=True).str.split().tolist())

    text_extracted = []
    for i in range(len(text_stripped)):
        text_extracted.append(text_stripped[i]+text_punctuation[i])
    
    return text_extracted


def CountWordFrequency(text_extracted):
    print("Counting word frequencies...")
    
    words_count = {}
    for line in text_extracted:
        for word in line:
            if word in words_count:
                words_count[word] += 1
            else:
                words_count[word] = 1

    return words_count


def CountWordScore(text_extracted, scores):
    print("Counting word scores...")
    
    words_score = {}
    for i, line in enumerate(text_extracted):
        for word in line:
            score = scores[i] # Get the score for the current line
            
            if word in words_score:
                if score in words_score[word]:
                    words_score[word][score] += 1
                else:
                    words_score[word][score] = 1
            else:
                words_score[word] = {score: 1}
    
    for score in range(1, 6):
        for word in words_score:
            if score not in words_score[word]:
                words_score[word][score] = 0

    return words_score

# Combine all the information into a single line
def CreateLine(words_count, words_score):
    print("Combining word frequency and score...")
    
    lines = []
    
    for word in words_count:
        line = {"word": word, "count": words_count[word]}
        for score in range(1, 6):
            if score in words_score[word]:
                line[str(score)] = words_score[word][score]
            else:
                line[str(score)] = 0
        lines.append(line)
        
    return lines


def SaveToCSV(word_sorted, name_output, n_words_csv=-1):
    print("Saving to CSV...")
    
    if n_words_csv == -1:
        n_words_csv = len(word_sorted)

    output_csv = pd.DataFrame(word_sorted[:n_words_csv], columns=['word', 'count', '1', '2', '3', '4', '5'])
    output_csv.to_csv(name_output, index=False)


# Load data
df = pd.read_csv(name_input)
texts = df['Text']
scores = df['Score']


# extract useful information
text_extracted = ExtractTextFromDataFrame(texts)
words_count = CountWordFrequency(text_extracted)
words_score = CountWordScore(text_extracted, scores)


# combine word frequency and score
words_lines = CreateLine(words_count, words_score)

# sort the dictionary by frequency
print("Sorting...")
words_sorted = sorted(words_lines, key=lambda x: x["count"], reverse=True)

# save to csv
SaveToCSV(words_sorted, name_output, n_words_csv)

# plot the word counters
if n_words_graph == -1:
    n_words_graph = len(words_sorted)

total_number_words = sum(x["count"] for x in words_sorted)
words_to_plot = [x["word"] for x in words_sorted[:n_words_graph]]
counts_to_plot = [x["count"]/total_number_words for x in words_sorted[:n_words_graph]]

plt.figure(figsize=(12, 8))
plt.bar(range(n_words_graph), counts_to_plot, align='center')
plt.xticks(range(n_words_graph), words_to_plot, rotation=90)
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.title(f'Top {n_words_graph} Most Common Words')
plt.show()
