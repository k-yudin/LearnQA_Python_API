import requests
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
obj = response.json()
token = obj['token']
job_to_finish_in_sec = obj['seconds']

response_before_job_done = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token': token})
obj_before_job_done = response_before_job_done.json()
if obj_before_job_done['status'] == 'Job is NOT ready':
    print(f"Job is not done yet, please wait for {job_to_finish_in_sec} seconds...")
else:
    print("Response object has invalid status parameter")

time_buffer_in_sec = 1
time.sleep(job_to_finish_in_sec+time_buffer_in_sec)

response_after_job_done = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token': token})
obj_after_job_done = response_after_job_done.json()

if obj_after_job_done['status'] == 'Job is ready' and obj_after_job_done['result'] is not None:
    print(f"Job is finished, result: {obj_after_job_done['result']}")
else:
    print(obj_after_job_done['status'])
