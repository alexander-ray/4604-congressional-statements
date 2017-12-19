# 4604-congressional-statements
Applied Machine Learning (INFO 4604) final project on congressional statements.

driver.py has the main driver code for logistic regression, linear svm, and lda. Also includes some helper functions.
Everything in "main" in driver should just be some combination of calling the other functions. The code there now is only to get LDA results.

feature_processor.py has the named entity removal functions, as well as a data-retrieval driver function.

scraper.py has the web scraping code, as well as the driver function to split datasets and save to file.

plotting.py has the plotting code for charts seen on the ppt.

Obviously lots of stackoverflow and scikit-learn documentation was used for debugging and syntax questions, but all functions based on stackoverflow responses or scikit-learn examples have a link to the relevant code above the function.
Most learning and plotting code is from class homework assignments. The basic BS4 scraper structure is from a previous project at https://github.com/alexander-ray/stump_speech_analysis/blob/master/speech_scraper.py


