#!python3
import pandas

read_file = 'test.csv'

def main():
    reader = pandas.read_csv(read_file)
    print(len(reader.values))

if __name__ == '__main__':
    main()