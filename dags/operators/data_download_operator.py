from azure.storage.blob import BlobServiceClient
#from config.constant import storage_account_key, storage_account_name, connection_string, container_name, blob_name, file_path_down

storage_account_key = "+w6iadskKBmzsPTwmDpkkXsuCcJ2XFcW2cmuh8fcAvXSFNVLOk2UpPwqWc2WMYNbDRT/aRqz+44c+ASt1yRMMA=="
storage_account_name = "cardstorage2"
connection_string = "DefaultEndpointsProtocol=https;AccountName=cardstorage2;AccountKey=+w6iadskKBmzsPTwmDpkkXsuCcJ2XFcW2cmuh8fcAvXSFNVLOk2UpPwqWc2WMYNbDRT/aRqz+44c+ASt1yRMMA==;EndpointSuffix=core.windows.net"
container_name = "cardcontainer2"
blob_name="Train11"
file_path_down="/home/unibash/G3/B/FRAUD_DETECTION_IN_IMBALANCED_DATA/data/raw/blobfile.csv"


def downloadFromBlobStorage():
    try:
        # Initialize a BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get a BlobClient for the target blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Download the blob to a local file
        with open(file_path_down, "wb") as data:
            data.write(blob_client.download_blob().readall())

        print(f"Downloaded {blob_name} from {container_name} to {file_path_down}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


downloadFromBlobStorage()
