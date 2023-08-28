import os

def collect_python_files_content(root_folder):
    qa_pairs = []
    
    # Recursively walk through directories
    for dirpath, dirnames, filenames in os.walk(root_folder):
        print(f"Processing {dirpath}...")
        for filename in filenames:
            if filename.endswith(".py"):
                print(f"Processing {filename}...")
                question = filename[:-3]  # Remove .py extension
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    print(f"Reading {file_path}")
                    try:
                        answer = file.read()
                        qa_pairs.append((question, answer))
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
    return qa_pairs

def save_to_txt(qa_pairs, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as f:
        for question, answer in qa_pairs:
            f.write("Question: " + question + "\n")
            f.write("Answer: " + answer + "\n")
            f.write("---\n")

if __name__ == "__main__":
    root_folders = ["datasets/tutorials_python", "datasets/plot_types_python", "datasets/gallery_python"]
    all_qa_pairs = []
    
    for root_folder in root_folders:
        print(f"Processing {root_folder}...")
        all_qa_pairs.extend(collect_python_files_content(root_folder))
    
    save_to_txt(all_qa_pairs, "wip_qa_dataset.txt")
    print("Dataset saved to wip_qa_dataset.txt")
