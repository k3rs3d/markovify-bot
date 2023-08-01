import os
import argparse
import markovify
import json


def read_text_from_files(directory):
    text = ""
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r') as file:
                    text += file.read() + "\n"
    except Exception as e:
        print(f"An error occurred while reading files: {e}")
    return text


def build_model(directory, model_file, state_size=2):
    text = read_text_from_files(directory)
    text_model = markovify.Text(text, state_size=state_size)
    model_json = text_model.to_json()

    try:
        with open(model_file, 'w') as file:
            file.write(model_json)
        print(f"Model has been built and saved to {model_file}")
    except Exception as e:
        print(f"An error occurred while saving the model: {e}")


def generate_sentence(model_file, count=1, tries=32, overlap_ratio=0.5):
    if not os.path.exists(model_file):
        print(f"Model file {model_file} does not exist. Switching to build mode.")
        build_model('input', model_file)

    try:
        with open(model_file, 'r') as file:
            model_json = file.read()

        text_model = markovify.Text.from_json(model_json)

        sentences = []
        for _ in range(count):
            sentence = text_model.make_sentence(tries=tries, max_overlap_ratio=overlap_ratio)
            if sentence is not None:
                sentences.append(sentence)
        print("\n".join(sentences))

    except Exception as e:
        print(f"Error occurred while generating: {e}")


def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Generate a random sentence or build a model based on text files in a directory.")

    # Add the arguments
    parser.add_argument('-d', '--Directory', metavar='directory', type=str, help='the directory to read text files from', default='input')
    parser.add_argument('-m', '--Mode', metavar='mode', type=str, help='the mode of operation - "build" or "run"', default='run')
    parser.add_argument('-f', '--File', metavar='file', type=str, help='the file to save/load the model', default='model.json')
    parser.add_argument('-s', '--StateSize', metavar='state_size', type=int, help='the state size of the Markov model', default=3)
    parser.add_argument('-t', '--Tries', metavar='tries', type=int, help='the number of tries for generating a sentence', default=32)
    parser.add_argument('-o', '--OverlapRatio', metavar='overlap_ratio', type=float, help='the maximum overlap ratio', default=0.8)
    parser.add_argument('-c', '--Count', metavar='count', type=int, help='the number of sentences to generate', default=1)

    # Execute the parse_args() method
    args = parser.parse_args()

    if args.Mode.lower() == "build":
        build_model(args.Directory, args.File, args.StateSize)
    elif args.Mode.lower() == "run":
        generate_sentence(args.File, args.Count, args.Tries, args.OverlapRatio)
    else:
        print(f"Unknown mode: {args.Mode}")


if __name__ == "__main__":
    main()
