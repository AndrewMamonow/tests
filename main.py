import unittest
import requests


documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
        {"type": "driver license", "number": "5455 028765", "name": "Василий Иванов"},
      ]

directories = {
        '1': ['2207 876234', '11-2', '5455 028765'],
        '2': ['10006'],
        '3': []
      }

def get_name(doc_number):

    for document in documents:
        if doc_number == document['number']:
            return document['name']
    return "Документ не найден"
    
def get_directory(doc_number):
    #
    for shelf_number in directories.keys():
        #number_list = directories[shelf_number]
        if doc_number in directories[shelf_number]:
            return shelf_number
    return "Полки с таким документом не найдено"
            
def add_document(document_type, number, name, shelf_number):
    #
    documents_dict={'type':document_type,
    'number':number,
    'name':name}
    documents.append(documents_dict)
    directories.setdefault(str(shelf_number), [])
    directories[str(shelf_number)].append(number)
    return directories[str(shelf_number)]

def remove_document(number):
    for directory_number, directory_docs_list in directories.items():
        if number in directory_docs_list:
            directory_docs_list.remove(number)
            return True
            break
    return False


class TestSomething(unittest.TestCase):
   
    def test_get_name(self):
        for document in documents:
            self.assertEqual(get_name(document['number']), document['name'])

    def test_get_name_false(self):
        self.assertEqual(get_name(''), "Документ не найден")
    
    def test_get_directory(self):
        for key, value in directories.items():
            for document in value:
                self.assertEqual(get_directory(document), key)

    def test_get_directory_false(self):
        self.assertEqual(get_directory(''), "Полки с таким документом не найдено")

    def test_add_document(self):
        self.assertIn('311 020203', add_document('international passport', '311 020203', 'Александр Пушкин', 3))

    def test_add_document_false(self):
        self.assertNotIn('', add_document('international passport', '311 020203', 'Александр Пушкин', 3))

    def test_remove_documen(self):
        self.assertTrue(remove_document('311 020203'))

    def test_remove_documen(self):
        self.assertFalse(remove_document(''))



class YandexDiskTest(unittest.TestCase):
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    TOKEN = ''

    def setUp(self):
        self.headers = {
                        'Authorization': self.TOKEN
                        }
        self.folder_name = "Images"
        self.folder_path = self.folder_name
        self.folder_path = {
                'path': self.folder_name
                }        
    def tearDown(self):
        # Удаление папки после теста
        requests.delete(self.BASE_URL, params=self.folder_path, headers=self.headers)

    def test_create_folder_success(self):
        # Тест на успешное создание папки
        response = requests.put(self.BASE_URL, params=self.folder_path, headers=self.headers)
        self.assertEqual(response.status_code, 201)  

    def test_exist_folder_success(self):
        # Тест на наличие папки
        requests.put(self.BASE_URL, params=self.folder_path, headers=self.headers)
        response = requests.get(self.BASE_URL, params=self.folder_path, headers=self.headers)
        self.assertEqual(response.status_code, 200)  
    
    def test_create_folder_exists(self):
        # Тест на повторное создание папки
        requests.put(self.BASE_URL, params=self.folder_path, headers=self.headers)
        response = requests.put(self.BASE_URL, params=self.folder_path, headers=self.headers)
        self.assertEqual(response.status_code, 409)

    def test_folder_invalid_path(self):
        # Тест на наличие папки с недопустимым путем
        invalid_path = {
                'path': "//folder\name"
                }        
        response = requests.get(self.BASE_URL, params=invalid_path, headers=self.headers)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
   


    