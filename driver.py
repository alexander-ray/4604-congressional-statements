from feature_processor import Feature_Processor
import json

def main():
    fp = Feature_Processor()
    #fp.get_features("https://projects.propublica.org/represent/statements?page=", 1)
    tmp = {}
    with open("test.txt") as json_file:
        tmp = json.load(json_file)

    print(tmp)
if __name__ == '__main__':
    main()