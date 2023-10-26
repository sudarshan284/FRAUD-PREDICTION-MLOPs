from azure.storage.blob import BlobServiceClient
#from config.constant import storage_account_key, storage_account_name, connection_string, container_name, file_path_up, file_name

storage_account_key = "+w6iadskKBmzsPTwmDpkkXsuCcJ2XFcW2cmuh8fcAvXSFNVLOk2UpPwqWc2WMYNbDRT/aRqz+44c+ASt1yRMMA=="
storage_account_name = "cardstorage2"
connection_string = "DefaultEndpointsProtocol=https;AccountName=cardstorage2;AccountKey=+w6iadskKBmzsPTwmDpkkXsuCcJ2XFcW2cmuh8fcAvXSFNVLOk2UpPwqWc2WMYNbDRT/aRqz+44c+ASt1yRMMA==;EndpointSuffix=core.windows.net"
container_name = "cardcontainer2"
file_path_up = "/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/data/raw/Train1.csv"
file_name = "Train11"


def uploadToBlobStorage():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container = container_name, blob = file_name)

        with open(file_path_up,"rb") as data:
            blob_client.upload_blob(data)
        print("Upload " + file_name + " from local to container " + container_name)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

uploadToBlobStorage()

#uploadToBlobStorage(file_path_up,file_name)


