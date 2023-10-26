import shutil

abc = "/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/result/evaluation_abc_results.txt"
dtc = "/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/result/evaluation_dtc_results.txt"
gbc = "/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/result/evaluation_gbc_results.txt"
rfc = "/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/result/evaluation_rfc_results.txt"

def  modelselection():
    file_paths = [abc, dtc, gbc, rfc]

    max_accuracy = -1.0  # Initialize with a very low value
    best_file = None

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            file_contents = file.read()

        # Find the accuracy in the file
        accuracy = None
        for line in file_contents.split('\n'):
            if line.startswith("Accuracy:"):
                accuracy = float(line.split(":")[1].strip())

        # Update if a higher accuracy is found
        if accuracy is not None and accuracy > max_accuracy:
            max_accuracy = accuracy
            best_file = file_path


    print(f"The file with the highest accuracy is {best_file} with an accuracy of {max_accuracy}")

    if best_file=="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/result/evaluation_abc_results.txt":
        best_model="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/abc_model.pkl"
        final_model="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/final_model.pkl"
        shutil.copy(best_model, final_model)

    elif best_file=="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/result/evaluation_dtc_results.txt":
        best_model="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/dtc_model.pkl"
        final_model="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/final_model.pkl"
        shutil.copy(best_model, final_model)

    elif best_file=="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/result/evaluation_gbc_results.txt":
        best_model="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/gbc_model.pkl"
        final_model="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/final_model.pkl"
        shutil.copy(best_model, final_model)
        
    else:
        best_file=="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/result/evaluation_rfc_results.txt"
        best_model="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/rfc_model.pkl"
        final_model="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/models/final_model.pkl"
        shutil.copy(best_model, final_model)

modelselection()