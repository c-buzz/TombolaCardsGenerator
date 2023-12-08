# TombolaCardsGenerator
Script for the generation of a sequence of 6 Tombola cards.

Each cards sequence (6 cards) must follow these rules:
 - All 90 numbers in range [1-90] must be used throughout the cards
 - Each card must contain 15 numbers in a matrix 3 x 9
 - Each card row must contain exactly 5 numbers
 - Each card column must contain maximum 3 numbers in the range [col*10; col*10+9] (col is column index [0-8]), with the exception of first ([1-9]) and last column ([80-90])

A card is represented as a 3x9 `numpy` array where a value 0 is used as a placeholder for _no number_

