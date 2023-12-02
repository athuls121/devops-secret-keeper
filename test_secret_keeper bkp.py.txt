import unittest
from pywebio import start_server
import requests
import os  # Import os module to access environment variables

class TestSecretKeeper(unittest.TestCase):
    def setUp(self):
        # Fetch the external IP from the environment variable
        self.external_ip = os.getenv('EXTERNAL_LOAD_BALANCER_IP')
        if self.external_ip:
            print("External Load Balancer IP:", self.external_ip)
            # Start the PyWebIO server in a separate thread for testing
            self.server_thread = threading.Thread(target=self.start_pywebio_server)
            self.server_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
            self.server_thread.start()
        else:
            raise Exception("Failed to fetch the External Load Balancer IP")

    def start_pywebio_server(self):
        start_server(lambda: None, port=8083)  # Use a dummy function as we're testing IP accessibility, not server functionality

    def test_application_up(self):
        # Test if the application is up by sending a GET request to the load balancer IP
        url = f"http://{self.external_ip}/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)  # Should return a 200 status code

if __name__ == '__main__':
    unittest.main()
