
class storage_client_mock:

    def __init__(self, blob_data=dict()):
        ### If using blob_test, follow format ###
        # blob_test = {<name_of_blob>.<extension> : test data,
        #              <name_of_blob>.<extension> : test data}

        self.blob_data = dict()
        for key in blob_data:
            if type(key) == str:
                lower_key = key.lower()
                self.blob_data[lower_key] = blob_data[key]
        
        self.bucketz = dict()

    def list_buckets(self):
        return self.bucketz

    def bucket(self, bucket_name):
        if bucket_name in self.bucketz:
            return self.bucketz[bucket_name]

        temp_bucket = bucket_object(bucket_name, self.blob_data)
        self.bucketz[bucket_name] = temp_bucket
        return temp_bucket


class bucket_object:

    def __init__(self, bucket_name, blob_data):
        self.blob_data = blob_data
        self.bucket_name = bucket_name
        self.blobz = dict()

        for name in blob_data:
            self.blobz[name] = blob_object(name, blob_data[name])

    def list_blobs(self):
        return list(self.blobz.values())

    def blob(self, blob_name):
        blob_name = blob_name.lower()
        
        if blob_name in self.blobz:
            return self.blobz[blob_name]

        temp_blob = blob_object(blob_name)
        self.blobz[blob_name] = temp_blob
        return temp_blob

    def get_blob(self, blob_name):
        return self.blob(blob_name)


class blob_object:

    def __init__(self, blob_name, test_data=None):
        self.test_data = test_data
        self.name = blob_name
        self.public_url = False
        self.uploaded = None

    def exists(self):
        if not self.public_url:
            return False
        else:
            return True

    def _set_public_url(self, url_name):
        self.public_url = url_name

    def upload_from_string(self, content):
        self.uploaded = True
        self.public_url = 'test/test.com'
        self.string_content = content

    def upload_from_file(self, content):
        self.uploaded = True
        self.public_url = 'test/test.com'
        self.file_content = content

    def download_as_text(self, encoding=None):
        if self.uploaded:
            return self.string_content
        if self.test_data:
            return self.test_data
        return 'This is a test string from download_as_string'

    def download_as_string(self):
        if self.uploaded:
            return self.string_content.encode('utf-8')
        if self.test_data:
            return self.test_data.encode('utf-8')
        return 'This is a test string from download_as_string'.encode('utf-8')

    def download_to_filename(self):
        if self.uploaded:
            return self.file_content
        return 'This is a test from download_to_filename'

    def open(self, mode=None): 
        if self.test_data:
            data =  self.test_data       
        else:
            raise ValueError

        return [line.encode('utf-8') for line in data]


class mock_model_load:

    def __init__ (self, *args, **kwargs):
        pass

    def predict(self, data, *args, **kwargs):
        preds = [
            [0.1, 0.2, 0.3, 0.4],
            [0.2, 0.3, 0.4, 0.1],
            [0.3, 0.4, 0.1, 0.2]
        ]
        return preds


def mock_tokenizer_from_json(*args, **kwargs):
    return mock_tokenizer()


class mock_tokenizer:
    
    def __init__(self, *args, **kwargs):
        self.text = ['unk', 'world', 'there', 'hello', '<sos>', '<eos>']
        self.word_index = {'<sos>':4, '<eos>':5}
        print(self.word_index)

    def texts_to_sequences(self, data, *args, **kwargs):                      
        return [[1,2,3]]
    
    def sequences_to_texts(self, data, *args, **kwargs):
        return [self.text[idx] for idx in data]


def load_user_mock(data):
    mock_user = User_mock(data)
    return mock_user


class User_mock:

    def __init__(self, name):
        self.name = name
        self.id = 10

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False