import pickle


PICKLE_FILE = 'encoding.pickle'


def main():
    # append data to the pickle file

    for item in read_from_pickle(PICKLE_FILE):
        print(repr(item))



def read_from_pickle(path):
    with open(path, 'rb') as file:
        try:
            while True:
                yield pickle.load(file)
        except EOFError:
            pass


if __name__ == '__main__':
    main()
