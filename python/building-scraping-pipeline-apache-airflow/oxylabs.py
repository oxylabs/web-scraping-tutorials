import requests

JOB_STATUS_DONE = 'done'

HTTP_NO_CONTENT = 204


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_jobs(self, urls):
        payload = {
            'source': 'universal_ecommerce',
            'url': urls
        }

        response = requests.request(
            'POST',
            'https://data.oxylabs.io/v1/queries/batch',
            auth=(self.username, self.password),
            json=payload,
        )

        return response.json()

    def is_status_done(self, job_id):
        job_status_response = requests.request(
            method='GET',
            url='http://data.oxylabs.io/v1/queries/%s' % job_id,
            auth=(self.username, self.password),
        )

        job_status_data = job_status_response.json()

        return job_status_data['status'] == JOB_STATUS_DONE

    def fetch_content_list(self, job_id):
        job_result_response = requests.request(
            method='GET',
            url='http://data.oxylabs.io/v1/queries/%s/results' % job_id,
            auth=(self.username, self.password),
        )
        if job_result_response.status_code == HTTP_NO_CONTENT:
            return None

        job_results_json = job_result_response.json()

        return job_results_json['results']