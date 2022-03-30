# Solutions for Conductive Backend Test

## Introduction

Firstly, I would like to thank the people at Conductive for giving me the opportunity to participate in this assessment. I have enjoyed working on the assessment and I thought it was really good. This document contains my findings and an explanation for the implementation choices made during the assignment. If you have any further queries, please do not hesitate to forward them to me at **abrarhgalib@gmail.com**. Thanks and have a great day!

## Solutions for Part 1

Part 1 involved reading the entire data set and generating statiscal information from this. The data set is a list of schools in US with their names, geo location and metro locale ranking among other attributes. Specifically, the following questions were of interest:

1. How many schools are there in total?

2. How many schools are there per state?

3. Which city has the highest number of schools and how many schools are there in that city?

4. How many schools are there per metro-centric locale (1-8, N for unassigned)?

5. How many unique cities have at least one school in it?

The entire data set is loaded into memory as a `list` of `dict` with only the required attributes being mapped. A friendlier name was used for mapping these values compared to the original headings in the CSV file.

Each question is unique and the logical approach is to define a separate function/method that processes the dataset (without side effect i.e.,) and yields the required answer. However, if performance is considered, it will be clear that a single function should process the entire dataset and produce all the answer. The advantage in doing so is that the entire dataset can then be processed in a single pass and each groups can be extracted as necessary. While this is not ideal for situations where runtime memory may be low but otherwise provides an efficient albeit less maintainable (or readable) chunk of function/method.

In the case of the solution, a single function was exported to the user. This function can be modified to either separately process the answer in a separate method or process them in one method. The default will always use the latter approach (dubbed as **"fast"**). You can also check **slow** version that uses separate methods.

## Solution for Part 2

This part of the question was more interesting. Full text search is an interesting problem in CS. For this part of the problem, this problem is presented in the following form:

1. Given the dataset, allow the user to find schools by name, city and/or state. Show three best possible choices to the user.

The complications arise when you start thinking about "best choices". How do you rank names of school or city? How do you decide which names are "closer" or "matches better" compared to other names? Finally, how do you provide all that under **200ms**?

There are many possible ways in which this problem can be addressed:

1. Linearly searching through the dataset and using a pattern match against all school names, city names and/or state names

2. Using a sorted list and using Binary Search on the sorted list

3. Using a Trie data structure

Approach 1 is simple to understand and implement, it does not perform well and takes longer than **200ms** on average. So the choice was between 2 and 3. Approach 3 adds many more complexities to the implementation; also, it only makes more sense in context where newer entries are added to the dataset during runtime which is not the case here. Therefore, approach 2 looks like the more desirable option to go for, both in terms of its fairly simple implementation and its performance (or rather time complexity).

Now that performance is satisfactory, there still remains the question of ranking strings. There are many metrics for comparing string and determining their closeness like **Levenshtein Distance**, **Smith-Waterman-Gotoh** algorithms. However, these algorithms are much slower when comparing a large number of strings. This presents a slight issue regarding binary search: binary search generally looks for an exact match; this means typos, spelling mistakes can render incorrect results. To make UX better, the school names were converted to `lowercase` and all spaces were removed. Furthermore, sorting also uses lexicographic order (or natural ordering). This presents another issue: what if the result is not found? In that case, consider the following:

1. In binary search, there are two partitions: left and right

2. For each, there are pointers `lo` and `hi`

3. Once the search loop exits, in this case `lo` > `hi`, specifically `lo = hi+1`. This position is known as the indexing point (or where the entry should have been if it was present). So that means entries at `lo` and `hi` are on either side of the search key and based on lexicographic ordering, are the closest ones to the search key

## Other Information

1. The name of the CSV file is hard coded into both scripts. To change, change the variable `fname` in the script

2. There are some utility functions in `utils.py` file