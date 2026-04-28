import glob
import os


def combine_and_truncate_per_file(input_folder, output_filename, limit):
    filenames = glob.glob(os.path.join(input_folder, "*.txt"))
    if not filenames:
        print(f"No files found in {input_folder}")
        return

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for fname in filenames:
            file_word_count = 0
            with open(fname, 'r', encoding='utf-8') as infile:
                for line in infile:
                    words = line.split()
                    line_len = len(words)

                    if file_word_count + line_len <= limit:
                        outfile.write(line)
                        file_word_count += line_len
                    else:
                        words_needed = limit - file_word_count
                        if words_needed > 0:
                            outfile.write(" ".join(words[:words_needed]) + "\n")
                        break

            print(f"Added {file_word_count} words from {os.path.basename(fname)}")

    print(f"--- Successfully created {output_filename} ---")


word_limit = 727500 # min tokens per input file post-cleaning and lemmatization
combine_and_truncate_per_file("samples_A_clean", "corpus_A/corpus_A.txt", word_limit)
combine_and_truncate_per_file("samples_B_clean", "corpus_B/corpus_B.txt", word_limit)
